"""Abstract class for an AST code evaluator."""

import abc


class ASTCodeEvaluator(abc.ABC):
    """An abstract AST code element."""

    def __init__(self):
        """Initializes ASTCodeEvaluator."""

    @abc.abstractmethod
    def eval_ast(self, ast, state):
        """Evaluates an AST dict.

        Args:
            ast: The AST object.
            state: The state context in which the AST is evaluated.

        Returns:
            None
        """
