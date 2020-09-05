"""The assignment labels of an Uppaal automaton edge."""

import copy

from uppyyl_simulator.backend.ast.parsers.generated.uppaal_c_language_parser import UppaalCLanguageParser

from uppyyl_simulator.backend.ast.parsers.uppaal_c_language_semantics import UppaalCLanguageSemantics
from uppyyl_simulator.backend.ast.printers.uppaal_c_language_printer import UppaalCPrinter
from uppyyl_simulator.backend.data_structures.ast.ast_code_element import ASTCodeElement


##########
# Update #
##########
class Update(ASTCodeElement):
    """An edge update class.

    Via an update, a non-clock variable is re-assigned.
    """

    def __init__(self, updt_data, autom=None):
        """Initializes Update.

        Args:
            updt_data: The edge update string or AST data.
        """
        super().__init__(updt_data)
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
        """Copies the Update instance.

        Returns:
            The copied Update instance.
        """
        copy_updt = Update(copy.deepcopy(self.ast))
        return copy_updt

    def update_ast(self):
        """Updates the AST dict from the AST text string.

        Returns:
            None
        """
        self.ast = self.parser.parse(self.text, rule_name='Update')

    def __str__(self):
        return f'Update({self.text})'


#########
# Reset #
#########
class Reset(ASTCodeElement):
    """An edge clock reset class.

    Via a clock reset, a clock variable is re-assigned.
    """
    def __init__(self, rst_data, autom=None):
        """Initializes Reset.

        Args:
            rst_data: The edge clock reset string or AST data.
        """
        super().__init__(rst_data)
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
        """Copies the Reset instance.

        Returns:
            The copied Reset instance.
        """
        copy_reset = Reset(copy.deepcopy(self.ast))
        return copy_reset

    def update_ast(self):
        """Updates the AST dict from the AST text string.

        Returns:
            None
        """
        self.ast = self.parser.parse(self.text, rule_name='Update')

    def __str__(self):
        return f'Reset({self.text})'
