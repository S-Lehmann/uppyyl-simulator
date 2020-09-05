"""An automaton network implementation."""

from collections import OrderedDict

from uppyyl_simulator.backend.models.base.declaration import (
    Declaration
)
from .automaton import Automaton
from .query import Query


##########
# System #
##########
class System:
    """An automaton network / system class."""
    
    def __init__(self):
        """Initializes System."""
        self.automata = OrderedDict()
        self.declaration = None
        self.queries = []
        self.backup_states = []
        self.trace = None

    def add_automaton(self, autom):
        """Adds a given automaton object to the system.

        Args:
            autom: The automaton object.

        Returns:
            The automaton object.
        """
        self.automata[autom.id] = autom
        return autom

    def new_automaton(self, name, id_):
        """Creates a new automaton object and adds it to the system.

        Args:
            name: The location name.
            id_: An optionally custom automaton id.

        Returns:
            The new automaton object.
        """
        autom = Automaton(name, id_)
        return self.add_automaton(autom)

    def get_automaton_by_name(self, name):
        """Gets an automaton object by a given name.

        Args:
            name: The automaton name.

        Returns:
            The automaton object.
        """
        for autom_ID in self.automata:
            autom = self.automata[autom_ID]
            if name == autom.name:
                return autom
        raise Exception(f'Automaton "{name}" not found in system.')

    def get_automaton_by_id(self, id_):
        """Gets an automaton object by a given id.

        Args:
            id_: The automaton name.

        Returns:
            The automaton object.
        """
        if id_ in self.automata:
            return self.automata[id_]
        raise Exception(f'Automaton with id "{id_}" not found in system.')

    def get_automaton_by_index(self, index):
        """Gets an automaton object by a given index.

        Args:
            index: The automaton index.

        Returns:
            The automaton object.
        """
        automs = list(self.automata.values())
        if len(automs) >= index + 1:
            return automs[index]
        raise Exception(f'Automaton with index "{index}" not found in system.')

    def set_declaration(self, decl):
        """Sets the declaration.

        Args:
            decl: A declaration string or object.

        Returns:
            The declaration object.
        """
        if isinstance(decl, str):
            decl = Declaration(decl)
        self.declaration = decl
        return decl

    def add_query(self, query):
        """Adds a query to the system.

        Args:
            query: The query object.
        """
        self.queries.append(query)

    def new_query(self, query_text, query_comment=None):
        """Creates a new query object and adds it to the system.

        Args:
            query_text: The query text.
            query_comment: An optionally query comment.

        Returns:
            The new query object.
        """
        query = Query(query_text, query_comment)
        self.add_query(query)

    def __str__(self):
        obj_str = ""
        obj_str += f'Global declaration: {f"{chr(10)}{self.declaration}" if self.declaration else "None"}\n'

        obj_str += "Automata:\n"
        for autom_ID in self.automata:
            obj_str += "---------------------------\n"
            obj_str += str(self.automata[autom_ID])
            obj_str += "---------------------------\n"

        return obj_str
