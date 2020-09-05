"""Abstract class for an AST code element."""

import abc


class ASTCodeElement(abc.ABC):
    """An abstract AST code element."""

    def __init__(self, data):
        """Initializes ASTCodeElement.

        Args:
            data: The AST data in string form or as AST dict.
        """
        self.printer = None
        self.parser = None
        self.init_parser()
        self.init_printer()

        self.text = None
        self.ast = None
        if isinstance(data, str):
            self.set_text(data)
        else:
            self.set_ast(data)

    @abc.abstractmethod
    def init_parser(self):
        """Initializes the AST code parser.

        Returns:
            None
        """

    @abc.abstractmethod
    def init_printer(self):
        """Initializes the AST code printer.

        Returns:
            None
        """

    def update_text(self):
        """Updates the AST text string from the AST dict.

        Returns:
            None
        """
        self.text = self.printer.ast_to_string(self.ast)

    @abc.abstractmethod
    def update_ast(self):
        """Updates the AST dict from the AST text string.

        Returns:
            None
        """

    def set_text(self, text):
        """Sets the AST text string, and update the AST dict accordingly.

        Returns:
            None
        """
        self.text = text
        if text == "":
            self.ast = None
        else:
            self.update_ast()

    def set_ast(self, ast):
        """Sets the AST dict, and update the AST text string accordingly.

        Returns:
            None
        """
        self.ast = ast
        self.update_text()

    @abc.abstractmethod
    def copy(self):
        """Copies the ASTCodeElement instance.

        Returns:
            The copied ASTCodeElement instance.
        """


#################
# AST Functions #
#################
def apply_func_to_ast(ast, func):
    """Applies a function recursively to all (nested) elements of an AST.

    Args:
        ast: The AST instance.
        func: The function applied to the AST elements.

    Returns:
        The adapted AST and values accumulated during application.
    """
    acc = []
    ast = apply_func_to_ast_helper(ast, func, acc)
    return ast, acc


def apply_func_to_ast_helper(ast, func, acc):
    """Recursive helper function for "apply_func_to_ast".

    Args:
        ast: The AST instance.
        func: The function applied to the AST elements.
        acc: A list of values accumulated during application.

    Returns:
        The adapted AST.
    """
    if isinstance(ast, dict):  # If val is AST
        for prop_name, prop_val in ast.items():
            ast[prop_name] = apply_func_to_ast_helper(prop_val, func, acc)
        ast = func(ast, acc)
    elif isinstance(ast, list):  # If val is List
        for i in range(0, len(ast)):
            ast[i] = apply_func_to_ast_helper(ast[i], func, acc)
    return ast


def apply_funcs_to_ast(ast, funcs):
    """Applies multiple functions simultaneously to all (nested) elements of an AST.
    
    Args:
        ast: The AST instance.
        funcs: A list of functions applied to the AST elements simultaneously.

    Returns:
        The adapted AST.
    """

    def helper_func(ast_):
        """Helper function which applies the given functions to the AST.

        Args:
            ast_: The AST instance.

        Returns:
            The adapted AST.
        """
        for func in funcs:
            func(ast_)
        return ast_

    return apply_func_to_ast(ast, helper_func)
