"""This module implements additional semantics for the parsing results of the Uppaal C Language parser."""

from enum import Enum


##############################
# Associativity / Precedence #
##############################
class Associativity(Enum):
    """An enum of possible associativity."""
    LEFT = 0
    RIGHT = 1


all_op_data = {
    # Parentheses and ArrayAccess excluded so that additional bracket expressions are not required for inner expressions
    # "Parentheses": {"associativity": Associativity.LEFT, "precedence": 1},  # FunctionCall
    # "ArrayAccess": {"associativity": Associativity.LEFT, "precedence": 1},  # SquareBrackets
    "Dot": {"associativity": Associativity.LEFT, "precedence": 1},
    "PostIncrAssign": {"associativity": Associativity.LEFT, "precedence": 1},
    "PostDecrAssign": {"associativity": Associativity.LEFT, "precedence": 1},
    "Plus": {"associativity": Associativity.RIGHT, "precedence": 2},
    "Minus": {"associativity": Associativity.RIGHT, "precedence": 2},
    "LogNot": {"associativity": Associativity.RIGHT, "precedence": 2},
    "PreIncrAssign": {"associativity": Associativity.RIGHT, "precedence": 2},
    "PreDecrAssign": {"associativity": Associativity.RIGHT, "precedence": 2},
    "Neg": {"associativity": Associativity.RIGHT, "precedence": 2},
    "Mult": {"associativity": Associativity.LEFT, "precedence": 3},
    "Div": {"associativity": Associativity.LEFT, "precedence": 3},
    "Mod": {"associativity": Associativity.LEFT, "precedence": 3},
    "Sub": {"associativity": Associativity.LEFT, "precedence": 4},
    "Add": {"associativity": Associativity.LEFT, "precedence": 4},
    "LShift": {"associativity": Associativity.LEFT, "precedence": 5},
    "RShift": {"associativity": Associativity.LEFT, "precedence": 5},
    "Minimum": {"associativity": Associativity.LEFT, "precedence": 6},
    "Maximum": {"associativity": Associativity.LEFT, "precedence": 6},
    "LessThan": {"associativity": Associativity.LEFT, "precedence": 7},
    "LessEqual": {"associativity": Associativity.LEFT, "precedence": 7},
    "GreaterEqual": {"associativity": Associativity.LEFT, "precedence": 7},
    "GreaterThan": {"associativity": Associativity.LEFT, "precedence": 7},
    "Equal": {"associativity": Associativity.LEFT, "precedence": 8},
    "NotEqual": {"associativity": Associativity.LEFT, "precedence": 8},
    "BitAnd": {"associativity": Associativity.LEFT, "precedence": 9},
    "BitXor": {"associativity": Associativity.LEFT, "precedence": 10},
    "BitOr": {"associativity": Associativity.LEFT, "precedence": 11},
    "LogAnd": {"associativity": Associativity.LEFT, "precedence": 12},
    "LogOr": {"associativity": Associativity.LEFT, "precedence": 13},
    "Imply": {"associativity": Associativity.LEFT, "precedence": 13},
    "Ternary": {"associativity": Associativity.RIGHT, "precedence": 14},
    # "TernaryThenOp":  {"associativity": Associativity.RIGHT, "precedence": 14},
    # "TernaryElseOp":  {"associativity": Associativity.RIGHT, "precedence": 14},
    "Assign": {"associativity": Associativity.RIGHT, "precedence": 15},
    "AddAssign": {"associativity": Associativity.RIGHT, "precedence": 15},
    "SubAssign": {"associativity": Associativity.RIGHT, "precedence": 15},
    "MultAssign": {"associativity": Associativity.RIGHT, "precedence": 15},
    "DivAssign": {"associativity": Associativity.RIGHT, "precedence": 15},
    "ModAssign": {"associativity": Associativity.RIGHT, "precedence": 15},
    "BitAndAssign": {"associativity": Associativity.RIGHT, "precedence": 15},
    "BitOrAssign": {"associativity": Associativity.RIGHT, "precedence": 15},
    "LShiftAssign": {"associativity": Associativity.RIGHT, "precedence": 15},
    "RShiftAssign": {"associativity": Associativity.RIGHT, "precedence": 15},
    "BitXorAssign": {"associativity": Associativity.RIGHT, "precedence": 15},
    "ForAll": {"associativity": Associativity.LEFT, "precedence": 16},
    "Exists": {"associativity": Associativity.LEFT, "precedence": 16},
    "Sum": {"associativity": Associativity.LEFT, "precedence": 16},
}


