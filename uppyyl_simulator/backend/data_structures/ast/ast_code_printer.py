"""Abstract class for an AST code printer."""

import abc


class ASTCodePrinter(abc.ABC):
    """An abstract AST code printer."""

    def __init__(self):
        """Initializes ASTCodePrinter."""

    @abc.abstractmethod
    def ast_to_string(self, ast):
        """Prints an AST into a code string.

        Args:
            ast: The AST object.

        Returns:
            The code string.
        """
