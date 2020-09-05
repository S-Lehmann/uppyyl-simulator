"""All classes for a system state representation, including location state, variable state, and clock state."""
import collections
import copy
import itertools
import pprint
from typing import Dict

from uppyyl_simulator.backend.ast.evaluators.uppaal_c_evaluator import UppaalCEvaluator
from uppyyl_simulator.backend.data_structures.dbm.dbm import DBM
from uppyyl_simulator.backend.data_structures.state.variable import UppaalVariable
from uppyyl_simulator.backend.data_structures.types.reference import UppaalReference
from uppyyl_simulator.backend.data_structures.types.array import UppaalArray
from uppyyl_simulator.backend.data_structures.types.bool import UppaalBool
from uppyyl_simulator.backend.data_structures.types.bounded_int import UppaalBoundedInt
from uppyyl_simulator.backend.data_structures.types.chan import UppaalChan
from uppyyl_simulator.backend.data_structures.types.clock import UppaalClock
from uppyyl_simulator.backend.data_structures.types.int import UppaalInt
from uppyyl_simulator.backend.data_structures.types.scalar import UppaalScalar
from uppyyl_simulator.backend.data_structures.types.struct import UppaalStruct
from uppyyl_simulator.backend.data_structures.types.void import UppaalVoid
from uppyyl_simulator.backend.helper.helper import prepend_to_lines
from uppyyl_simulator.backend.models.ta.ta import (
    Location
)

base_classes = {
    "void": UppaalVoid,
    "int": UppaalInt,
    "bool": UppaalBool,
    "Uppaal_bounded_int": UppaalBoundedInt,
    "scalar": UppaalScalar,
    "struct": UppaalStruct,
    "Uppaal_array": UppaalArray,
    "clock": UppaalClock,
    "chan": UppaalChan,
}

pp = pprint.PrettyPrinter(indent=4, compact=True)


###########################
# Instance Scope Accessor #
###########################
class InstanceScopeAccessor(collections.abc.MutableMapping):
    """An accessor for instance scopes (allows accessing scopes like variables, e.g. Inst.x)."""

    def __init__(self, inst_name, system_state):
        """Initialize InstanceScopeAccessor.

        Args:
            inst_name: The name of the instance.
            system_state: The system state.
        """
        self.inst_name = inst_name
        self.system_state = system_state

    def __setitem__(self, key, value):
        raise Exception("Cannot set value via instance scope accessor.")

    def __getitem__(self, key):
        constants_scope = self.system_state.program_state["constant"]["instances"][self.inst_name]
        variable_scope = self.system_state.program_state["variable"]["instances"][self.inst_name]
        if key in constants_scope:
            return constants_scope[key]
        elif key in variable_scope:
            return variable_scope[key]
        else:
            tmpl_name = self.system_state.instance_data[self.inst_name]
            tmpl = self.system_state.system.get_template_by_name(tmpl_name)
            active_loc = self.system_state.location_state[self.inst_name]
            for loc in tmpl.locations.values():
                if key == loc.name:
                    if loc == active_loc:
                        return UppaalBool(True)
                    else:
                        return UppaalBool(False)

        raise Exception(f'Variable "{key}" not found in scope of instance "{self.inst_name}".')

    def __delitem__(self, key):
        constants_scope = self.system_state.program_state["constant"]["instances"][self.inst_name]
        variable_scope = self.system_state.program_state["variable"]["instances"][self.inst_name]
        if key in constants_scope:
            del constants_scope[key]
        elif key in variable_scope:
            del variable_scope[key]
        else:
            raise Exception(f'Variable "{key}" cannot be remove from scope of instance "{self.inst_name}".')

    def __iter__(self):
        constants_scope = self.system_state.program_state["constant"]["instances"][self.inst_name]
        variable_scope = self.system_state.program_state["variable"]["instances"][self.inst_name]
        return itertools.chain(iter(constants_scope), iter(variable_scope))

    def __len__(self):
        constants_scope = self.system_state.program_state["constant"]["instances"][self.inst_name]
        variable_scope = self.system_state.program_state["variable"]["instances"][self.inst_name]
        return len(constants_scope) + len(variable_scope)

    def copy(self):
        """Copies the InstanceScopeAccessor instance.

        Returns:
            The copied InstanceScopeAccessor instance.
        """
        copy_obj = InstanceScopeAccessor(inst_name=self.inst_name, system_state=self.system_state)
        return copy_obj

    def __str__(self):
        name_str = f'"{self.inst_name}"' if self.inst_name else f''
        return f'InstanceScopeAccessor(name={name_str})'


