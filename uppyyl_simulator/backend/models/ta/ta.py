"""A Uppaal timed automaton (TA) implementation."""

from collections import OrderedDict

import uppyyl_simulator.backend.models.base.automaton as basic_automaton
from uppyyl_simulator.backend.helper.helper import (
    unique_id
)


############
# Template #
############
from uppyyl_simulator.backend.models.ta.labels.assignment import Update, Reset
from uppyyl_simulator.backend.models.ta.labels.guard import VariableGuard, ClockGuard
from uppyyl_simulator.backend.models.ta.labels.invariant import Invariant
from uppyyl_simulator.backend.models.ta.labels.parameter import Parameter
from uppyyl_simulator.backend.models.ta.labels.select import Select
from uppyyl_simulator.backend.models.ta.labels.sync import Synchronization


class Template(basic_automaton.Automaton):
    """A Uppaal model template class.

    It is used as a template to derive concrete automaton instances from.
    """

    def __init__(self, name, id_=None):
        """Initializes Template.

        Args:
            name: The template name.
            id_: The unique template ID ("tmpl-...").
        """
        super().__init__(name, id_ if id_ else unique_id("tmpl"))
        self.parameters = []

    def new_location(self, name=None, id_=None):
        """Creates a new location object and adds it to the template.

        Args:
            name: The location name.
            id_: An optionally custom location id.

        Returns:
            The new location object.
        """
        loc = Location(name, self, id_)
        return self.add_location(loc)

    def new_edge(self, source, target, id_=None):
        """Creates a new edge object based of location objects and adds it to the template.

        Args:
            source: The source location of the edge.
            target: The target location of the edge.
            id_: An optionally custom edge id.

        Returns:
            The new edge object.
        """
        edge = Edge(source, target, self, id_)
        return self.add_edge(edge)

    def add_parameter(self, param):
        """Adds a parameter to the template.

        Args:
            param: The parameter.

        Returns:
            The parameter list.
        """
        self.parameters.append(param)
        return param

    def new_parameter(self, param_data):
        """Creates a new parameter from a parameter string or AST dict.

        Args:
            param_data: The parameter string or AST dict.

        Returns:
            The parameter object.
        """
        param = Parameter(param_data)
        self.add_parameter(param)
        return param

    def assign_from(self, tmpl, assign_ids=False):
        """Assigns the template attributes (e.g., locations, edges) from another template.

        Args:
            tmpl: The other template.
            assign_ids: Choose whether the IDs should be copied, too, or generated anew.
        """
        super().assign_from(tmpl, assign_ids)
        self.parameters = tmpl.parameters.copy()

    def copy(self):
        """Copies the Template instance.

        Returns:
            The copied Template instance.
        """
        copy_tmpl = Template(self.name, self.id)
        copy_tmpl.assign_from(self, True)
        return copy_tmpl

    def __str__(self):
        obj_str = super().__str__()
        obj_str += f'Parameters: {self.parameters}\n'
        return obj_str


#############
# Automaton #
#############
# class Automaton(basic_automaton.Automaton):
#     """A Uppaal automaton class.
#
#     An automaton is derived from a model template.
#     """
#
#     def __init__(self, name, tmpl, args, id_=None):
#         """Initializes Automaton.
#
#         Args:
#             name: The automaton name.
#             tmpl: The corresponding template object.
#             args: The initial arguments for the instantiated automaton.
#             id_: The unique automaton ID ("atmt-...").
#         """
#         super().__init__(name, id_ if id_ else unique_id("atmt"))
#         self.tmpl = tmpl
#         self.args = args
#
#     def new_location(self, name=None, id_=None):
#         """Creates a new location object and adds it to the automaton.
#
#         Args:
#             name: The location name.
#             id_: An optionally custom location id.
#
#         Returns:
#             The new location object.
#         """
#         loc = Location(name, self, id_)
#         self.add_location(loc)
#         return loc
#
#     def new_edge(self, source, target, id_=None):
#         """Creates a new edge object based of location objects and adds it to the automaton.
#
#         Args:
#             source: The source location of the edge.
#             target: The target location of the edge.
#             id_: An optionally custom edge id.
#
#         Returns:
#             The new edge object.
#         """
#         edge = Edge(source, target, self, id_)
#         self.add_edge(edge)
#         return edge
#
#     def assign_from(self, autom, assign_ids=False):
#         """Assigns the automaton attributes (e.g., locations, edges) from another automaton.
#
#         Args:
#             autom: The other automaton.
#             assign_ids: Choose whether the IDs should be copied, too, or generated anew.
#         """
#         super().assign_from(autom, assign_ids)
#         self.tmpl = autom.tmpl
#         self.args = None
#
#     def copy(self):
#         """Copies the Automaton instance.
#
#         Returns:
#             The copied Automaton instance.
#         """
#         copy_autom = Automaton(self.name, None, None, self.id)
#         copy_autom.assign_from(self, True)
#         return copy_autom
#
#     def __str__(self):
#         obj_str = super().__str__()
#         return obj_str


