"""The guard labels of an Uppaal automaton edge."""

import copy

from uppyyl_simulator.backend.ast.parsers.generated.uppaal_c_language_parser import UppaalCLanguageParser

from uppyyl_simulator.backend.ast.parsers.uppaal_c_language_semantics import UppaalCLanguageSemantics
from uppyyl_simulator.backend.ast.printers.uppaal_c_language_printer import UppaalCPrinter
from uppyyl_simulator.backend.data_structures.ast.ast_code_element import ASTCodeElement


##################
# Variable Guard #
##################
class VariableGuard(ASTCodeElement):
    """An edge variable guard class.

    Via a variable guard, a condition on a non-clock variable is enforced.
    """

    def __init__(self, grd_data, autom=None):
        """Initializes VariableGuard.

        Args:
            grd_data: The edge variable guard string or AST data.
        """
        super().__init__(grd_data)
        self.autom = autom

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
        """Copies the VariableGuard instance.

        Returns:
            The copied VariableGuard instance.
        """
        copy_grd = VariableGuard(copy.deepcopy(self.ast))
        return copy_grd

    def update_ast(self):
        """Updates the AST dict from the AST text string.

        Returns:
            None
        """
        self.ast = self.parser.parse(self.text, rule_name='Guard')

    def __str__(self):
        return f'VariableGuard({self.text})'


###############
# Clock Guard #
###############
class ClockGuard(ASTCodeElement):
    """An edge variable guard class.

    Via a clock guard, a condition on a clock variable is enforced.
    """

    def __init__(self, grd_data, autom=None):
        """Initializes ClockGuard.

        Args:
            grd_data: The edge clock guard string or AST data.
        """
        super().__init__(grd_data)
        self.autom = autom

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
        """Copies the ClockGuard instance.

        Returns:
            The copied ClockGuard instance.
        """
        copy_grd = ClockGuard(copy.deepcopy(self.ast))
        return copy_grd

    def update_ast(self):
        """Updates the AST dict from the AST text string.

        Returns:
            None
        """
        self.ast = self.parser.parse(self.text, rule_name='Guard')

    def __str__(self):
        return f'ClockGuard({self.text})'