###########################
# Multi Instance Accessor #
###########################
class MultiInstanceAccessor:
    """A (callable) accessor for multiple instances created via parameterized template.

    Required to allows expressions of the form "Inst(1).x" for a "system Inst;" where Inst is instantiated multiple
    times based on bounded integer template parameters.
    """

    def __init__(self, tmpl_name, param_count=0):
        """Initializes MultiInstanceAccessor.

        Args:
            tmpl_name: The name of the template.
            param_count: The number of template parameters.
        """
        self.tmpl_name = tmpl_name
        self.param_count = param_count

    def __call__(self, args, state):
        assert len(args) == self.param_count
        if self.param_count == 0:
            inst_id = f'{self.tmpl_name}'
        else:
            inst_id = f'{self.tmpl_name}({",".join(map(lambda arg: str(int(arg)), args))})'
        scope_accessor = InstanceScopeAccessor(inst_name=inst_id, system_state=state)
        return scope_accessor

    def copy(self):
        """Copies the MultiInstanceAccessor instance.

        Returns:
            The copied MultiInstanceAccessor instance.
        """
        copy_obj = MultiInstanceAccessor(tmpl_name=self.tmpl_name, param_count=self.param_count)
        return copy_obj

    def __str__(self):
        name_str = f'"{self.tmpl_name}"' if self.tmpl_name else f''
        return f'MultiInstanceAccessor(name={name_str})'


