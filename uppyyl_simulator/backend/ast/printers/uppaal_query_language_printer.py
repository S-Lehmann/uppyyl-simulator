"""The implementation of a printer for Uppaal query ASTs."""

from uppyyl_simulator.backend.data_structures.ast.ast_code_printer import (
    ASTCodePrinter
)
from uppyyl_simulator.backend.ast.printers.uppaal_c_language_printer import (
    UppaalCPrinter
)


####################
# AST code printer #
####################
class UppaalQueryPrinter(ASTCodePrinter):
    """The Uppaal query printer class."""

    def __init__(self, do_log_details=False):
        """Initializes UppaalQueryPrinter.

        Args:
            do_log_details: Choose whether intermediate details of the string generation should be printed.
        """
        super().__init__()
        self.do_log_details = do_log_details
        self.uppaal_c_printer = UppaalCPrinter()

    def ast_to_string(self, ast):
        """Generates a string from a given AST.

        Args:
            ast: The AST that is printed.

        Returns:
            The generated string.
        """
        if ast is None:
            return ""
        assert isinstance(ast, dict)

        if self.do_log_details:
            print(f'[ast_to_string] {ast["astType"]}: {list(ast.keys())}')
        if ast["astType"] in to_string_funcs:
            res = to_string_funcs[ast["astType"]](self, ast)
            if self.do_log_details:
                print(f'Result of {ast}: {res}')
            return res
        raise Exception("AST type \"" + ast["astType"] + "\" not supported by ast_to_string.")


#####################
# Query Expressions #
#####################
def predicate(printer, ast):
    """Prints a predicate."""
    return f'{printer.uppaal_c_printer.ast_to_string(ast["expr"])}'


def prop_all(printer, ast):
    """Prints an all property "A ..."."""
    prop_str = printer.ast_to_string(ast["prop"])
    return f'A{prop_str}'


def prop_exists(printer, ast):
    """Prints an exists property "E ..."."""
    prop_str = printer.ast_to_string(ast["prop"])
    return f'E{prop_str}'


def prop_leads_to(printer, ast):
    """Prints a leads to property "phi_1 -> phi_2"."""
    left_str = printer.ast_to_string(ast["left"])
    right_str = printer.ast_to_string(ast["right"])
    return f'{left_str} --> {right_str}'


def prop_globally(printer, ast):
    """Prints a globally property "[] ..."."""
    prop_str = printer.ast_to_string(ast["prop"])
    return f'[]{prop_str}'


def prop_finally(printer, ast):
    """Prints a finally property "<> ..."."""
    prop_str = printer.ast_to_string(ast["prop"])
    return f'<>{prop_str}'


def prop_until(printer, ast):
    """Prints an until property "phi_1 U phi_2"."""
    left_str = printer.ast_to_string(ast["left"])
    right_str = printer.ast_to_string(ast["right"])
    return f'{left_str} U {right_str}'


def prop_val_bounds(printer, ast):
    """Prints an infimum / supremum property "(inf|sup): prop"."""
    type_str = ast["type"]
    pred_str = f'{{{printer.ast_to_string(ast["predicate"])}}}' if ast.get("predicate") else ""
    exprs_str = ", ".join(map(lambda expr: printer.uppaal_c_printer.ast_to_string(expr), ast["exprs"]))
    return f'{type_str}{pred_str}: {exprs_str}'


def prop_time_bound(printer, ast):
    """Prints a simulate query "simulate n [<=t] {obs_vars}"."""
    var_str = f'{ast["var"]} ' if ast.get("var") else ""
    upper_bound_str = printer.uppaal_c_printer.ast_to_string(ast["upperBound"])
    return f'{var_str}<={upper_bound_str}'


def prop_smc_sim(printer, ast):
    """Prints a simulate query "simulate n [<=t] {obs_vars}"."""
    run_count_str = printer.uppaal_c_printer.ast_to_string(ast["runCount"])
    time_bound_str = printer.ast_to_string(ast["timeBound"])
    obs_vars_str = ", ".join(map(lambda var: printer.uppaal_c_printer.ast_to_string(var), ast["obsVars"]))
    return f'simulate {run_count_str} [{time_bound_str}] {{{obs_vars_str}}}'


def prop_smc_sim_accept_runs(printer, ast):
    """Prints a simulate query "simulate n [<= t] {obs_vars} : n : (pred)"."""
    simulate_str = printer.ast_to_string(ast["simulate"])
    accept_bound_str = printer.uppaal_c_printer.ast_to_string(ast["acceptBound"])
    pred_str = printer.ast_to_string(ast["predicate"])
    return f'{simulate_str} : {accept_bound_str} : ({pred_str})'


def prop_smc_prop_estimate(printer, ast):
    """Prints a prob. estimate query "Pr [<=t] ((<>|[]) prop))"."""
    time_bound_str = printer.ast_to_string(ast["timeBound"])
    prop_str = printer.ast_to_string(ast["prop"])
    return f'Pr [{time_bound_str}] ({prop_str})'


def prop_smc_hypothesis_test(printer, ast):
    """Prints a hypothesis testing query "Pr [<=t] (<> prop) <= 0.6"."""
    prop_estimate_str = printer.ast_to_string(ast["prop"])
    op_str = ast["op"]
    prob_val_str = printer.uppaal_c_printer.ast_to_string(ast["probVal"])
    return f'{prop_estimate_str} {op_str} {prob_val_str}'


def prop_smc_prob_compare(printer, ast):
    """Prints a prob. comparison query "Pr [<=t1] (<> prop1) <= Pr [<=t2] (<> prop2)"."""
    left_prop_estimate_str = printer.ast_to_string(ast["left"])
    op_str = ast["op"]
    right_prop_estimate_str = printer.ast_to_string(ast["right"])
    return f'{left_prop_estimate_str} {op_str} {right_prop_estimate_str}'


def prop_smc_value_estimate(printer, ast):
    """Prints a value estimate query "E[<=20; 10] ((min|max): x)"."""
    run_count_str = printer.uppaal_c_printer.ast_to_string(ast["runCount"])
    time_bound_str = printer.ast_to_string(ast["timeBound"])
    op_str = ast["op"]
    expr_str = printer.uppaal_c_printer.ast_to_string(ast["expr"])
    return f'E[{time_bound_str}; {run_count_str}] ({op_str}: {expr_str})'


to_string_funcs = {
    "Predicate": predicate,

    "PropAll": prop_all,
    "PropExists": prop_exists,
    "PropLeadsTo": prop_leads_to,

    "PropGlobally": prop_globally,
    "PropFinally": prop_finally,
    "PropUntil": prop_until,

    "PropValBounds":  prop_val_bounds,

    "PropTimeBound": prop_time_bound,
    "PropSMCSim": prop_smc_sim,
    "PropSMCSimAcceptRuns": prop_smc_sim_accept_runs,
    "PropSMCProbEstimate": prop_smc_prop_estimate,
    "PropSMCHypothesisTest": prop_smc_hypothesis_test,
    "PropSMCProbCompare": prop_smc_prob_compare,
    "PropSMCValueEstimate": prop_smc_value_estimate,
}