def ast_rotate_right(ast):
    """Performs a right rotation of the AST around its root.

    Args:
        ast: The AST dict.

    Returns:
        The new root of the rotated AST.
    """
    root = ast
    if "left" in root:  # If root is binary
        pivot = root["left"]
        if "right" in pivot:  # If pivot is binary
            root["left"] = pivot["right"]
            pivot["right"] = root
        elif "expr" in pivot:  # If pivot is unary
            root["left"] = pivot["expr"]
            pivot["expr"] = root
    elif "expr" in root:  # If root is unary
        pivot = root["expr"]
        if "right" in pivot:  # If pivot is binary
            root["expr"] = pivot["right"]
            pivot["right"] = root
        elif "expr" in pivot:  # If pivot is unary
            root["expr"] = pivot["expr"]
            pivot["expr"] = root
    else:
        return root

    new_root = pivot
    return new_root


def _check_left_assoc_prec(op_data, op_child_data):
    return ((op_data["precedence"] < op_child_data["precedence"]) or
            ((op_data["precedence"] == op_child_data["precedence"]) and
             (op_data["associativity"] == Associativity.LEFT)))


def ast_rotate_right_while_assoc_prec(ast):
    """Performs a right rotation of the AST around its root if associativity and precedence are not enforced yet.

    Args:
        ast: The AST dict.

    Returns:
        The new root of the rotated AST.
    """

    if ("op" in ast) and (ast["op"] in all_op_data):
        if ("left" in ast) and ("op" in ast["left"]) and (ast["left"]["op"] in all_op_data):  # If child is binary
            op_data = all_op_data[ast["op"]]
            op_child_data = all_op_data[ast["left"]["op"]]
        elif ("expr" in ast) and ("op" in ast["expr"]) and (ast["expr"]["op"] in all_op_data):  # If child is unary
            op_data = all_op_data[ast["op"]]
            op_child_data = all_op_data[ast["expr"]["op"]]
        else:
            return ast

        if _check_left_assoc_prec(op_data, op_child_data):
            ast = ast_rotate_right(ast)
            if "left" in ast:
                ast["left"] = ast_rotate_right_while_assoc_prec(ast["left"])
            elif "expr" in ast:
                ast["expr"] = ast_rotate_right_while_assoc_prec(ast["expr"])

    return ast


def ast_rotate_left(ast):
    """Performs a left rotation of the binary AST around its root.

    Args:
        ast: The AST dict.

    Returns:
        The new root of the rotated AST.
    """
    root = ast
    if "right" in root:  # If root is binary
        pivot = root["right"]
        if "left" in pivot:  # If pivot is binary
            root["right"] = pivot["left"]
            pivot["left"] = root
        elif "expr" in pivot:  # If pivot is unary
            root["right"] = pivot["expr"]
            pivot["expr"] = root
    elif "expr" in root:  # If root is unary
        pivot = root["expr"]
        if "left" in pivot:  # If pivot is binary
            root["expr"] = pivot["left"]
            pivot["left"] = root
        elif "expr" in pivot:  # If pivot is unary
            root["expr"] = pivot["expr"]
            pivot["expr"] = root
    else:
        return root

    new_root = pivot
    return new_root


