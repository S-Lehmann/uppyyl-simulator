"""This module implements modifiers for Uppaal NTA systems."""

import copy

from uppyyl_simulator.backend.data_structures.ast.ast_code_element import (
    apply_func_to_ast
)


##################
# SystemModifier #
##################
from uppyyl_simulator.backend.data_structures.types.bool import UppaalBool
from uppyyl_simulator.backend.data_structures.types.int import UppaalInt
from uppyyl_simulator.backend.models.ta.ta_modifier import TemplateModifier


class SystemModifier:
    """This class provides the modifiers for Uppaal NTA systems."""

    def __init__(self):
        """Initializes SystemModifier."""
        pass

    @staticmethod
    def move_sys_vars_to_global_decl(system):
        """Moves all variable declarations in the system declaration section to the global declaration.

        Args:
            system: The system object.

        Returns:
            None
        """

        system_decl_stmts = system.system_declaration.ast["decls"]
        global_decl_stmts = system.declaration.ast["decls"]
        i = 0
        while i < len(system_decl_stmts):
            system_stmt = system_decl_stmts[i]
            if (system_stmt["astType"] == "VariableDecls" or system_stmt["astType"] == "TypeDecls"
                    or system_stmt["astType"] == "Function"):
                global_decl_stmts.append(system_stmt)
                del system_decl_stmts[i]
                continue
            i += 1
        system.declaration.update_text()
        system.system_declaration.update_text()

    @staticmethod
    def convert_instances_to_templates(system, instance_data, keep_original_templates=True):
        """Generate a template for each automata instance (optionally keep original templates).

        Args:
            system: The system object
            instance_data: The template and argument data of all instances
            keep_original_templates: Defines whether the original templates should be kept or not

        Returns:

        """
        # Remove original instantiations from system declaration AST
        system_decl_stmts = system.system_declaration.ast["decls"]
        i = 0
        while i < len(system_decl_stmts):
            system_stmt = system_decl_stmts[i]
            if system_stmt["astType"] == 'Instantiation':
                del system_decl_stmts[i]
                continue
            i += 1
        # instance_asts = list(filter(lambda decl: decl["astType"] == 'Instantiation', system_decl_stmts))
        # print(instance_asts)

        # Create templates based on instance data
        old_instance_templates = {}
        new_instance_templates = {}
        for inst_name, inst_data in instance_data.items():
            tmpl_name = inst_data["template_name"]
            args = inst_data["args"]
            ref_tmpl = system.get_template_by_name(tmpl_name)
            # inst_name = instance_ast["instanceName"]
            # tmpl_name = instance_ast["templateName"]
            old_instance_templates[inst_name] = ref_tmpl

            new_tmpl_name = f'{inst_name}_Tmpl'
            new_tmpl = system.new_template(new_tmpl_name)
            new_tmpl.assign_from(ref_tmpl)
            system.templates[new_tmpl.id] = new_tmpl

            new_instance_templates[inst_name] = new_tmpl

            # Convert all variables defined in the local declaration to global ones
            SystemModifier.convert_local_vars_to_global_vars(system=system, tmpl=new_tmpl)

            # Replace all template argument variables with their respective input variables
            arg_names = list(map(lambda param: param.ast["varData"]["varName"], new_tmpl.parameters))
            var_replacements = list(zip(arg_names, args))

            def model_var_adapt_func(var_replacements_):
                """Helper function for name adaption."""

                def ast_func(ast, _acc):
                    """Helper function for name adaption."""
                    for arg_name, rep_val in var_replacements_:
                        if ast["astType"] == 'Variable' and ast["name"] == arg_name:
                            if isinstance(rep_val, str):
                                ast = {"astType": 'Variable', "name": rep_val}
                            elif isinstance(rep_val, UppaalInt):
                                ast = {"astType": 'Integer', "val": rep_val}
                            elif isinstance(rep_val, UppaalBool):
                                ast = {"astType": 'Boolean', "val": rep_val}
                            break
                    return ast

                return ast_func

            adaptions = [model_var_adapt_func(var_replacements_=var_replacements)]

            TemplateModifier.adapt_asts(tmpl=new_tmpl, adaptions=adaptions)

            # Remove all template arguments
            new_tmpl.parameters = []

            # # Remove all inputs for template arguments
            # instance_ast["args"] = []

        # Add all templates as instances ot system declaration
        for inst_name, tmpl in new_instance_templates.items():
            instantiation_ast = {
                "astType": 'Instantiation',
                "instanceName": inst_name,
                "params": [],
                "templateName": tmpl.name,
                "args": []
            }
            system_decl_stmts.append(instantiation_ast)

        # # Adapt system declaration to instantiate from new templates
        # for i in range(0, len(instance_asts)):
        #     instance_ast = instance_asts[i]
        #     instance_ast["templateName"] = f'{instance_ast["instanceName"]}_Tmpl'

        SystemModifier.move_sys_vars_to_global_decl(system=system)
        system.declaration.update_text()
        system.system_declaration.update_text()

        if not keep_original_templates:
            old_tmpls = set(old_instance_templates.values())
            for old_tmpl in old_tmpls:
                del system.templates[old_tmpl.id]

    @staticmethod
    def convert_local_vars_to_global_vars(system, tmpl):
        """Convert all local template variables to global ones (requires at most one instance per template).

        Args:
            system: The system object
            tmpl: The template from which all variables should be moved to the global declaration

        Returns:
            None
        """
        if isinstance(tmpl, str):
            tmpl = system.get_template(tmpl)

        # Extract variable declarations from local declaration text
        local_var_names = []
        local_type_names = []
        local_func_names = []
        stmts = tmpl.declaration.ast["decls"]
        for i in range(0, len(stmts)):
            stmt = stmts[i]
            if stmt["astType"] == "VariableDecls":
                for single_var_id in stmt["varData"]:
                    local_var_names.append(single_var_id["varName"])
            elif stmt["astType"] == "Function":
                local_func_names.append(stmt["name"])
            elif stmt["astType"] == "TypeDecls":
                for type_name_id in stmt["names"]:
                    local_type_names.append(type_name_id["varName"])

        # Copy local ast
        new_global_ast_part = copy.deepcopy(tmpl.declaration.ast)

        # Replace all locally defined variables, types and functions with their global counterparts
        for i in range(0, len(local_var_names)):
            def local_var_adapt_func(ast, _acc):
                """Helper function for variable name adaption."""
                if ast["astType"] == 'VariableID' and ast["varName"] == local_var_names[i]:
                    ast["varName"] = f'{tmpl.name}_{local_var_names[i]}'
                return ast

            new_global_ast_part, _ = apply_func_to_ast(ast=new_global_ast_part, func=local_var_adapt_func)

        for i in range(0, len(local_func_names)):
            def local_func_adapt_func(ast, _acc):
                """Helper function for function name adaption."""
                if ast["astType"] == 'FuncDef' and ast["name"] == local_func_names[i]:
                    ast["varName"] = f'{tmpl.name}_{local_func_names[i]}'
                return ast

            new_global_ast_part, _ = apply_func_to_ast(ast=new_global_ast_part, func=local_func_adapt_func)

        for i in range(0, len(local_type_names)):
            def local_type_adapt_func(ast, _acc):
                """Helper function for type name adaption."""
                if ast["astType"] == 'CustomType' and ast["type"] == local_type_names[i]:
                    ast["type"] = f'{tmpl.name}_{local_type_names[i]}'
                return ast

            new_global_ast_part, _ = apply_func_to_ast(ast=new_global_ast_part, func=local_type_adapt_func)

        # Insert new global AST part into global declaration ast
        new_stmts = new_global_ast_part["decls"]
        for new_stmt in new_stmts:
            system.declaration.ast["decls"].append(new_stmt)

        # Update variables inside model
        var_replacements = []
        for i in range(0, len(local_var_names)):
            def model_var_adapt_func(old_name, new_name):
                """Helper function for name adaption."""

                def ast_func(ast, _acc):
                    """Helper function for name adaption."""
                    if ast["astType"] == 'Variable' and ast["name"] == old_name:
                        ast["name"] = new_name
                    return ast

                return ast_func

            old_name_ = local_var_names[i]
            new_name_ = f'{tmpl.name}_{old_name_}'

            var_replacements.append(model_var_adapt_func(old_name=old_name_, new_name=new_name_))

        TemplateModifier.adapt_asts(tmpl=tmpl, adaptions=var_replacements)

        # Clear local declaration
        tmpl.set_declaration("")

        system.declaration.update_text()
