"""A graph implementation."""

from collections import OrderedDict

from uppyyl_simulator.backend.helper.helper import (
    unique_id
)


#########
# Graph #
#########
class Graph:
    """A graph class."""

    def __init__(self, name=None, id_=None):
        """Initializes Graph.

        Args:
            name: The graph name.
            id_: The unique graph ID ("graph-...").
        """
        self.id = id_ if id_ else unique_id("graph")
        self.name = name if name else self.id.replace("-", "_")
        self.nodes = OrderedDict()
        self.edges = OrderedDict()

    def add_node(self, node):
        """Adds an existing node object to the graph.

        Args:
            node: The node object.

        Returns:
            The added node object.
        """
        self.nodes[node.id] = node
        return node

    def new_node(self, name, id_=None):
        """Creates a new node object and adds it to the graph.

        Args:
            name: The node name.
            id_: An optionally custom node id.

        Returns:
            The new node object.
        """
        node = Node(name, self, id_)
        self.add_node(node)
        return node

    def get_node_by_name(self, name):
        """Gets a node object by a given name.

        Args:
            name: The node name.

        Returns:
            The node object.
        """
        for node_id in self.nodes:
            node = self.nodes[node_id]
            if name == node.name:
                return node
        raise Exception(f'Node "{name}" not found in graph.')

    def get_node_by_id(self, id_):
        """Gets a node object by a given id.

        Args:
            id_: The node id.

        Returns:
            The node object.
        """
        if id_ in self.nodes:
            return self.nodes[id_]
        raise Exception(f'Node with id "{id_}" not found in graph.')

    def get_node_by_index(self, index):
        """Gets a node object by a given index.

        Args:
            index: The node index.

        Returns:
            The node object.
        """
        nodes = list(self.nodes.values())
        if len(nodes) >= index + 1:
            return nodes[index]
        raise Exception(f'Node with index "{index}" not found in graph "{self.name}".')

    def add_edge(self, edge):
        """Adds an existing edge object to the graph.

        Args:
            edge: The edge object.

        Returns:
            The added edge object.
        """
        self.edges[edge.id] = edge
        return edge

    def new_edge(self, source, target, id_=None):
        """Creates a new edge object based of node objects and adds it to the graph.

        Args:
            source: The source node of the edge.
            target: The target node of the edge.
            id_: An optionally custom edge id.

        Returns:
            The new edge object.
        """
        edge = Edge(source, target, self, id_)
        self.add_edge(edge)
        return edge

    def new_edge_by_node_names(self, source_name, target_name, id_=None):
        """Creates a new edge object based of node objects and adds it to the graph.

        Args:
            source_name: The source node name.
            target_name: The target node name.
            id_: An optionally custom edge id.

        Returns:
            The new edge object.
        """
        source_node = self.get_node_by_name(source_name)
        target_node = self.get_node_by_name(target_name)
        edge = self.new_edge(source_node, target_node, id_)
        return edge

    def new_edge_by_node_ids(self, source_id, target_id, id_=None):
        """Creates a new edge object based on ids and adds it to the graph.

        Args:
            source_id: The source node id.
            target_id: The target node id.
            id_: An optionally custom edge id.

        Returns:
            The new edge object.
        """
        source_node = self.get_node_by_id(source_id)
        target_node = self.get_node_by_id(target_id)
        edge = self.new_edge(source_node, target_node, id_)
        return edge

    def get_edge_by_name(self, name):
        """Gets an edge object by a given name.

        Args:
            name: The edge name.

        Returns:
            The edge object.
        """
        for edge_id in self.edges:
            edge = self.edges[edge_id]
            if name == edge.name:
                return edge
        raise Exception(f'Edge with name "{name}" not found in graph.')

    def get_edge_by_id(self, id_):
        """Gets an edge object by a given id.

        Args:
            id_: The edge id.

        Returns:
            The edge object.
        """
        if id_ in self.edges:
            return self.edges[id_]
        raise Exception(f'Edge with id "{id_}" not found in graph.')

    def get_edge_by_index(self, index):
        """Gets an edge object by a given index.

        Args:
            index: The edge index.

        Returns:
            The edge object.
        """
        edges = list(self.edges.values())
        if len(edges) >= index + 1:
            return edges[index]
        raise Exception(f'Edge with index "{index}" not found in graph "{self.name}".')

    def assign_from(self, other, assign_ids=False):
        """Assigns the graph attributes (e.g., nodes, edges) from another graph.

        Args:
            other: The other graph.
            assign_ids: Choose whether the IDs should be copied, too, or generated anew.
        """

        self.nodes = OrderedDict()
        node_id_assocs = {}
        for node_id in other.nodes:
            node = other.nodes[node_id]
            new_node = self.new_node(None, node.id if assign_ids else None)
            new_node.assign_from(node)

            self.nodes[new_node.id] = new_node
            node_id_assocs[node.id] = new_node.id

        self.edges = OrderedDict()
        edge_id_assocs = {}
        for edge_id in other.edges:
            edge = other.edges[edge_id]
            source_node = self.nodes[node_id_assocs[edge.source.id]]
            target_node = self.nodes[node_id_assocs[edge.target.id]]

            new_edge = self.new_edge(source_node, target_node, edge.id if assign_ids else None)
            new_edge.assign_from(edge)

            self.edges[new_edge.id] = new_edge
            edge_id_assocs[edge.id] = new_edge.id

        return {"node_id_assocs": node_id_assocs, "edge_id_assocs": edge_id_assocs}

    def copy(self):
        """Copies the Graph instance.

        Returns:
            The copied Graph instance.
        """
        copy_obj = Graph(self.name, self.id)
        copy_obj.assign_from(self, True)
        return copy_obj

    def __str__(self):
        obj_str = ""

        obj_str += f'Name: {self.name}\n'
        obj_str += f'ID: {self.id}\n'

        obj_str += "\nNodes:\n"
        for node_ID in self.nodes:
            obj_str += "--------\n"
            obj_str += str(self.nodes[node_ID])

        obj_str += "\nEdges:\n"
        for edge_ID in self.edges:
            obj_str += "--------\n"
            obj_str += str(self.edges[edge_ID])

        return obj_str