############
# Location #
############
class Location(basic_automaton.Location):
    """An Uppaal automaton location class."""

    def __init__(self, name=None, parent=None, id_=None):
        """Initializes Location.

        Args:
            name: The location name.
            parent: The parent automaton object.
            id_: The unique location ID ("loc-...").
        """
        super().__init__(name, parent, id_ if id_ else unique_id("loc"))
        self.invariants = []
        self.urgent = False
        self.committed = False

        self.view = {"self": {"pos": {"x": 0, "y": 0}},
                     "name_label": {"pos": {"x": 20, "y": -20}, "id": unique_id("label")},
                     "invariant_label": {"pos": {"x": 20, "y": 20}, "id": unique_id("label")}}

    def set_whole_position(self, pos):
        """Sets the position of the locations and moves all its labels accordingly.

        Args:
            pos: The new location position.
        """
        shift = {"x": pos["x"] - self.view["self"]["pos"]["x"],
                 "y": pos["y"] - self.view["self"]["pos"]["y"]}
        self.view["self"]["pos"] = pos
        self.view["name_label"]["pos"] = {"x": self.view["name_label"]["pos"]["x"] + shift["x"],
                                          "y": self.view["name_label"]["pos"]["y"] + shift["y"]}
        self.view["invariant_label"]["pos"] = {"x": self.view["invariant_label"]["pos"]["x"] + shift["x"],
                                               "y": self.view["invariant_label"]["pos"]["y"] + shift["y"]}

    def set_urgent(self, status=True):
        """Sets the location to (non-)urgent.
        No time can pass all long as an urgent location is active.

        Args:
            status: The urgent status.
        """
        self.urgent = status
        if status:
            self.committed = False

    def set_committed(self, status=True):
        """Sets the location to (non-)committed.
        No time can pass all long as a committed location is active.
        Furthermore, the location needs to be left on the next transition.

        Args:
            status: The committed status.
        """
        self.committed = status
        if status:
            self.urgent = False

    def add_invariant(self, inv):
        """Adds an existing invariant object to the location.

        Args:
            inv: The invariant object.

        Returns:
            The invariant object.
        """
        self.invariants.append(inv)
        return inv

    def new_invariant(self, inv_data):
        """Creates a new invariant object and add it to the location.

        Args:
            inv_data: The invariant text or AST dict.

        Returns:
            The invariant object.
        """
        inv = Invariant(inv_data, self.parent)
        self.add_invariant(inv)
        return inv

    def assign_from(self, other, assign_ids=False, copy_view_data=True):
        """Assigns the attributes of the location from another location.

        Args:
            other: The other location.
            assign_ids: Choose whether the IDs should be copied, too, or generated anew.
            copy_view_data: Choose whether the graphical view data should be copied as well.
        """
        super().assign_from(other, assign_ids=assign_ids)
        self.invariants = map(lambda inv: inv.copy(), other.invariants)
        self.urgent = other.urgent
        self.committed = other.committed

        if copy_view_data:
            self.view = {}
            self.view["self"] = {
                "pos": {
                    "x": other.view["self"]["pos"]["x"],
                    "y": other.view["self"]["pos"]["y"]
                }
            }
            self.view["name_label"] = {
                "pos": {
                    "x": other.view["name_label"]["pos"]["x"],
                    "y": other.view["name_label"]["pos"]["y"]
                },
                "id": unique_id("label")
            }
            self.view["invariant_label"] = {
                "pos": {
                    "x": other.view["invariant_label"]["pos"]["x"],
                    "y": other.view["invariant_label"]["pos"]["y"]
                },
                "id": unique_id("label")
            }

    def __str__(self):
        obj_str = super().__str__()

        inv_strs = list(map(lambda v: f'"{v}"', self.invariants))
        obj_str += f'Invariants ({len(self.invariants)}): {", ".join(inv_strs)}\n'

        return obj_str


