"""An automaton implementation."""

from uppyyl_simulator.backend.helper.helper import (
    unique_id
)
from uppyyl_simulator.backend.models.base.declaration import (
    Declaration
)
from uppyyl_simulator.backend.models.graph import graph
from uppyyl_simulator.backend.models.graph.graph import Graph, Node


#############
# Automaton #
#############
class Automaton(Graph):
    """An automaton class."""

    def __init__(self, name, id_=None):
        """Initializes Automaton.

        Args:
            name: The automaton name.
            id_: The unique automaton ID ("atmt-...").
        """
        super().__init__(name, id_ if id_ else unique_id("atmt"))
        self.declaration = None
        self.init_loc = None

    @property
    def locations(self):
        """A property for locations to rename base "nodes" attribute to "locations".

        Returns:
            The nodes attribute.
        """
        return self.nodes

    @locations.setter
    def locations(self, value):
        """A property setter for locations (as alias for "nodes").

        Args:
            value: The new nodes value.

        Returns:
            None
        """
        self.nodes = value

    def set_declaration(self, decl):
        """Sets the state declaration of the automaton.

        Args:
            decl: The declaration code (or object).

        Returns:
            The declaration object.
        """
        if isinstance(decl, str):
            decl = Declaration(decl)
        self.declaration = decl
        return decl

    def add_location(self, loc):
        """Adds an existing location object to the automaton.

        Args:
            loc: The location object.

        Returns:
            The added location object.
        """
        return super().add_node(node=loc)

    def new_node(self, name, id_=None):
        """Creates a new node object and adds it to the graph.

        Args:
            name: The node name.
            id_: An optionally custom node id.

        Returns:
            The new node object.
        """
        return self.new_location(name, id_)

    def new_location(self, name, id_=None):
        """Creates a new location object and adds it to the automaton.

        Args:
            name: The location name.
            id_: An optionally custom location id.

        Returns:
            The new location object.
        """
        loc = Location(name, self, id_)
        self.add_location(loc)
        return loc

    def get_location_by_name(self, name):
        """Gets a location object by a given name.

        Args:
            name: The location name.

        Returns:
            The location object.
        """
        try:
            return super().get_node_by_name(name)
        except Exception:
            raise Exception(f'Location "{name}" not found in automaton "{self.name}".')

    def get_location_by_id(self, id_):
        """Gets a location object by a given id.

        Args:
            id_: The location id.

        Returns:
            The location object.
        """
        try:
            return super().get_node_by_id(id_)
        except Exception:
            raise Exception(f'Location with id "{id_}" not found in automaton "{self.name}".')

    def get_location_by_index(self, index):
        """Gets a location object by a given index.

        Args:
            index: The location index.

        Returns:
            The location object.
        """
        try:
            return super().get_node_by_index(index)
        except Exception:
            raise Exception(f'Location with index "{index}" not found in automaton "{self.name}".')

    def add_edge(self, edge):
        """Adds an existing edge object to the automaton.

        Args:
            edge: The edge object.

        Returns:
            The added edge object.
        """
        self.edges[edge.id] = edge
        return edge

    def new_edge(self, source, target, id_=None):
        """Creates a new edge object based of location objects and adds it to the automaton.

        Args:
            source: The source location of the edge.
            target: The target location of the edge.
            id_: An optionally custom edge id.

        Returns:
            The new edge object.
        """
        edge = Edge(source, target, self, id_)
        self.add_edge(edge)
        return edge

    def new_edge_by_loc_names(self, source_name, target_name, id_=None):
        """Creates a new edge object based on ids and adds it to the automaton.

        Args:
            source_name: The source location name.
            target_name: The target location name.
            id_: An optionally custom edge id.

        Returns:
            The new edge object.
        """
        return super().new_edge_by_node_names(source_name, target_name, id_)

    def new_edge_by_loc_ids(self, source_id, target_id, id_=None):
        """Creates a new edge object based on ids and adds it to the automaton.

        Args:
            source_id: The source location id.
            target_id: The target location id.
            id_: An optionally custom edge id.

        Returns:
            The new edge object.
        """
        return super().new_edge_by_node_ids(source_id, target_id, id_)

    def set_init_location_by_id(self, loc_id):
        """Sets the initial automaton location to the location with the given id.

        Args:
            loc_id: The location id.

        Returns:
            The initial location object.
        """
        loc = self.locations[loc_id]
        self.set_init_location(loc)
        return loc

    def set_init_location_by_name(self, loc_name):
        """Sets the initial automaton location to the location with the given name.

        Args:
            loc_name: The location name.

        Returns:
            The initial location object.
        """
        loc = self.get_location_by_name(loc_name)
        self.set_init_location(loc)
        return loc

    def set_init_location(self, loc):
        """Sets the initial automaton location to the given location.

        Args:
            loc: The location object.

        Returns:
            The initial location object.
        """
        self.init_loc = loc
        return loc

    def assign_from(self, other, assign_ids=False):
        """Assigns the automaton attributes (e.g., locations, edges) from another automaton.

        Args:
            other: The other automaton.
            assign_ids: Choose whether the IDs should be copied, too, or generated anew.
        """
        assoc_data = super().assign_from(other=other, assign_ids=assign_ids)

        if other.declaration:
            self.set_declaration(other.declaration.copy())

        if other.init_loc:
            self.set_init_location(self.locations[assoc_data["loc_id_assocs"][other.init_loc.id]])

    def copy(self):
        """Copies the Automaton instance.

        Returns:
            The copied Automaton instance.
        """
        copy_autom = Automaton(self.name, self.id)
        copy_autom.assign_from(self, True)
        return copy_autom

    def __str__(self):
        obj_str = ""

        obj_str += f'Name: {self.name}\n'
        obj_str += f'ID: {self.id}\n'

        obj_str += "\nLocations:\n"
        for loc_ID in self.locations:
            obj_str += "--------\n"
            obj_str += str(self.locations[loc_ID])

        obj_str += "\nEdges:\n"
        for edge_ID in self.edges:
            obj_str += "--------\n"
            obj_str += str(self.edges[edge_ID])

        obj_str += "\n"
        obj_str += f'Declaration: {f"{chr(10)}{self.declaration}" if self.declaration else "None"}\n'
        obj_str += f'Init Location: {self.init_loc.name if self.init_loc else "None"}\n'

        return obj_str


############
# Location #
############
class Location(Node):
    """An automaton location class."""

    def __init__(self, name=None, parent=None, id_=None):
        """Initializes Location.

        Args:
            name: The location name.
            parent: The parent automaton object.
            id_: The unique location ID ("loc-...").
        """
        super().__init__(name=name, parent=parent, id_=id_ if id_ else unique_id("loc"))

    def assign_from(self, other, assign_ids=False):
        """Assigns the attributes of the location from another location.

        Args:
            other: The other location.
            assign_ids: Choose whether the IDs should be copied, too, or generated anew.
        """
        self.name = other.name

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
class Edge(graph.Edge):
    """An automaton edge class."""

    def __init__(self, source, target, parent=None, id_=None):
        """Initializes Edge.

        Args:
            source: The source location object.
            target: The target location object.
            parent: The parent automaton object.
            id_: The unique edge ID ("edge-...").
        """
        super().__init__(source=source, target=target, parent=parent, id_=id_)
