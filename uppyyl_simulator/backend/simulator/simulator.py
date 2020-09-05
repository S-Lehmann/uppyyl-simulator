"""An implementation of a simulator for Uppaal model systems."""

import copy
import itertools
import random
from collections import OrderedDict

from uppyyl_simulator.backend.ast.parsers.generated.uppaal_c_language_parser import (
    UppaalCLanguageParser
)

from uppyyl_simulator.backend.ast.evaluators.uppaal_c_evaluator import (
    UppaalCEvaluator
)
from uppyyl_simulator.backend.ast.parsers.uppaal_c_language_semantics import (
    UppaalCLanguageSemantics
)
from uppyyl_simulator.backend.ast.parsers.uppaal_xml_model_parser import (
    uppaal_xml_to_system
)
from uppyyl_simulator.backend.data_structures.dbm.dbm_operations.dbm_operations import DBMOperationSequence, \
    DBMOperationGenerator
from uppyyl_simulator.backend.data_structures.state.system_state import (
    SystemState
)
from uppyyl_simulator.backend.data_structures.state.variable import UppaalVariable
from uppyyl_simulator.backend.data_structures.types.chan import UppaalChan
from uppyyl_simulator.backend.models.ta.transition import Transition

dbm_op_gen = DBMOperationGenerator()


class Error(Exception):
    """Base class for exceptions."""
    pass


class TransitionError(Error):
    """Exception raised for transition errors due to non-valid target states.

    Attributes:
        message -- explanation of the error
    """


def product_dict(src_dict: OrderedDict):
    """Calculates the cartesian product of a dictionary of lists.

    Args:
        src_dict: The source dictionary.
    """
    keys = src_dict.keys()
    vals = src_dict.values()
    for combination in itertools.product(*vals):
        yield dict(zip(keys, combination))


relation_from_ast_op = {
    "LessEqual": "<=",
    "LessThan": "<",
    "Equal": "==",
    "NotEqual": "!=",
    "GreaterEqual": ">=",
    "GreaterThan": ">",
}


def adapt_dbm_constraint_ast(dbm_constr_ast):
    """Transforms the expression ast of a constraint into a clock constraint ast.

    Args:
        dbm_constr_ast: The constraint expression ast.

    Returns:
        The clock constraint ast.
    """
    if (dbm_constr_ast["expr"]["left"]["astType"] == "BinaryExpr"
            and dbm_constr_ast["expr"]["left"]["op"] == 'Sub'):
        # Constraint: t1 - t2 (<|<=|>=|>) c
        clock1 = dbm_constr_ast["expr"]["left"]["left"]
        clock2 = dbm_constr_ast["expr"]["left"]["right"]
    else:
        # if (dbm_constr_ast["expr"]["left"]["astType"] == "UnaryExpr"
        #         and dbm_constr_ast["expr"]["left"]["op"] == "Minus"):
        #     # Constraint: -t2 (<|<=|>=|>) c  # Note: Cannot occur, as not supported by Uppaal
        #     clock1 = None
        #     clock2 = dbm_constr_ast["expr"]["left"]["expr"]
        # else:

        # Constraint: t1 (<|<=|>=|>) c
        clock1 = dbm_constr_ast["expr"]["left"]
        clock2 = None
    rel = dbm_constr_ast["expr"]["op"]
    val = dbm_constr_ast["expr"]["right"]
    return {"clock1": clock1, "clock2": clock2, "rel": rel, "val": val, "astType": "ClockConstraint"}


def adapt_dbm_reset_ast(dbm_reset_ast):
    """Transforms the expression ast of a reset into a clock reset ast.

    Args:
        dbm_reset_ast: The reset expression ast.

    Returns:
        The clock reset ast.
    """
    clock = dbm_reset_ast["expr"]["left"]
    val = dbm_reset_ast["expr"]["right"]
    return {"clock": clock, "val": val, "astType": "ClockReset"}


