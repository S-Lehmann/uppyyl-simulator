"""The channel synchronization label of an Uppaal automaton edge."""

import copy

from uppyyl_simulator.backend.ast.parsers.generated.uppaal_c_language_parser import UppaalCLanguageParser

from uppyyl_simulator.backend.ast.parsers.uppaal_c_language_semantics import UppaalCLanguageSemantics
from uppyyl_simulator.backend.ast.printers.uppaal_c_language_printer import UppaalCPrinter
from uppyyl_simulator.backend.data_structures.ast.ast_code_element import ASTCodeElement


###################
# Synchronization #
###################
class Synchronization(ASTCodeElement):
    """An edge channel synchronization class.

    Via a channel synchronization, multiple edge can be synchronized and triggered simultaneously.
    """

    def __init__(self, sync_data, autom=None):
        """Initializes Synchronization.

        Args:
            sync_data: The edge channel synchronization string or AST data.
        """
        super().__init__(sync_data)
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
        """Copies the Synchronization instance.

        Returns:
            The copied Synchronization instance.
        """
        copy_sync = Synchronization(copy.deepcopy(self.ast))
        return copy_sync

    def update_ast(self):
        """Updates the AST dict from the AST text string.

        Returns:
            None
        """
        self.ast = self.parser.parse(self.text, rule_name='Sync')

    def __str__(self):
        return f'Sync({self.text})'
