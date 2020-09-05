"""A weighted graph implementation."""

from uppyyl_simulator.backend.helper.helper import (
    unique_id
)

#################
# WeightedGraph #
#################
from uppyyl_simulator.backend.models.graph.graph import Graph, Edge


class WeightedGraph(Graph):
    """A weighted graph class."""

    def __init__(self, name=None, id_=None):
        """Initializes WeightedGraph.

        Args:
            name: The graph name.
            id_: The unique graph ID ("w-graph-...").
        """
        id_ = id_ if id_ else unique_id("w-graph")
        super().__init__(name, id_)

    def new_edge(self, source, target, id_=None, weight=0):
        """Creates a new edge object based of node objects and adds it to the graph.

        Args:
            source: The source node of the edge.
            target: The target node of the edge.
            id_: An optionally custom edge id.
            weight: The edge weight.

        Returns:
            The new edge object.
        """
        edge = WeightedEdge(source, target, self, id_, weight)
        self.add_edge(edge)
        return edge

    def new_edge_by_node_names(self, source_name, target_name, id_=None, weight=0):
        """Creates a new edge object based of node objects and adds it to the graph.

        Args:
            source_name: The source node name.
            target_name: The target node name.
            id_: An optionally custom edge id.
            weight: The edge weight.

        Returns:
            The new edge object.
        """
        source_node = self.get_node_by_name(source_name)
        target_node = self.get_node_by_name(target_name)
        edge = self.new_edge(source_node, target_node, id_, weight)
        return edge

    def new_edge_by_node_ids(self, source_id, target_id, id_=None, weight=0):
        """Creates a new edge object based on ids and adds it to the graph.

        Args:
            source_id: The source node id.
            target_id: The target node id.
            id_: An optionally custom edge id.
            weight: The edge weight.

        Returns:
            The new edge object.
        """
        source_node = self.get_node_by_id(source_id)
        target_node = self.get_node_by_id(target_id)
        edge = self.new_edge(source_node, target_node, id_, weight)
        return edge


################
# WeightedEdge #
################
class WeightedEdge(Edge):
    """An weighted graph edge class."""

    def __init__(self, source, target, parent=None, id_=None, weight=None):
        """Initializes WeightedEdge.

        Args:
            source: The source node object.
            target: The target node object.
            parent: The parent graph object.
            id_: The unique edge ID ("w-edge-...").
            weight: The edge weight.
        """
        id_ = id_ if id_ else unique_id("w-edge")
        super().__init__(source, target, parent, id_)

        self.weight = weight

    def set_weight(self, weight):
        """Sets the edge weight.

        Args:
            weight: The edge weight.
        """
        self.weight = weight

    def assign_from(self, other, assign_ids=False):
        """Assigns the attributes of the edge from another edge.

        Args:
            other: The other edge.
            assign_ids: Choose whether the IDs should be copied, too, or generated anew.
        """
        super().assign_from(other, assign_ids)
        self.weight = other.weight

    def __str__(self):
        obj_str = super().__str__()
        obj_str += f'Weight: {self.weight}\n'

        return obj_str