################
# System State #
################
class SystemState:
    """A representation of the complete system state, including location state, program state, and clock state."""

    def __init__(self):
        """Initializes SystemState."""
        self.system = None
        self.program_state = {
            "constant": {
                "system": {},
                "instances": {},
            },
            "variable": {
                "system": {},
                "instances": {},
            },
            "local": []
        }
        self.location_state: Dict[str, Location] = {}
        self.dbm_state = None

        self.instance_data = {}
        self.instance_scope_accessors = {}
        self.active_instance_name = None  # The active instance scope is searched first before the system scope

        # While active, the "get" function treats instance scopes as accessible variables
        # (e.g., allows "Inst.var" to access variable "var" of instance "Inst")
        self.access_instance_scopes = False

    def activate_system_scope(self, access_instance_scopes=False):
        """Activates the system scope, so that new variables are defined on system level.

        Args:
            access_instance_scopes: Choose whether instances should be accessible like variables.
        """
        self.active_instance_name = None
        self.access_instance_scopes = access_instance_scopes

    def activate_instance_scope(self, inst_name):
        """Activates an instance scope, so that new variables are defined on instance level.

        Args:
            inst_name: The name of the instance.
        """
        if (inst_name in self.program_state["constant"]["instances"] and
                inst_name in self.program_state["variable"]["instances"]):
            self.active_instance_name = inst_name
            self.access_instance_scopes = False  # Disable access to other instances from within an instance
        else:
            raise Exception(f'Cannot activate scope of instance {inst_name} in SystemState.')

    def assign(self, key, val):
        """Assigns a new value to an existing variable.

        Args:
            key: The variable name.
            val: The new variable value.
        """
        var = self.get(key)
        if isinstance(val, UppaalVariable):
            val = val.val
        var.assign(val)

    def define(self, key, clazz, const=False):
        """Defines a new variable of a given type (i.e., class) in the currently active scope.

        Args:
            key: The variable name.
            clazz: The variable type.
            const: Choose whether the variable should belong to constant or variable state.
        """
        scope_name, scope, scope_path = self.get_active_scope(const)
        var = UppaalVariable(name=key, val=clazz())
        scope[key] = var
        if hasattr(var, "update_path"):
            var.update_path(scope_path=scope_path, var_path=[key])

    def add(self, key, var, const=False):
        """Adds a given variable to the currently active scope.

        Args:
            key: The variable name.
            var: The variable.
            const: Choose whether the variable should belong to constant or variable state.
        """
        scope_name, scope, scope_path = self.get_active_scope(const)
        if key in scope:
            raise Exception(f'Key "{key}" already exists in current scope "{scope_name}" of SystemState.')
        scope[key] = var
        if hasattr(var, "update_path"):
            var.update_path(scope_path=scope_path, var_path=[key])

    def set(self, key, var, const=False):
        """Sets a (potentially existing) variable.

        Args:
            key: The variable name.
            var: The variable.
            const: Choose whether the variable should belong to constant or variable state.
        """
        scope_name, scope, scope_path = self.get_active_scope(const)
        scope[key] = var
        if hasattr(var, "update_path"):
            var.update_path(scope_path=scope_path, var_path=[key])

    def get(self, key):
        """Provides the value of a given variable name.

        The function first checks the local scopes, then the instance scopes, followed by potential references to
        instance scopes as variables (e.g., Inst.x), and finally the global scope.

        Args:
            key: The variable name.

        Returns:
            The variable value.
        """
        for i in range(len(self.program_state["local"]) - 1, -1, -1):
            local_scope_name, local_scope = self.program_state["local"][i]
            if key in local_scope:
                return local_scope[key]
        if self.active_instance_name is not None:
            const_instance_scope = self.program_state["constant"]["instances"][self.active_instance_name]
            if key in const_instance_scope:
                return const_instance_scope[key]
            var_instance_scope = self.program_state["variable"]["instances"][self.active_instance_name]
            if key in var_instance_scope:
                return var_instance_scope[key]
        if self.access_instance_scopes and (key in self.instance_scope_accessors):
            return self.instance_scope_accessors[key]
        if key in self.program_state["constant"]["system"]:
            return self.program_state["constant"]["system"][key]
        if key in self.program_state["variable"]["system"]:
            return self.program_state["variable"]["system"][key]
        if key in base_classes:
            return base_classes[key]

        raise Exception(f'Key "{key}" not found in SystemState.')

    def get_active_scope(self, const=False):
        """Gets the currently active scope.

        Args:
            const: Choose whether a constant or variable scope is looked for.

        Returns:
            The active scope.
        """
        if len(self.program_state["local"]) > 0:
            scope_index = len(self.program_state["local"])-1
            scope_name, scope = self.program_state["local"][scope_index]
            scope_path = ["variable", "instances", scope_index]
            return scope_name, scope, scope_path
        elif self.active_instance_name is not None:
            if const:
                active_instance_scope = self.program_state["constant"]["instances"][self.active_instance_name]
                scope_path = ["constant", "instances", self.active_instance_name]
            else:
                active_instance_scope = self.program_state["variable"]["instances"][self.active_instance_name]
                scope_path = ["variable", "instances", self.active_instance_name]
            return self.active_instance_name, active_instance_scope, scope_path
        else:
            if const:
                global_scope = self.program_state["constant"]["system"]
                scope_path = ["constant", "system"]
            else:
                global_scope = self.program_state["variable"]["system"]
                scope_path = ["variable", "system"]
            return "__GLOBAL__", global_scope, scope_path

    def new_instance_scope(self, inst_name=None):
        """Creates a new instance scope of a given instance name.

        Args:
            inst_name: The instance name.
        """
        if (inst_name in self.program_state["constant"]["instances"] or
                inst_name in self.program_state["variable"]["instances"]):
            raise Exception(f'Scope for instance "{inst_name}" already exists in SystemState.')
        self.program_state["constant"]["instances"][inst_name] = {}
        self.program_state["variable"]["instances"][inst_name] = {}

    def add_local_scope(self, name, scope):
        """Add a given scope to the local scope stack.

        Args:
            name: The local scope name.
            scope: The new scope.

        Returns:
            The new scope.
        """
        self.program_state["local"].append((name, scope))
        return scope

    def new_local_scope(self, name=None):
        """Creates a new local scope of a given name.

        Args:
            name: The local scope name.

        Returns:
            The new local scope.
        """
        new_scope = {}
        self.add_local_scope(name=name, scope=new_scope)
        return new_scope

    def remove_local_scope(self):
        """Removes the innermost local scope.

        Returns:
            The removed scope.
        """
        try:
            scope = self.program_state["local"].pop()
        except IndexError:
            raise IndexError("No local scope to remove exists.")
        return scope

    def pretty_string(self):
        """Provides a pretty string representation of the current state.

        Returns:
            The string representation of the current state.
        """
        string = ""
        string += f'--------------------\n'
        string += f'--- System State ---\n'
        string += f'--------------------\n'

        body_string = ""
        body_string += f'============== System Scope [Const] ==============\n\n'
        for key, var in self.program_state["constant"]["system"].items():
            body_string += f'{key} = {var}\n'
        body_string += "\n"

        body_string += f'============== Instance Scopes [Const] ==============\n\n'
        for scope_name, scope in self.program_state["constant"]["instances"].items():
            active_str = f'[active] ' if self.active_instance_name == scope_name else f''
            body_string += f'== Instance Scope "{scope_name}" {active_str}==\n'
            for key, var in scope.items():
                body_string += f'{key} = {var}\n'
            body_string += "\n"

        body_string += f'============== System Scope [Variable] ==============\n\n'
        for key, var in self.program_state["variable"]["system"].items():
            body_string += f'{key} = {var}\n'
        body_string += "\n"

        body_string += f'============== Instance Scopes [Variable] ==============\n\n'
        for scope_name, scope in self.program_state["variable"]["instances"].items():
            active_str = f'[active] ' if self.active_instance_name == scope_name else f''
            body_string += f'== Instance Scope "{scope_name}" {active_str}==\n'
            for key, var in scope.items():
                body_string += f'{key} = {var}\n'
            body_string += "\n"

        body_string += f'============== Instance Accessors ==============\n\n'
        for key, var in self.instance_scope_accessors.items():
            body_string += f'{var}\n'
        body_string += "\n"

        body_string += f'============== Local Scopes ==============\n\n'
        for i, (scope_name, scope) in enumerate(self.program_state["local"]):
            scope_name_str = f'["{scope_name}"]' if scope_name else f''
            body_string += f'== Local Scope {i} {scope_name_str}==\n'
            for key, var in scope.items():
                body_string += f'{key} = {var}\n'
            body_string += "\n"

        body_string = prepend_to_lines(body_string, "| ")
        string += body_string

        return string

    def _get_array_clock_names(self, array_val, clock_names):
        """Recursively gets all clock names from an array."""
        for val in array_val.data:
            if isinstance(val, UppaalArray):
                self._get_array_clock_names(val, clock_names)
            elif isinstance(val, UppaalClock):
                clock_names.append(val.name)

    def get_clock_names(self):
        """Gets the names of all clocks contained in the system state.

        Returns:
            A list of all clock names.
        """
        clock_names = []

        relevant_scopes = [self.program_state["constant"]["system"], self.program_state["variable"]["system"]]
        relevant_scopes.extend(self.program_state["constant"]["instances"].values())
        relevant_scopes.extend(self.program_state["variable"]["instances"].values())

        for scope in relevant_scopes:
            for key, var in scope.items():
                if isinstance(var, UppaalVariable):
                    val = var.val
                    if isinstance(val, UppaalClock):
                        clock_names.append(var.name)
                    elif isinstance(val, UppaalArray):
                        self._get_array_clock_names(val, clock_names)

        return clock_names

    ###

    def _init_program_state_from_system(self, system):
        """Initializes the program state from a system instance.

        Args:
            system: The system instance.
        """
        c_evaluator = UppaalCEvaluator(do_log_details=False)

        # Evaluate global declaration
        global_decl_ast = system.declaration.ast
        c_evaluator.eval_ast(global_decl_ast, self)

        # Evaluate variable declarations in system declaration
        system_decl_ast = system.system_declaration.ast
        system_data = c_evaluator.eval_ast(system_decl_ast, self)

        self.instance_data = {}
        for inst_group in system_data["system_instances"]:
            for inst_name in inst_group:
                if inst_name in system_data["instance_data"]:  # If process was instantiated in system declaration
                    inst_data = system_data["instance_data"][inst_name]
                    tmpl_name = inst_data["template_name"]
                    tmpl = system.get_template_by_name(tmpl_name)

                    self.new_instance_scope(inst_name)
                    self.activate_instance_scope(inst_name)

                    inst_arg_asts = inst_data["args"]
                    inst_args = list(map(lambda arg_ast: c_evaluator.eval_ast(arg_ast, self), inst_arg_asts))
                    tmpl_param_asts = list(map(lambda p: p.ast, tmpl.parameters))
                    c_evaluator.initialize_parameters(param_asts=tmpl_param_asts, args=inst_args, state=self)

                    template_decl_ast = tmpl.declaration.ast
                    if template_decl_ast is not None:
                        c_evaluator.eval_ast(template_decl_ast, self)

                    instance_accessor = InstanceScopeAccessor(inst_name=inst_name, system_state=self)
                    self.instance_scope_accessors[inst_name] = instance_accessor

                    self.instance_data[inst_name] = tmpl_name

                else:  # If process/instance is instantiated via ranged parameters (using "system Tmpl;")
                    tmpl_name = inst_name
                    try:
                        tmpl = system.get_template_by_name(tmpl_name)
                    except Exception:
                        raise Exception(f'Instance "{inst_name}" is part of system, but was not defined.')

                    if len(tmpl.parameters) == 0:  # If no parameters exist, add single instance scope
                        self.new_instance_scope(inst_name)
                        self.activate_instance_scope(inst_name)

                        tmpl_param_asts = list(map(lambda p: p.ast, tmpl.parameters))
                        c_evaluator.initialize_parameters(param_asts=tmpl_param_asts, args=[], state=self)

                        template_decl_ast = tmpl.declaration.ast
                        if template_decl_ast is not None:
                            c_evaluator.eval_ast(template_decl_ast, self)

                        instance_accessor = InstanceScopeAccessor(inst_name=inst_name, system_state=self)
                        self.instance_scope_accessors[inst_name] = instance_accessor

                        self.instance_data[inst_name] = tmpl_name

                    else:  # Otherwise add instance scope for all combinations of ranged integer / scalar parameters
                        param_clazzes = []
                        for param in tmpl.parameters:
                            prefixes, param_clazz = c_evaluator.eval_ast(param.ast["type"], self)
                            param_clazzes.append(param_clazz)

                        value_combinations_iter = itertools.product(*param_clazzes)

                        # Create instances based on ranged integers / scalars
                        for value_combination in value_combinations_iter:
                            sub_inst_name_part = f'({",".join(map(str, value_combination))})'
                            sub_inst_name = f'{inst_name}{sub_inst_name_part}'

                            self.new_instance_scope(sub_inst_name)
                            self.activate_instance_scope(sub_inst_name)

                            tmpl_param_asts = list(map(lambda p: p.ast, tmpl.parameters))
                            inst_arg_asts = list(map(lambda arg_val: {"val": arg_val, "astType": "Integer"},
                                                     value_combination))
                            inst_args = list(map(lambda arg_ast: c_evaluator.eval_ast(arg_ast, self), inst_arg_asts))
                            c_evaluator.initialize_parameters(param_asts=tmpl_param_asts, args=inst_args,
                                                              state=self)

                            # TODO: Optimize, as this part is equal for all instances of template
                            template_decl_ast = tmpl.declaration.ast
                            if template_decl_ast is not None:
                                c_evaluator.eval_ast(template_decl_ast, self)

                            self.instance_data[sub_inst_name] = tmpl_name

                        instance_accessor = MultiInstanceAccessor(tmpl_name=inst_name,
                                                                  param_count=len(param_clazzes))
                        self.instance_scope_accessors[inst_name] = instance_accessor

    def _init_dbm_state(self):
        """Initializes the DBM state."""
        clock_names = self.get_clock_names()
        self.dbm_state = DBM(clocks=clock_names, zero_init=True)

    def _init_location_state_from_system(self, system):
        """Initializes the location state from a system instance."""
        self.location_state = {}
        for inst_name, tmpl_name in self.instance_data.items():
            self.location_state[inst_name] = system.get_template_by_name(tmpl_name).init_loc

    def init_from_system(self, system):
        """Initializes the system state from a system instance.

        Args:
            system: The TA system.
        """
        self.system = system
        self._init_program_state_from_system(system)
        self._init_dbm_state()
        self._init_location_state_from_system(system)

    def get_variable_state_string(self):
        """Gets a short string representation of the variable part of the program state.

        Returns:
            The variable program state string.
        """
        var_strs = []
        for key, var in self.program_state["variable"]["system"].items():
            if not isinstance(var.val, UppaalReference):
                var_strs.append(f'{key}={var.val}')
        for inst_name, inst_scope in self.program_state["variable"]["instances"].items():
            for key, var in inst_scope.items():
                if not isinstance(var.val, UppaalReference):
                    var_strs.append(f'{inst_name}.{key}={var.val}')
        string = ", ".join(var_strs)
        return string

    def get_compact_variable_state(self):
        """Gets a compact representation dict of the variable part of the program state.

        Returns:
            The compact variable program state dict.
        """
        compact_state = {
            "variable": {
                "system": {},
                "instances": {}
            }
        }

        for key, var in self.program_state["variable"]["system"].items():
            compact_val = var.val.get_raw_data()
            compact_state["variable"]["system"][key] = compact_val
        for inst_scope_name, inst_scope in self.program_state["variable"]["instances"].items():
            compact_state["variable"]["instances"][inst_scope_name] = {}
            for key, var in inst_scope.items():
                compact_val = var.val.get_raw_data()
                compact_state["variable"]["instances"][inst_scope_name][key] = compact_val

        return compact_state

    def assign_from_compact_variable_state(self, compact_var_state):  # TODO: Test and revise
        """Assigns the variable part of the program state from a compact data dict.

        Args:
            compact_var_state: The compact variable program state dict.
        """
        for other_key, other_val in compact_var_state["variable"]["system"].items():
            self_var = self.program_state["variable"]["system"][other_key]
            self_var.val = self_var.clazz(init=other_val)
        for other_inst_scope_name, other_inst_scope in compact_var_state["variable"]["instances"].items():
            self_inst_scope = self.program_state["variable"]["instances"][other_inst_scope_name]
            for key, val in other_inst_scope.items():
                var = self_inst_scope[key]
                var.val = var.clazz(init=val)

    def _copy_program_state(self):
        # Shallow copy constant part
        program_state_copy = {
            "constant": self.program_state["constant"],
            "variable": {
                "system": {},
                "instances": {},
            },
            "local": []
        }

        # Copy system scope
        for section in ["variable"]:  # ["constant", "variable"]
            for key, orig_var in self.program_state[section]["system"].items():
                copy_var = orig_var.copy()
                if isinstance(orig_var.val, UppaalReference):  # Set the correct (new) pointee for a reference
                    copy_var.val.init_pointee(program_state_copy)
                program_state_copy[section]["system"][key] = copy_var

        # Copy instance scopes
        for section in ["variable"]:  # ["constant", "variable"]
            for inst_scope_name, inst_scope in self.program_state[section]["instances"].items():
                program_state_copy[section]["instances"][inst_scope_name] = {}
                for key, orig_var in inst_scope.items():
                    copy_var = orig_var.copy()
                    if isinstance(orig_var.val, UppaalReference):  # Set the correct (new) pointee for a reference
                        copy_var.val.init_pointee(program_state_copy)
                    program_state_copy[section]["instances"][inst_scope_name][key] = copy_var

        # Copy local scopes
        for local_scope_name, local_scope in self.program_state["local"]:
            copy_local_scope = {}
            for key, orig_var in local_scope.items():
                copy_var = orig_var.copy()
                if isinstance(orig_var.val, UppaalReference):  # Set the correct (new) pointee for a reference
                    copy_var.val.init_pointee(program_state_copy)
                copy_local_scope[key] = copy_var
            program_state_copy["local"].append(copy_local_scope)

        return program_state_copy

    def copy(self):
        """Copies the SystemState instance.

        Returns:
            The copied SystemState instance.
        """
        copy_obj = SystemState()

        # Copy state data
        copy_obj.program_state = self._copy_program_state()
        copy_obj.location_state = copy.copy(self.location_state)
        copy_obj.dbm_state = self.dbm_state.copy()

        return copy_obj

    def __str__(self):
        string = ""
        string += self.pretty_string()

        return string