#############
# Simulator #
#############
class Simulator:
    """A simulator for Uppaal model systems."""

    def __init__(self):
        """Initializes UppaalSimulator."""
        self.init_system_state = None
        self.system_state = None
        self.transitions = None
        self.recent_transition = None

        self.transition_trace = []
        self.dbm_op_sequence = DBMOperationSequence()
        self.transition_counts = {
            "potential": None,
            "enabled": None,
            "valid": None
        }

        self.system = None

        self.c_language_parser = UppaalCLanguageParser(semantics=UppaalCLanguageSemantics())
        self.c_evaluator = UppaalCEvaluator(do_log_details=False)

    def load_system(self, system_path):
        """Loads a system at a given path into the simulator.

        Args:
            system_path: The system path.
        """
        with open(system_path) as file:
            system_xml_str = file.read()
        self.set_system(system_xml_str)

    def set_system(self, system):
        """Sets the system of the simulator.

        Args:
            system: The system as string or system object.
        """
        if isinstance(system, str):
            system = uppaal_xml_to_system(system)
        self.system = system
        self.init_system_state = self.generate_init_system_state()
        self.init_simulator()

    def generate_init_system_state(self):
        """Generates the initial system state defined by the declaration and system declaration.

        Returns:
            The generated system state.
        """
        system_state = SystemState()

        # Init const and variable state
        system_state.init_from_system(self.system)
        system_state.activate_system_scope(access_instance_scopes=True)

        return system_state

    def init_simulator(self):
        """Initializes the simulator."""
        self.transition_trace = []
        self.dbm_op_sequence = DBMOperationSequence()

        init_state = self.init_system_state.copy()
        initial_transition = Transition(source_state=None, triggered_edges=None, target_state=init_state)
        loc_res = self._evaluate_locations(initial_transition.target_state)
        initial_transition.dbm_op_sequence.extend(loc_res["dbm_op_seq"])
        self.execute_transition(initial_transition)

    def get_sequence(self):
        """Gets the sequence of applied DBM operations.

        Returns:
            The DBM operation sequence.
        """
        return self.dbm_op_sequence

    def set_current_state(self, state):
        """Sets the current simulator state.

        Args:
            state: The new state.
        """
        self.system_state = state

    @staticmethod
    def _get_transition_type_from_source_locs(source_locs):
        urgent = False
        committed = False
        for loc in source_locs:
            urgent = urgent or loc.urgent
            committed = committed or loc.committed
        return urgent, committed

    def _get_all_potential_transitions(self, state):
        # Get all possible outgoing edges classified by synchronization type
        all_out_edges = {}
        for inst_name, loc in state.location_state.items():
            state.activate_instance_scope(inst_name)
            no_sync_edges = []
            caller_edges = {}
            listener_edges = {}
            for _, edge in loc.out_edges.items():
                select_val_combinations = self._get_select_val_combinations(edge=edge, state=state)
                for select_val_comb in select_val_combinations:
                    edge_scope = {k: UppaalVariable(name=k, val=v) for k, v in select_val_comb.items()}
                    state.add_local_scope(name='edge', scope=edge_scope)
                    if edge.sync is None:
                        no_sync_edges.append((edge_scope, edge))
                    else:
                        chan_obj: UppaalChan = self.c_evaluator.eval_ast(edge.sync.ast["channel"], state).val
                        if edge.sync.ast["op"] == '!':
                            if chan_obj not in caller_edges:
                                caller_edges[chan_obj] = []
                            caller_edges[chan_obj].append((edge_scope, edge))
                        else:
                            if chan_obj not in listener_edges:
                                listener_edges[chan_obj] = []
                            listener_edges[chan_obj].append((edge_scope, edge))

                    state.remove_local_scope()

            all_out_edges[inst_name] = {
                "no_sync": no_sync_edges,
                "caller": caller_edges,
                "listener": listener_edges
            }

        # Get all potential transitions (target states do not need to be known at this point)
        all_pot_trans = []
        inst_names = state.location_state.keys()
        for i, (inst_name, inst_edges) in enumerate(all_out_edges.items()):
            for edge_data in inst_edges["no_sync"]:  # Get non-synced transitions
                triggered_edges_data = dict.fromkeys(inst_names, (None, None))
                triggered_edges_data[inst_name] = edge_data
                edge_scopes = {k: v[0] for (k, v) in triggered_edges_data.items()}
                triggered_edges = {k: v[1] for (k, v) in triggered_edges_data.items()}

                source_locs_of_involved_edges = map(lambda e: e.source, filter(lambda e: e is not None,
                                                                               triggered_edges.values()))
                loc_urgent, loc_committed = self._get_transition_type_from_source_locs(
                    source_locs_of_involved_edges)
                trans = Transition(source_state=state,
                                   triggered_edges=triggered_edges,
                                   target_state=None,
                                   urgent=loc_urgent,
                                   committed=loc_committed,
                                   edge_scopes=edge_scopes)
                all_pot_trans.append(trans)
            for chan_obj, caller_edges in inst_edges["caller"].items():

                if chan_obj.broadcast:
                    # Get broadcast-sync transitions
                    broadcast_listeners = OrderedDict()
                    for j, (other_inst_name, other_inst_edges) in enumerate(all_out_edges.items()):
                        if i == j:  # Skip listener edges of caller instance
                            broadcast_listeners[other_inst_name] = [(None, None)]
                        else:
                            listener_edges = other_inst_edges["listener"].get(chan_obj, [])
                            broadcast_listeners[other_inst_name] = listener_edges
                    broadcast_listener_combinations = product_dict(broadcast_listeners)
                    for broadcast_listener_combination in broadcast_listener_combinations:
                        for caller_edge_data in caller_edges:
                            triggered_edges_data = copy.copy(broadcast_listener_combination)
                            triggered_edges_data[inst_name] = caller_edge_data
                            edge_scopes = {k: v[0] for (k, v) in triggered_edges_data.items()}
                            triggered_edges = {k: v[1] for (k, v) in triggered_edges_data.items()}

                            source_locs_of_involved_edges = map(lambda e: e.source, filter(lambda e: e is not None,
                                                                                           triggered_edges.values()))
                            loc_urgent, loc_committed = self._get_transition_type_from_source_locs(
                                source_locs_of_involved_edges)
                            trans = Transition(source_state=state,
                                               triggered_edges=triggered_edges,
                                               target_state=None,
                                               urgent=chan_obj.urgent or loc_urgent,
                                               committed=loc_committed,
                                               edge_scopes=edge_scopes)
                            all_pot_trans.append(trans)

                else:
                    # Get binary-sync transitions
                    for caller_edge_data in caller_edges:
                        for j, (other_inst_name, other_inst_edges) in enumerate(all_out_edges.items()):
                            listener_edges = other_inst_edges["listener"].get(chan_obj)
                            if i == j or listener_edges is None:  # Skip insts of caller and without listeners on chan
                                continue
                            for listener_edge_data in listener_edges:
                                triggered_edges_data = dict.fromkeys(inst_names, (None, None))
                                triggered_edges_data[inst_name] = caller_edge_data
                                triggered_edges_data[other_inst_name] = listener_edge_data
                                edge_scopes = {k: v[0] for (k, v) in triggered_edges_data.items()}
                                triggered_edges = {k: v[1] for (k, v) in triggered_edges_data.items()}

                                source_locs_of_involved_edges = map(
                                    lambda e: e.source, filter(lambda e: e is not None, triggered_edges.values()))
                                loc_urgent, loc_committed = self._get_transition_type_from_source_locs(
                                    source_locs_of_involved_edges)
                                trans = Transition(source_state=state,
                                                   triggered_edges=triggered_edges,
                                                   target_state=None,
                                                   urgent=chan_obj.urgent or loc_urgent,
                                                   committed=loc_committed,
                                                   edge_scopes=edge_scopes)
                                all_pot_trans.append(trans)

        # Filter out non-committed transitions if committed current locations exist
        source_locs = state.location_state.values()
        has_committed_locs = any(loc.committed for loc in source_locs)
        if has_committed_locs:
            all_committed_trans = list(filter(lambda trans_: trans_.committed, all_pot_trans))
            all_pot_trans = all_committed_trans if all_committed_trans else all_pot_trans

        # print(f'Potential transitions: {len(all_pot_trans)}')
        return all_pot_trans

    def _get_select_val_combinations(self, edge, state):
        select_val_iterators = OrderedDict()
        for select in edge.selects:
            select_var_name = select.ast["name"]
            _, select_var_type = self.c_evaluator.eval_ast(ast=select.ast["type"], state=state)
            key = select_var_name
            select_val_iterators[key] = select_var_type
        select_val_combinations = product_dict(select_val_iterators)
        return select_val_combinations

    def _get_all_enabled_transitions(self, state, all_pot_trans=None):
        if all_pot_trans is None:
            all_pot_trans = self._get_all_potential_transitions(state=state)
        enabled_transitions = []
        for trans in all_pot_trans:
            # Init target state from source state
            trans.target_state = trans.source_state.copy()
            # Update target locations from triggered edges
            for inst_name, edge in trans.triggered_edges.items():
                if edge is None:
                    continue
                trans.target_state.location_state[inst_name] = edge.target

            grd_res = self._evaluate_guards(transition=trans)
            trans.dbm_op_sequence.extend(grd_res["dbm_op_seq"])
            if not trans.target_state.dbm_state.is_empty() and grd_res["var_guard_res"]:
                enabled_transitions.append(trans)
        return enabled_transitions

    def _get_all_valid_transitions(self, state, all_enabled_trans=None):
        if all_enabled_trans is None:
            all_enabled_trans = self._get_all_enabled_transitions(state=state, all_pot_trans=None)
        valid_transitions = []
        for trans in all_enabled_trans:
            reset_res = self._evaluate_resets(transition=trans)
            trans.dbm_op_sequence.extend(reset_res["dbm_op_seq"])
            loc_res = self._evaluate_locations(state=trans.target_state)
            trans.dbm_op_sequence.extend(loc_res["dbm_op_seq"])
            if not trans.target_state.dbm_state.is_empty():
                valid_transitions.append(trans)
        return valid_transitions

    def _evaluate_guards(self, transition: Transition):
        dbm_op_seq = DBMOperationSequence()
        state = transition.target_state

        # Get guard operations
        grd_operations = []
        var_guard_res = True
        for inst_name, edge in transition.triggered_edges.items():
            if edge is None:
                continue
            state.activate_instance_scope(inst_name)
            has_edge_scope = inst_name in transition.edge_scopes
            if has_edge_scope:
                state.add_local_scope(name="edge", scope=transition.edge_scopes[inst_name])
            for guard in edge.clock_guards:
                # if isinstance(guard, ClockGuard):
                # TODO: Remove distinguishing clock and variables guards in separate lists, as it affects the order

                constr_operation = self._make_constraint_operation_from_ast(constr_ast=guard.ast, state=state)
                grd_operations.append(constr_operation)
            for guard in edge.variable_guards:
                ret = self.c_evaluator.eval_ast(ast=guard.ast["expr"], state=state)
                var_guard_res = var_guard_res and ret
            if has_edge_scope:
                state.remove_local_scope()

        # Apply guards
        dbm_op_seq.extend(grd_operations)
        for guard in grd_operations:
            guard.apply(state.dbm_state)

        # Close DBM if any guards were applied
        if len(grd_operations) > 0:
            close_operation = dbm_op_gen.generate_close()
            dbm_op_seq.append(close_operation)
            close_operation.apply(state.dbm_state)

        return {"dbm_op_seq": dbm_op_seq, "var_guard_res": var_guard_res}

    def _evaluate_resets(self, transition: Transition):
        dbm_op_seq = DBMOperationSequence()
        state = transition.target_state

        # Execute "reset" statements
        reset_operations = []
        for inst_name, edge in transition.triggered_edges.items():
            if edge is None:
                continue
            has_edge_scope = inst_name in transition.edge_scopes
            if has_edge_scope:
                state.add_local_scope(name="edge", scope=transition.edge_scopes[inst_name])
            state.activate_instance_scope(inst_name)
            for update in edge.updates:
                self.c_evaluator.eval_ast(ast=update.ast, state=state)
            for reset in edge.resets:
                reset_operation = self._make_reset_operation_from_ast(reset_ast=reset.ast, state=state)
                reset_operations.append(reset_operation)
            if has_edge_scope:
                state.remove_local_scope()

        # Apply resets
        dbm_op_seq.extend(reset_operations)
        for reset in reset_operations:
            # print(reset)
            reset.apply(state.dbm_state)

        return {"dbm_op_seq": dbm_op_seq}

    def _evaluate_locations(self, state):
        all_pot_trans = self._get_all_potential_transitions(state=state)
        all_urgent_or_committed_trans = list(filter(lambda trans: trans.urgent or trans.committed, all_pot_trans))
        dbm_op_seq = DBMOperationSequence()
        if len(all_urgent_or_committed_trans) == 0:
            df_operation = dbm_op_gen.generate_delay_future()
            df_operation.apply(state.dbm_state)
            dbm_op_seq.append(df_operation)

        inv_res = self._evaluate_invariants(state)
        dbm_op_seq.extend(inv_res["dbm_op_seq"])
        return {"dbm_op_seq": dbm_op_seq}

    def _evaluate_invariants(self, state):
        dbm_op_seq = DBMOperationSequence()

        # Get invariant operations
        inv_operations = []
        for inst_name, loc in state.location_state.items():
            state.activate_instance_scope(inst_name)
            for inv in loc.invariants:
                constr_operation = self._make_constraint_operation_from_ast(constr_ast=inv.ast, state=state)
                inv_operations.append(constr_operation)

        # Apply invariant operations
        dbm_op_seq.extend(inv_operations)
        for inv in inv_operations:
            # print(inv)
            inv.apply(state.dbm_state)

        # Close DBM if any invariants were applied
        if len(inv_operations) > 0:
            close_operation = dbm_op_gen.generate_close()
            dbm_op_seq.append(close_operation)
            close_operation.apply(state.dbm_state)

        return {"dbm_op_seq": dbm_op_seq}

    def get_transitions(self):
        """Gets all valid transitions for the current state.

        Returns:
            The list of valid transitions.
        """
        return self._get_all_valid_transitions(state=self.system_state)

    def _make_constraint_operation_from_ast(self, constr_ast, state):
        dbm_constr_ast = adapt_dbm_constraint_ast(constr_ast)

        # if dbm_constr_ast["clock1"] is not None:
        clock1 = self.c_evaluator.eval_ast(ast=dbm_constr_ast["clock1"], state=state)
        clock1_name = clock1.name
        # else:
        #     clock1_name = "T0_REF"  # Note: Cannot occur, as "-t2 (<|<=|>=|>) c" is not supported by Uppaal

        if dbm_constr_ast["clock2"] is not None:
            clock2 = self.c_evaluator.eval_ast(ast=dbm_constr_ast["clock2"], state=state)
            clock2_name = clock2.name
        else:
            clock2_name = "T0_REF"

        rel = relation_from_ast_op[dbm_constr_ast["rel"]]
        val = self.c_evaluator.eval_ast(dbm_constr_ast["val"], state)

        constr_operation = dbm_op_gen.generate_constraint(clock1=clock1_name, clock2=clock2_name, rel=rel, val=val)
        return constr_operation

    def _make_reset_operation_from_ast(self, reset_ast, state):
        dbm_reset_ast = adapt_dbm_reset_ast(reset_ast)
        clock = self.c_evaluator.eval_ast(ast=dbm_reset_ast["clock"], state=state)
        clock_name = clock.name
        val = self.c_evaluator.eval_ast(dbm_reset_ast["val"], state)

        reset_operation = dbm_op_gen.generate_reset(clock=clock_name, val=val)
        return reset_operation

    def execute_transition(self, transition):
        """Executes a given transition from the current state.

        Args:
            transition: The transition that is executed.
        """
        self.system_state = transition.target_state
        potential_transitions = self._get_all_potential_transitions(state=self.system_state)
        enabled_transitions = self._get_all_enabled_transitions(state=self.system_state,
                                                                all_pot_trans=potential_transitions)
        valid_transitions = self._get_all_valid_transitions(state=self.system_state,
                                                            all_enabled_trans=enabled_transitions)
        self.system_state.transitions = valid_transitions
        self.transition_counts = {
            "potential": len(potential_transitions),
            "enabled": len(enabled_transitions),
            "valid": len(valid_transitions)
        }
        self.transitions = valid_transitions

        self.transition_trace.append(transition)
        self.dbm_op_sequence.extend(transition.dbm_op_sequence)

    def simulate_step(self):
        """Performs a single random simulation step.

        Returns:
            The executed transition.
        """
        if not self.transitions:
            print(f'No transitions possible from current state.')
            return None

        random_transition_id = random.randint(0, len(self.transitions) - 1)
        transition = self.transitions[random_transition_id]
        self.execute_transition(transition)

        return transition

    def simulate(self, time_scope=None, max_steps=None):  # TODO: Add "T_GLOBAL" to system if it does not exist
        """Simulates the system up to a given time value of step count.

        Args:
            time_scope: The maximum time scope of the simulation.
            max_steps: The maximum number of simulation steps.
        """
        if time_scope is None and max_steps is None:
            raise TypeError(f'Either of parameters "time_scope" or "steps" need to be set.')
        global_time_interval = self.system_state.dbm_state.get_interval("T_GLOBAL")
        step = 0
        while ((time_scope is None or global_time_interval.lower.val <= time_scope) and
               (max_steps is None or step < max_steps)):
            self.simulate_step()
            global_time_interval = self.system_state.dbm_state.get_interval("T_GLOBAL")
            step += 1
            print(global_time_interval)

    def revert_to_state_by_index(self, idx):
        """Reverts the simulation to the state at given index.

        Args:
            idx: The targeted state index.
        """
        trans = self.transition_trace[idx]
        self.transition_trace = self.transition_trace[:idx + 1]
        self.system_state = trans.target_state
        valid_transitions = self._get_all_valid_transitions(state=self.system_state, all_enabled_trans=None)
        self.transitions = valid_transitions
