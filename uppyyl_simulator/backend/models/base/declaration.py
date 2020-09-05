"""The variable declaration of an automaton network."""

import copy

from uppyyl_simulator.backend.data_structures.ast.ast_code_element import (
    ASTCodeElement, apply_func_to_ast
)
from uppyyl_simulator.backend.ast.parsers.generated.uppaal_c_language_parser import (
    UppaalCLanguageParser
)
from uppyyl_simulator.backend.ast.printers.uppaal_c_language_printer import (
    UppaalCPrinter
)
from uppyyl_simulator.backend.ast.parsers.uppaal_c_language_semantics import (
    UppaalCLanguageSemantics
)


###############
# Declaration #
###############
class Declaration(ASTCodeElement):
    """A declaration class.

    In the declaration, all functions, types and data variables used by the system are defined.
    """

    def __init__(self, decl_data):
        """Initializes Declaration.

        Args:
            decl_data: The declaration string or AST data.
        """
        super().__init__(decl_data)
        self._identify_clocks()

    def init_parser(self):
        """Initializes the AST code parser.

        Returns:
            None
        """
        self.parser = UppaalCLanguageParser(semantics=UppaalCLanguageSemantics())

    def init_printer(self):
        """Initializes the AST code printer.

        Returns:
            None
        """
        self.printer = UppaalCPrinter()

    def copy(self):
        """Copies the Declaration instance.

        Returns:
            The copied Declaration instance.
        """
        copy_decl = Declaration(copy.deepcopy(self.ast))
        return copy_decl

    def update_ast(self):
        """Updates the AST dict from the AST text string.

        Returns:
            None
        """
        self.ast = self.parser.parse(self.text, rule_name='UppaalDeclaration', trace=False)

    def __str__(self):
        return f'Declaration(\n{self.text}\n)'

    def _identify_clocks(self):
        _, clocks = apply_func_to_ast(self.ast, _get_clock)
        self.clocks = clocks


def _get_clock(ast, acc):
    """Gets the AST element if it is a clock.

    Args:
        ast: The AST element.
        acc: The list of accumulated clocks

    Returns:

    """
    if ast["astType"] == "VariableDecls":
        if ast["type"]["typeId"]["astType"] == "CustomType" and ast["type"]["typeId"]["type"] == "clock":
            for single_var_data in ast["varData"]:
                acc.append(single_var_data["varName"])
    return ast
