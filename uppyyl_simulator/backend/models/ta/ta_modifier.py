"""This module implements modifiers for Uppaal TAs."""

from uppyyl_simulator.backend.data_structures.ast.ast_code_element import (
    apply_funcs_to_ast
)


####################
# TemplateModifier #
####################
class TemplateModifier:
    """This class provides the modifiers for Uppaal TAs."""

    def __init__(self):
        """Initializes TemplateModifier."""
        pass

    @staticmethod
    def scale_view(tmpl, scale_factor):
        """Scales the view data of all TA template components (e.g., to get space for new intermediate locations).

        Args:
            tmpl: The template object.
            scale_factor: The factor by which the view should be scaled.
        """
        for loc_id in tmpl.locations:
            loc = tmpl.locations[loc_id]

            old_loc_pos = loc.view["self"]["pos"]
            new_loc_pos = {"x": old_loc_pos["x"] * scale_factor, "y": old_loc_pos["y"] * scale_factor}
            loc_diff = {"x": new_loc_pos["x"] - old_loc_pos["x"], "y": new_loc_pos["y"] - old_loc_pos["y"]}
            loc.set_whole_position(new_loc_pos)
            for edge_id in loc.out_edges:
                edge = loc.out_edges[edge_id]
                edge.view["grd_label"]["pos"]["x"] += loc_diff["x"]
                edge.view["grd_label"]["pos"]["y"] += loc_diff["y"]
                edge.view["assign_label"]["pos"]["x"] += loc_diff["x"]
                edge.view["assign_label"]["pos"]["y"] += loc_diff["y"]
                edge.view["sync_label"]["pos"]["x"] += loc_diff["x"]
                edge.view["sync_label"]["pos"]["y"] += loc_diff["y"]
                edge.view["select_label"]["pos"]["x"] += loc_diff["x"]
                edge.view["select_label"]["pos"]["y"] += loc_diff["y"]

                nails = edge.view["nails"]
                for nail_id in nails:
                    nail = nails[nail_id]
                    nail["pos"]["x"] *= scale_factor
                    nail["pos"]["y"] *= scale_factor

    @staticmethod
    def adapt_asts(tmpl, adaptions):
        """Adapts the asts of a template (in locations and edges).

        Args:
            tmpl: The template object.
            adaptions (list of func): The list of adaption functions

        Returns:
            None
        """
        for loc_id in tmpl.locations:
            loc = tmpl.locations[loc_id]
            LocationModifier.adapt_asts(loc, adaptions)

        for edge_id in tmpl.edges:
            edge = tmpl.edges[edge_id]
            EdgeModifier.adapt_asts(edge, adaptions)

    @staticmethod
    def replace_variables(tmpl, replacements):
        """Replace multiple variables simultaneously.

        Args:
            tmpl: The template object.
            replacements: The list of search-replace functions

        Returns:
            None
        """
        pass

    # replace_variable(var_name, new_ast) {
    #     self.adapt_asts([
    #     { "select_func": (ast) => ast.type == 'Variable' && ast.name == var_name,
    #        "adapt_func":    (ast) => {return copy_ast(new_ast);} }
    #     ]);
    # }

    # replace_variables(adaptions) {
    #     for (var i=0; i<adaptions.length; i++) {
    #         adaptions[i][0] = {"type": "Variable", "name": replacements[i][0]};
    #     }
    #     self.adapt_asts(replacements);
    # }


####################
# LocationModifier #
####################
class LocationModifier:
    """This class provides the modifiers for Uppaal TA locations."""
    def __init__(self):
        pass

    @staticmethod
    def adapt_asts(loc, adaptions):
        """Adapts the asts of a location (in invariants).

        Args:
            loc: The location object.
            adaptions (list of func): The list of adaption functions

        Returns:
            None
        """
        for i in range(0, len(loc.invariants)):
            inv = loc.invariants[i]
            inv.ast = apply_funcs_to_ast(inv.ast, adaptions)
            inv.update_text()


################
# EdgeModifier #
################
class EdgeModifier:
    """This class provides the modifiers for Uppaal TA edges."""
    def __init__(self):
        pass

    @staticmethod
    def adapt_asts(edge, adaptions):
        """Adapts the asts of an edge (in guards, invariants, assignments, syncs, and selects).

        Args:
            edge: The edge object
            adaptions : The list of search-replace functions

        Returns:
            None
        """
        for i in range(0, len(edge.clock_guards)):
            grd = edge.clock_guards[i]
            grd.ast = apply_funcs_to_ast(grd.ast, adaptions)
            grd.update_text()

        for i in range(0, len(edge.variable_guards)):
            grd = edge.variable_guards[i]
            grd.ast = apply_funcs_to_ast(grd.ast, adaptions)
            grd.update_text()

        for i in range(0, len(edge.updates)):
            updt = edge.updates[i]
            updt.ast = apply_funcs_to_ast(updt.ast, adaptions)
            updt.update_text()

        for i in range(0, len(edge.resets)):
            rst = edge.resets[i]
            rst.ast = apply_funcs_to_ast(rst.ast, adaptions)
            rst.update_text()

        sync = edge.sync
        sync.ast = apply_funcs_to_ast(sync.ast, adaptions)
        sync.update_text()

        for i in range(0, len(edge.selects)):
            sel = edge.selects[i]
            sel.ast = apply_funcs_to_ast(sel.ast, adaptions)
            sel.update_text()
