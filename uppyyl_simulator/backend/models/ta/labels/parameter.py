"""A parameter label of an Uppaal template."""

import copy

from uppyyl_simulator.backend.ast.parsers.generated.uppaal_c_language_parser import UppaalCLanguageParser
from uppyyl_simulator.backend.ast.parsers.uppaal_c_language_semantics import UppaalCLanguageSemantics
from uppyyl_simulator.backend.ast.printers.uppaal_c_language_printer import UppaalCPrinter
from uppyyl_simulator.backend.data_structures.ast.ast_code_element import ASTCodeElement


#############
# Parameter #
#############
class Parameter(ASTCodeElement):
    """A template parameter class.

    The template parameters are used to assign individual values to the instance automata derived from a template.
    """

    def __init__(self, param_data, autom=None):
        """Initializes Parameter.

        Args:
            param_data: The parameter string or AST data.
        """
        super().__init__(param_data)
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
        """Copies the Parameter instance.

        Returns:
            The copied Parameter instance.
        """
        copy_param = Parameter(copy.deepcopy(self.ast))
        return copy_param

    def update_ast(self):
        """Updates the AST dict from the AST text string.

        Returns:
            None
        """
        self.ast = self.parser.parse(self.text, rule_name='Parameter')

    def __str__(self):
        return f'Parameter({self.text})'
