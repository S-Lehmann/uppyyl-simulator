"""The select labels of an Uppaal automaton edge."""

import copy

from uppyyl_simulator.backend.ast.parsers.generated.uppaal_c_language_parser import UppaalCLanguageParser

from uppyyl_simulator.backend.ast.parsers.uppaal_c_language_semantics import UppaalCLanguageSemantics
from uppyyl_simulator.backend.ast.printers.uppaal_c_language_printer import UppaalCPrinter
from uppyyl_simulator.backend.data_structures.ast.ast_code_element import ASTCodeElement


##########
# Select #
##########
class Select(ASTCodeElement):
    """An edge select statement class.

    Via a select, a transition is split into individual transitions for each possible select value assignment.
    """

    def __init__(self, sel_data, autom=None):
        """Initializes Select.

        Args:
            sel_data: The edge select statement string or AST data.
        """
        super().__init__(sel_data)
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
        """Copies the Select instance.

        Returns:
            The copied Select instance.
        """
        copy_sync = Select(copy.deepcopy(self.ast))
        return copy_sync

    def update_ast(self):
        """Updates the AST dict from the AST text string.

        Returns:
            None
        """
        self.ast = self.parser.parse(self.text, rule_name='Select')

    def __str__(self):
        return f'Select({self.text})'