def ast_rotate_left_while_assoc_prec(ast):
    """Performs a left rotation of the AST around its root if associativity and precedence are not enforced yet.

    Args:
        ast: The AST dict.

    Returns:
        The new root of the rotated AST.
    """
    if ("op" in ast) and (ast["op"] in all_op_data):
        if ("right" in ast) and ("op" in ast["right"]) and (ast["right"]["op"] in all_op_data):  # If child is binary
            op_data = all_op_data[ast["op"]]
            op_child_data = all_op_data[ast["right"]["op"]]
        elif ("expr" in ast) and ("op" in ast["expr"]) and (ast["expr"]["op"] in all_op_data):  # If child is unary
            op_data = all_op_data[ast["op"]]
            op_child_data = all_op_data[ast["expr"]["op"]]
        else:
            return ast

        if _check_left_assoc_prec(op_data, op_child_data):
            ast = ast_rotate_left(ast)
            if "left" in ast:
                ast["left"] = ast_rotate_left_while_assoc_prec(ast["left"])
            elif "expr" in ast:
                ast["expr"] = ast_rotate_left_while_assoc_prec(ast["expr"])

    return ast


# Split logical conjunction for composed location invariants and edge guards
def split_logic_conjunction(ast):
    """Splits a top-level logical conjunction of expressions into sub-expressions.

    Args:
        ast: The AST dict.

    Returns:
        The list of sub-expressions.
    """
    terms = []
    ast = ast["expr"]
    if "op" not in ast:
        terms.insert(0, ast)
        return terms

    while ast["op"] == "LogAnd":
        terms.insert(0, ast["right"])
        ast = ast["left"]
    terms.insert(0, ast)
    return terms


# Required as the AST returned by TatSu is only a dict-like object with additional unwanted properties
def ast_dict_to_dict(ast):
    """Transforms a TatSu-type dictionary into a regular dict.

    Args:
        ast: The TatSu-type AST dict.

    Returns:
        The regular AST dict.
    """
    if isinstance(ast, dict):
        return dict(ast)
    return ast


###############################
# Uppaal C Language Semantics #
###############################
# noinspection PyPep8Naming
class UppaalCLanguageSemantics(object):
    """This class implements additional semantics for the parsing results of the Uppaal C Language parser."""

    def __init__(self):
        """Initializes UppaalCLanguageSemantics."""
        pass

    def Expression(self, ast):
        """Adapts an expression AST to enforce associativity and precedences via AST rotation."""
        ast = self._default(ast)
        ast = ast_rotate_left_while_assoc_prec(ast)
        return ast

    def QExpression(self, ast):
        """Adapts an expression AST to enforce associativity and precedences via AST rotation."""
        ast = self._default(ast)
        ast = ast_rotate_left_while_assoc_prec(ast)
        return ast

    def Variable(self, ast):
        """Transforms array indices to individual (nested) array access calls."""
        ast = self._default(ast)
        if "indices" in ast:
            indices = ast["indices"]
            del ast["indices"]
            for i in range(0, len(indices)):
                ast = {
                    "left": ast,
                    "op": "ArrayAccess",
                    "right": indices[i],
                    "astType": "BinaryExpr",
                }
        return ast

    def Invariants(self, ast):
        """Splits an invariant AST by logic conjunctions."""
        ast = self._default(ast)
        invs = split_logic_conjunction(ast)
        asts = list(map(lambda inv: {'astType': 'Invariant', 'expr': inv}, invs))
        return asts

    def Guards(self, ast):
        """Splits a guard AST by logic conjunctions."""
        ast = self._default(ast)
        grds = split_logic_conjunction(ast)
        asts = list(map(lambda grd: {'astType': 'Guard', 'expr': grd}, grds))
        return asts

    def Integer(self, ast):
        """Replaces the integer value string with an actual integer value."""
        ast = self._default(ast)
        ast["val"] = int(ast["val"])
        return ast

    def Double(self, ast):
        """Replaces the double value string with an actual float value."""
        ast = self._default(ast)
        ast["val"] = float(ast["val"])
        return ast

    def Boolean(self, ast):
        """Replaces the bool value string with an actual bool value."""
        ast = self._default(ast)
        ast["val"] = (ast["val"] == "true")
        return ast

    @staticmethod
    def _default(ast):
        return ast_dict_to_dict(ast)
