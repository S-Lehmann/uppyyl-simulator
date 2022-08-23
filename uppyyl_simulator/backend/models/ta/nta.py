"""A Uppaal automaton network implementation."""

from collections import OrderedDict

import uppyyl_simulator.backend.models.base.automaton_network as automaton_network
import uppyyl_simulator.backend.models.ta.ta as ta
from uppyyl_simulator.backend.models.ta.system_declaration import SystemDeclaration

is_global_dbm = True


##########
# System #
##########
class System(automaton_network.System):
    """An Uppaal automaton network / system class."""

    def __init__(self):
        """Initializes System."""
        super().__init__()

        self.templates = OrderedDict()
        self.automata = OrderedDict()
        self.system_declaration = None

    def set_system_declaration(self, decl):
        """Sets the system declaration.

        Args:
            decl: The system declaration code string (or object)

        Returns:
            The system declaration object.
        """

        if isinstance(decl, str):
            decl = SystemDeclaration(decl)
        self.system_declaration = decl
        return decl

    def add_template(self, tmpl):
        """Adds a given template object to the system.

        Args:
            tmpl: The template object.

        Returns:
            The template object.
        """
        self.templates[tmpl.id] = tmpl
        return tmpl

    def new_template(self, name, id_=None):
        """Creates a new template object and adds it to the system.

        Args:
            name: The location name.
            id_: An optionally custom template id.

        Returns:
            The new template object.
        """
        tmpl = ta.Template(name, id_)
        self.add_template(tmpl)
        return tmpl

    def get_template_by_name(self, name):
        """Gets an template object by a given name.

        Args:
            name: The template name.

        Returns:
            The template object.
        """
        for tmpl_ID in self.templates:
            tmpl = self.templates[tmpl_ID]
            if name == tmpl.name:
                return tmpl

        raise Exception(f'Template "{name}" not found in system.')

    def get_template_by_id(self, id_):
        """Gets an template object by a given id.

        Args:
            id_: The template name.

        Returns:
            The template object.
        """
        if id_ in self.templates:
            return self.templates[id_]
        raise Exception(f'Template with id "{id_}" not found in system.')

    def get_template_by_index(self, index):
        """Gets an template object by a given index.

        Args:
            index: The template index.

        Returns:
            The template object.
        """
        tmpls = list(self.templates.values())
        if len(tmpls) >= index + 1:
            return tmpls[index]
        raise Exception(f'Template with index "{index}" not found in system.')

    def __str__(self):
        obj_str = super().__str__()
        obj_str += "System declaration: " + (
            ("\n" + str(self.system_declaration)) if self.system_declaration else "None") + "\n"

        obj_str += "Templates:\n"
        for tmpl_ID in self.templates:
            obj_str += "---------------------------\n"
            obj_str += str(self.templates[tmpl_ID])
            obj_str += "---------------------------\n"

        return obj_str