########
# Edge #
########
class Edge(basic_automaton.Edge):
    """An Uppaal automaton edge class."""
    """
    Create an instance of Edge.

    @constructor
    @param {Location | string} source - The source location object or name.
    @param {Location | string} target - The target location object or name.
    @param {Automaton} autom - The parent automaton object.
    @param {string} [id=unique_id("edge")] - The unique edge ID ("edge-...").
    @alias Edge
    @augments basic_automaton.Edge
    @inner
    """

    def __init__(self, source, target, parent=None, id_=None):
        """Initializes Edge.

        Args:
            source: The source location object.
            target: The target location object.
            parent: The parent automaton object.
            id_: The unique edge ID ("edge-...").
        """
        super().__init__(source, target, parent, id_ if id_ else unique_id("edge"))

        self.clock_guards = []
        self.variable_guards = []
        self.updates = []
        self.resets = []
        self.sync = None
        self.selects = []

        self.view = {"nails": OrderedDict()}

        center = {"x": int((self.source.view["self"]["pos"]["x"] + self.target.view["self"]["pos"]["x"]) / 2),
                  "y": int((self.source.view["self"]["pos"]["y"] + self.target.view["self"]["pos"]["y"]) / 2)}
        self.view["guard_label"] = {"pos": {"x": center["x"], "y": center["y"] - 20}, "id": unique_id("label")}
        self.view["update_label"] = {"pos": {"x": center["x"], "y": center["y"]}, "id": unique_id("label")}
        self.view["sync_label"] = {"pos": {"x": center["x"], "y": center["y"] + 20}, "id": unique_id("label")}
        self.view["select_label"] = {"pos": {"x": center["x"], "y": center["y"] - 40}, "id": unique_id("label")}

    def add_nail(self, pos):
        """Adds a fixed point (nail) to the graphical representation of the edge.

        Args:
            pos: The fixed point position.

        Returns:
            None
        """
        nail_id = unique_id("nail")
        self.view["nails"][nail_id] = {"pos": pos}

    def add_clock_guard(self, grd):
        """Adds an existing clock guard object to the edge.

        Args:
            grd: The clock guard object.

        Returns:
            The clock guard object.
        """
        self.clock_guards.append(grd)
        return grd

    def new_clock_guard(self, grd_data):
        """Creates a new clock guard object and add it to the edge.

        Args:
            grd_data: The clock guard text or AST dict.

        Returns:
            The clock guard object.
        """
        grd = ClockGuard(grd_data, self.parent)
        self.add_clock_guard(grd)
        return grd

    def add_variable_guard(self, grd):
        """Adds an existing variable guard object to the edge.

        Args:
            grd: The variable guard object.

        Returns:
            The variable guard object.
        """
        self.variable_guards.append(grd)
        return grd

    def new_variable_guard(self, grd_data):
        """Creates a new variable guard object and add it to the edge.

        Args:
            grd_data: The variable guard text or AST dict.

        Returns:
            The variable guard object.
        """
        grd = VariableGuard(grd_data, self.parent)
        self.add_variable_guard(grd)
        return grd

    def add_select(self, sel):
        """Adds an existing select object to the edge.

        Args:
            sel: The select object.

        Returns:
            The select object.
        """
        self.selects.append(sel)
        return sel

    def new_select(self, sel_data):
        """Creates a new select object and add it to the edge.

        Args:
            sel_data: The select text or AST dict.

        Returns:
            The select object.
        """
        sel = Select(sel_data, self.parent)
        self.add_select(sel)
        return sel

    def add_update(self, updt):
        """Adds an existing update object to the edge.

        Args:
            updt: The update object.

        Returns:
            The update object.
        """
        self.updates.append(updt)
        return updt

    def new_update(self, updt_data):
        """Creates a new update object and add it to the edge.

        Args:
            updt_data: The update text or AST dict.

        Returns:
            The update object.
        """
        updt = Update(updt_data, self.parent)
        self.add_update(updt)
        return updt

    def add_reset(self, rst):
        """Adds an existing clock reset object to the edge.

        Args:
            rst: The clock reset object.

        Returns:
            The clock reset object.
        """
        self.resets.append(rst)
        return rst

    def new_reset(self, rst_data):
        """Creates a new clock reset object and add it to the edge.

        Args:
            rst_data: The clock reset text or AST dict.

        Returns:
            The clock reset object.
        """
        rst = Reset(rst_data, self.parent)
        self.add_reset(rst)
        return rst

    def set_sync(self, sync):
        """Sets the synchronization label.

        Args:
            sync: The synchronization text or AST dict.

        Returns:
            The synchronization object.
        """
        if not isinstance(sync, Synchronization):
            sync = Synchronization(sync, self.parent)
        self.sync = sync
        return sync

    def assign_from(self, other, assign_ids=False, copy_view_data=True):
        """Assigns the attributes of the edge from another edge.

        Args:
            other: The other edge.
            assign_ids: Choose whether the IDs should be copied, too, or generated anew.
            copy_view_data: Choose whether the graphical view data should be copied as well.
        """
        super().assign_from(other)
        self.clock_guards = map(lambda grd: grd.copy(), other.clock_guards)
        self.variable_guards = map(lambda grd: grd.copy(), other.variable_guards)
        self.updates = map(lambda updt: updt.copy(), other.updates)
        self.resets = map(lambda rst: rst.copy(), other.resets)
        self.sync = other.sync.copy() if other.sync else None
        self.selects = map(lambda sel: sel.copy(), other.selects)

        if copy_view_data:
            self.view = {"nails": OrderedDict()}
            for nail_id in other.view["nails"]:
                nail = {"id": unique_id("nail"), "pos": {"x": other.view["nails"][nail_id]["pos"]["x"],
                                                         "y": other.view["nails"][nail_id]["pos"]["y"]}}
                self.view["nails"][nail["id"]] = nail

            self.view["guard_label"] = {
                "pos": {"x": other.view["guard_label"]["pos"]["x"], "y": other.view["guard_label"]["pos"]["y"]},
                "id": unique_id("label")}
            self.view["update_label"] = {
                "pos": {"x": other.view["update_label"]["pos"]["x"], "y": other.view["update_label"]["pos"]["y"]},
                "id": unique_id("label")}
            self.view["sync_label"] = {
                "pos": {"x": other.view["sync_label"]["pos"]["x"], "y": other.view["sync_label"]["pos"]["y"]},
                "id": unique_id("label")}
            self.view["select_label"] = {
                "pos": {"x": other.view["select_label"]["pos"]["x"], "y": other.view["select_label"]["pos"]["y"]},
                "id": unique_id("label")}

    def __str__(self):
        obj_str = super().__str__()

        clock_grd_strs = list(map(lambda v: f'"{v}"', self.clock_guards))
        obj_str += f'Clock Guards: ({len(self.clock_guards)}): {", ".join(clock_grd_strs)}\n'

        variable_grd_strs = list(map(lambda v: f'"{v}"', self.variable_guards))
        obj_str += f'Variable Guards: ({len(self.variable_guards)}): {", ".join(variable_grd_strs)}\n'

        updt_strs = list(map(lambda v: f'"{v}"', self.updates))
        obj_str += f'Updates ({len(self.updates)}): {", ".join(updt_strs)}\n'

        rst_strs = list(map(lambda v: f'"{v}"', self.resets))
        obj_str += f'Resets ({len(self.resets)}): {", ".join(rst_strs)}\n'

        obj_str += f'Sync: {self.sync}\n'

        selects_strs = list(map(lambda v: f'"{v}"', self.selects))
        obj_str += f'Selects ({len(self.selects)}): {", ".join(selects_strs)}\n'

        return obj_str
