"""This module implements a Uppaal system transition."""

from uppyyl_simulator.backend.data_structures.dbm.dbm_operations.dbm_operations import DBMOperationSequence
from uppyyl_simulator.backend.data_structures.state.system_state import SystemState


class Transition:
    """A transition between two system states."""

    def __init__(self, source_state, triggered_edges, target_state, edge_scopes=None, urgent=False, committed=False):
        """Initializes Transition."""
        self.source_state: SystemState = source_state
        self.triggered_edges = triggered_edges
        self.target_state: SystemState = target_state
        self.edge_scopes = edge_scopes if edge_scopes else {}
        self.urgent = urgent
        self.committed = committed
        self.dbm_op_sequence = DBMOperationSequence()

    def short_string(self):
        """Generates a short string representation of the transition.

        Returns:
            The short string representation of the transition.
        """
        string = ""
        if self.triggered_edges:
            involved_instances = map(lambda kv: kv[0], filter(lambda kv: kv[1] is not None,
                                                              self.triggered_edges.items()))
            string += f'({", ".join(involved_instances)})'
        else:
            string += f'()'
        return string

    def __str__(self):
        string = ""
        string += f'== Active source locations: ==\n'
        if self.source_state is None:
            string += f'None'
        else:
            source_loc_strs = []
            for inst_name, loc in self.source_state.location_state.items():
                source_loc_strs.append(f'"{inst_name}": "{loc.name}"')
            string += ", ".join(source_loc_strs)
        string += f'\n'

        string += f'== Triggered edges: ==\n'
        if self.triggered_edges is None:
            string += f'None'
        else:
            edge_strs = []
            for inst_name, edge in self.triggered_edges.items():
                if edge is None:
                    edge_strs.append(f'"{inst_name}": None')
                else:
                    edge_strs.append(f'"{inst_name}": "{edge.source.name}" -> "{edge.target.name}"')
            string += ", ".join(edge_strs)
        string += f'\n'

        string += f'== Active target locations: ==\n'
        if self.target_state is None:
            string += f'None'
        else:
            target_loc_strs = []
            for inst_name, loc in self.target_state.location_state.items():
                target_loc_strs.append(f'"{inst_name}": "{loc.name}"')
            string += ", ".join(target_loc_strs)
        string += f'\n'

        return string