########
# Node #
########
class Node:
    """An graph node class."""

    def __init__(self, name=None, parent=None, id_=None):
        """Initializes Node.

        Args:
            name: The node name.
            parent: The parent graph object.
            id_: The unique node ID ("node-...").
        """
        self.id = id_ if id_ else unique_id("node")
        self.name = name if name else ""  # id.replace("-", "_");
        self.in_edges = OrderedDict()
        self.out_edges = OrderedDict()
        self.parent = parent

        self.view = {}

    def assign_from(self, other, assign_ids=False):
        """Assigns the attributes of the node from another node.

        Args:
            other: The other node.
            assign_ids: Choose whether the IDs should be copied, too, or generated anew.
        """
        self.name = other.name
        if assign_ids:
            self.id = other.id

    def __str__(self):
        obj_str = ""
        obj_str += f'Name: {self.name}\n'
        obj_str += f'ID: {self.id}\n'

        in_edge_names = list(map(lambda e: e.get_name(), self.in_edges.values()))
        obj_str += f'InEdges: {in_edge_names}\n'

        out_edge_names = list(map(lambda e: e.get_name(), self.out_edges.values()))
        obj_str += f'OutEdges: {out_edge_names}\n'

        return obj_str


########
# Edge #
########
class Edge:
    """An graph edge class."""

    def __init__(self, source, target, parent=None, id_=None):
        """Initializes Edge.

        Args:
            source: The source node object.
            target: The target node object.
            parent: The parent graph object.
            id_: The unique edge ID ("edge-...").
        """
        if source is None:
            raise Exception(f'Edge source "{source}" not defined.')
        if target is None:
            raise Exception(f'Edge target "{target}" not defined.')

        self.id = id_ if id_ else unique_id("edge")
        self.parent = parent

        self.source = None
        self.target = None
        self.set_source_node(source)
        self.set_target_node(target)

        self.view = {}

    def get_name(self):
        """Gets the name of the edge (of the form "source_name -> target_name").

        Returns:
            The edge name.
        """
        if self.source.name == "":
            source_name = self.source.id
        else:
            source_name = self.source.name

        if self.source.name == "":
            target_name = self.target.id
        else:
            target_name = self.target.name

        return f'{source_name}->{target_name}'

    # Source node #
    def set_source_node(self, node):
        """Sets the source node to a given node object.

        Args:
            node: The source node object.

        Returns:
            The source node object.
        """
        if self.source:
            del self.source.out_edges[self.id]

        self.source = node
        self.source.out_edges[self.id] = self
        return node

    def set_source_node_by_name(self, node_name):
        """Sets the source node to a node obtained via a node name.

        Args:
            node_name: The source node name.

        Returns:
            The source node object.
        """
        node = self.parent.get_node_by_name(node_name)
        self.set_source_node(node)
        return node

    def set_source_node_by_id(self, node_id):
        """Sets the source node to a node obtained via a node id.

        Args:
            node_id: The source node id.

        Returns:
            The source node object.
        """
        node = self.parent.get_node_by_id(node_id)
        self.set_source_node(node)
        return node

    # Target node #
    def set_target_node(self, node):
        """Sets the target node to a given node object.

        Args:
            node: The target node object.

        Returns:
            The target node object.
        """
        if self.target:
            del self.target.in_edges[self.id]

        self.target = node
        self.target.in_edges[self.id] = self
        return node

    def set_target_node_by_name(self, node_name):
        """Sets the target node to a node obtained via a node name.

        Args:
            node_name: The target node name.

        Returns:
            The target node object.
        """
        node = self.parent.get_node_by_name(node_name)
        self.set_target_node(node)
        return node

    def set_target_node_by_id(self, node_id):
        """Sets the target node to a node obtained via a node id.

        Args:
            node_id: The target node id.

        Returns:
            The target node object.
        """
        node = self.parent.get_node_by_id(node_id)
        self.set_target_node(node)
        return node

    def assign_from(self, other, assign_ids=False):
        """Assigns the attributes of the edge from another edge.

        Args:
            other: The other edge.
            assign_ids: Choose whether the IDs should be copied, too, or generated anew.
        """
        pass

    def __str__(self):
        obj_str = ""
        obj_str += f'ID: {self.id}\n'
        obj_str += f'Source: {self.source.name}\n'
        obj_str += f'Target: {self.target.name}\n'

        return obj_str
