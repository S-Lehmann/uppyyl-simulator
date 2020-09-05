"""The implementation of a printer for Uppaal C code ASTs."""

from uppyyl_simulator.backend.data_structures.ast.ast_code_printer import (
    ASTCodePrinter
)
from uppyyl_simulator.backend.helper.helper import indent


####################
# AST code printer #
####################
class UppaalCPrinter(ASTCodePrinter):
    """The Uppaal C code printer class."""

    def __init__(self, do_log_details=False):
        """Initializes UppaalCPrinter.

        Args:
            do_log_details: Choose whether intermediate details of the string generation should be printed.
        """
        super().__init__()
        self.do_log_details = do_log_details

    def ast_to_string(self, ast):
        """Generates a string from a given AST.

        Args:
            ast: The AST that is printed.

        Returns:
            The generated string.
        """
        if ast is None:
            return ""
        assert isinstance(ast, dict)

        if self.do_log_details:
            print(f'[ast_to_string] {ast["astType"]}: {list(ast.keys())}')
        if ast["astType"] in to_string_funcs:
            res = to_string_funcs[ast["astType"]](self, ast)
            if self.do_log_details:
                print(f'Result of {ast}: {res}')
            return res
        raise Exception("AST type \"" + ast["astType"] + "\" not supported by UppaalCPrinter.")


#####################
# Unary Expressions #
#####################
def plus(printer, ast):
    """Prints "+expr"."""
    return f'+{printer.ast_to_string(ast["expr"])}'


def minus(printer, ast):
    """Prints "-expr"."""
    return f'-{printer.ast_to_string(ast["expr"])}'


def log_not(printer, ast):
    """Prints "!expr"."""
    return f'!{printer.ast_to_string(ast["expr"])}'


######################
# Binary Expressions #
######################
def dot(printer, ast):
    """Prints "left.right"."""
    return f'{printer.ast_to_string(ast["left"])}.{printer.ast_to_string(ast["right"])}'


def array_access(printer, ast):
    """Prints "left[right]"."""
    return f'{printer.ast_to_string(ast["left"])}[{printer.ast_to_string(ast["right"])}]'


###

def add(printer, ast):
    """Prints "left + right"."""
    return f'{printer.ast_to_string(ast["left"])} + {printer.ast_to_string(ast["right"])}'


def sub(printer, ast):
    """Prints "left - right"."""
    return f'{printer.ast_to_string(ast["left"])} - {printer.ast_to_string(ast["right"])}'


def mult(printer, ast):
    """Prints "left * right"."""
    return f'{printer.ast_to_string(ast["left"])} * {printer.ast_to_string(ast["right"])}'


def div(printer, ast):
    """Prints "left / right"."""
    return f'{printer.ast_to_string(ast["left"])} / {printer.ast_to_string(ast["right"])}'


def mod(printer, ast):
    """Prints "left % right"."""
    return f'{printer.ast_to_string(ast["left"])} % {printer.ast_to_string(ast["right"])}'


def l_shift(printer, ast):
    """Prints "left << right"."""
    return f'{printer.ast_to_string(ast["left"])} << {printer.ast_to_string(ast["right"])}'


def r_shift(printer, ast):
    """Prints "left >> right"."""
    return f'{printer.ast_to_string(ast["left"])} >> {printer.ast_to_string(ast["right"])}'


###

def log_and(printer, ast):
    """Prints "left && right"."""
    return f'{printer.ast_to_string(ast["left"])} && {printer.ast_to_string(ast["right"])}'


def log_or(printer, ast):
    """Prints "left || right"."""
    return f'{printer.ast_to_string(ast["left"])} || {printer.ast_to_string(ast["right"])}'


def log_imply(printer, ast):
    """Prints "left imply right"."""
    return f'{printer.ast_to_string(ast["left"])} imply {printer.ast_to_string(ast["right"])}'


def bit_and(printer, ast):
    """Prints "left & right"."""
    return f'{printer.ast_to_string(ast["left"])} & {printer.ast_to_string(ast["right"])}'


def bit_or(printer, ast):
    """Prints "left | right"."""
    return f'{printer.ast_to_string(ast["left"])} | {printer.ast_to_string(ast["right"])}'


def bit_xor(printer, ast):
    """Prints "left ^ right"."""
    return f'{printer.ast_to_string(ast["left"])} ^ {printer.ast_to_string(ast["right"])}'


###

def minimum(printer, ast):
    """Prints "min(left, right)"."""
    return f'{printer.ast_to_string(ast["left"])} <? {printer.ast_to_string(ast["right"])}'


def maximum(printer, ast):
    """Prints "max(left, right)"."""
    return f'{printer.ast_to_string(ast["left"])} >? {printer.ast_to_string(ast["right"])}'


def greater_equal(printer, ast):
    """Prints "left >= right"."""
    return f'{printer.ast_to_string(ast["left"])} >= {printer.ast_to_string(ast["right"])}'


def greater_than(printer, ast):
    """Prints "left > right"."""
    return f'{printer.ast_to_string(ast["left"])} > {printer.ast_to_string(ast["right"])}'


def less_equal(printer, ast):
    """Prints "left <= right"."""
    return f'{printer.ast_to_string(ast["left"])} <= {printer.ast_to_string(ast["right"])}'


def less_than(printer, ast):
    """Prints "left < right"."""
    return f'{printer.ast_to_string(ast["left"])} < {printer.ast_to_string(ast["right"])}'


def equal(printer, ast):
    """Prints "left == right"."""
    return f'{printer.ast_to_string(ast["left"])} == {printer.ast_to_string(ast["right"])}'


def not_equal(printer, ast):
    """Prints "left != right"."""
    return f'{printer.ast_to_string(ast["left"])} != {printer.ast_to_string(ast["right"])}'


###

def assign(printer, ast):
    """Prints "left = right"."""
    return f'{printer.ast_to_string(ast["left"])} = {printer.ast_to_string(ast["right"])}'


def add_assign(printer, ast):
    """Prints "left += right"."""
    return f'{printer.ast_to_string(ast["left"])} += {printer.ast_to_string(ast["right"])}'


def sub_assign(printer, ast):
    """Prints "left -= right"."""
    return f'{printer.ast_to_string(ast["left"])} -= {printer.ast_to_string(ast["right"])}'


def mult_assign(printer, ast):
    """Prints "left *= right"."""
    return f'{printer.ast_to_string(ast["left"])} *= {printer.ast_to_string(ast["right"])}'


def div_assign(printer, ast):
    """Prints "left /= right"."""
    return f'{printer.ast_to_string(ast["left"])} /= {printer.ast_to_string(ast["right"])}'


def mod_assign(printer, ast):
    """Prints "left %= right"."""
    return f'{printer.ast_to_string(ast["left"])} %= {printer.ast_to_string(ast["right"])}'


def l_shift_assign(printer, ast):
    """Prints "left <<= right"."""
    return f'{printer.ast_to_string(ast["left"])} <<= {printer.ast_to_string(ast["right"])}'


def r_shift_assign(printer, ast):
    """Prints "left >>= right"."""
    return f'{printer.ast_to_string(ast["left"])} >>= {printer.ast_to_string(ast["right"])}'


def bit_and_assign(printer, ast):
    """Prints "left &= right"."""
    return f'{printer.ast_to_string(ast["left"])} &= {printer.ast_to_string(ast["right"])}'


def bit_or_assign(printer, ast):
    """Prints "left |= right"."""
    return f'{printer.ast_to_string(ast["left"])} |= {printer.ast_to_string(ast["right"])}'


def bit_xor_assign(printer, ast):
    """Prints "left ^= right"."""
    return f'{printer.ast_to_string(ast["left"])} ^= {printer.ast_to_string(ast["right"])}'


##########
# Others #
##########
def uppaal_declaration(printer, ast):
    """Prints the Uppaal declaration."""
    return '\n'.join(map(lambda x: printer.ast_to_string(x), ast["decls"]))


def uppaal_system_declaration(printer, ast):
    """Prints the Uppaal system declaration."""
    decls_str = '\n'.join(map(lambda decl: printer.ast_to_string(decl), ast["decls"]))
    # instances_str = '\n'.join(map(lambda inst: printer.ast_to_string(inst), ast["instances"]))
    system_decl_str = printer.ast_to_string(ast["systemDecl"])
    return f'{decls_str}\n{system_decl_str}'


###

# def empty_line(printer, ast):
#     return f'\n'

# def line_comment(_printer, ast):
#     return f'//{ast["comment"]}'
#
#
# def block_comment(_printer, ast):
#     return f'/*{ast["comment"]}*/'


###

def variable_decls(printer, ast):
    """Prints "type varName [= initData]"."""
    type_str = printer.ast_to_string(ast["type"])
    var_data_str = ', '.join(map(lambda var: printer.ast_to_string(var), ast["varData"]))
    return f'{type_str} {var_data_str};'


def variable_id(printer, ast):
    """Prints "varName [= initData]"."""
    var_name_str = ast["varName"]
    array_decl_str = ''.join(map(lambda decl: f'[{printer.ast_to_string(decl)}]', ast["arrayDecl"]))
    init_data_str = f' = {printer.ast_to_string(ast["initData"])}' if ast.get("initData") else ''
    return f'{var_name_str}{array_decl_str}{init_data_str}'


def initialiser_array(printer, ast):
    """Prints initial values "= { ... }"."""
    vals_str = ','.join(map(lambda var: printer.ast_to_string(var), ast["vals"]))
    return f'{{ {vals_str} }}'


def type_decls(printer, ast):
    """Prints "typedef ..."."""
    type_str = printer.ast_to_string(ast["type"])
    names_str = ', '.join(map(lambda name: printer.ast_to_string(name), ast["names"]))
    return f'typedef {type_str} {names_str};'


###

def type_(printer, ast):
    """Prints "[const|meta|...] type"."""
    prefixes_str = ''.join(map(lambda prefix: f'{prefix} ', ast["prefixes"]))
    type_id_str = printer.ast_to_string(ast["typeId"])
    return f'{prefixes_str}{type_id_str}'


def bounded_int_type(printer, ast):
    """Prints "int[a,b]"."""
    lower_str = printer.ast_to_string(ast["lower"])
    upper_str = printer.ast_to_string(ast["upper"])
    return f'int[{lower_str}, {upper_str}]'


def scalar_type(printer, ast):
    """Prints "scalar[n]"."""
    expr_str = printer.ast_to_string(ast["expr"])
    return f'scalar[{expr_str}]'


def struct_type(printer, ast):
    """Prints "struct {...}"."""
    field_decls_str = '\n'.join(map(lambda field: f'{indent(printer.ast_to_string(field), 2)}', ast["fields"]))
    return f'struct {{ \n{field_decls_str}\n}}'


def custom_type(_printer, ast):
    """Prints int, bool, ... type."""
    return ast["type"]


def field_decl(printer, ast):
    """Prints field declaration for struct type."""
    type_str = printer.ast_to_string(ast["type"])
    var_data_str = ', '.join(map(lambda var: printer.ast_to_string(var), ast["varData"]))
    return f'{type_str} {var_data_str};'


###

def function_def(printer, ast):
    """Prints "type func_name(....) { ... }"."""
    type_str = printer.ast_to_string(ast["type"])
    name_str = ast["name"]
    params_str = ', '.join(map(lambda param: printer.ast_to_string(param), ast["params"]))
    body_str = printer.ast_to_string(ast["body"])
    return f'\n{type_str} {name_str}({params_str}) {body_str}'


def statement_block(printer, ast):
    """Prints statement block "{ ... }"."""
    decls_str = ''.join(map(lambda decl: f'{indent(printer.ast_to_string(decl), 2)}\n', ast["decls"]))
    stmts_str = ''.join(map(lambda stmt: f'{indent(printer.ast_to_string(stmt), 2)}\n', ast["stmts"]))
    return f'{{ \n{decls_str}{stmts_str}}}'


def empty_statement(_printer, _ast):
    """Prints empty statement."""
    return f';'


def expr_statement(printer, ast):
    """Prints "expr;"."""
    expr_str = printer.ast_to_string(ast["expr"])
    return f'{expr_str};'


def for_loop(printer, ast):
    """Prints "for (init; cond; after) {body}"."""
    init_str = printer.ast_to_string(ast["init"])
    cond_str = printer.ast_to_string(ast["cond"])
    after_str = printer.ast_to_string(ast["after"])
    body_str = printer.ast_to_string(ast["body"])
    return f'for ({init_str}; {cond_str}; {after_str}) {body_str}'


def iteration(printer, ast):
    """Prints "for (name : type) {body}"."""
    name_str = ast["name"]
    type_str = printer.ast_to_string(ast["type"])
    body_str = printer.ast_to_string(ast["body"])
    return f'for ({name_str} : {type_str}) {body_str}'


def while_loop(printer, ast):
    """Prints "while (cond) {body}"."""
    cond_str = printer.ast_to_string(ast["cond"])
    body_str = printer.ast_to_string(ast["body"])
    return f'while ({cond_str}) {body_str}'


def do_while_loop(printer, ast):
    """Prints "do {body} while (cond)"."""
    cond_str = printer.ast_to_string(ast["cond"])
    body_str = printer.ast_to_string(ast["body"])
    return f'do {body_str} while ({cond_str});'


def if_statement(printer, ast):
    """Prints "if (cond) {thenBody} [else {elseBody}]"."""
    cond_str = printer.ast_to_string(ast["cond"])
    then_body_str = printer.ast_to_string(ast["thenBody"])
    else_body_str = f'else {printer.ast_to_string(ast["elseBody"])}' if ast.get("elseBody") else ''
    return f'if ({cond_str}) {then_body_str} {else_body_str}'


def return_statement(printer, ast):
    """Prints "return expr;"."""
    expr_str = printer.ast_to_string(ast["expr"])
    return f'return {expr_str};'


###

def parameter(printer, ast):
    """Prints a function parameter."""
    type_str = printer.ast_to_string(ast["type"])
    is_ref_str = '&' if ast["isRef"] else ''
    var_data_str = printer.ast_to_string(ast["varData"])
    return f'{type_str} {is_ref_str}{var_data_str}'


def system(_printer, ast):
    """Prints the instance system initialization."""
    process_names_str = ' < '.join(map(lambda proc_block: ', '.join(proc_block), ast["processNames"]))
    return f'system {process_names_str};'


def process(printer, ast):
    """Prints a single process."""
    func_name_str = ast["name"]
    args_str = ', '.join(map(lambda arg: printer.ast_to_string(arg), ast["args"]))
    return f'{func_name_str}({args_str})'


def instantiation(printer, ast):
    """Prints "Inst(params) = Tmpl(args)"."""
    instance_name_str = ast["instanceName"]
    if ast.get("params"):
        params_str = f'({", ".join(map(lambda param: printer.ast_to_string(param), ast["params"]))})'
    else:
        params_str = ''
    template_name_str = ast["templateName"]
    args_str = ', '.join(map(lambda arg: printer.ast_to_string(arg), ast["args"]))
    return f'{instance_name_str}{params_str} = {template_name_str}({args_str});'


# def progress_decl(printer, ast):
#     exprs_str = ' '.join(map(lambda expr: f'{printer.ast_to_string(expr)};', ast["exprs"]))
#     return f'{{ {exprs_str} }}'


###

# def gantt_decl(_printer, _ast):
#     return ''
#
#
# def gantt_def(_printer, _ast):
#     return ''
#
#
# def gantt_args(_printer, _ast):
#     return ''
#
#
# def gantt_entry_elem(_printer, _ast):
#     return ''
#
#
# def gantt_decl_select(_printer, _ast):
#     return ''
#
#
# def gantt_expr_list(_printer, _ast):
#     return ''
#
#
# def gantt_expr_single(_printer, _ast):
#     return ''
#
#
# def gantt_expr_select(_printer, _ast):
#     return ''
#
#
# def gantt_entry_select(_printer, _ast):
#     return ''


###

def chan_priority(printer, ast):
    """Prints a channel priority."""
    chan_block_strs = []
    for chan_block in ast["channels"]:
        chan_block_str = ', '.join(map(lambda chan: printer.ast_to_string(chan), chan_block))
        chan_block_strs.append(chan_block_str)
    channels_str = ' < '.join(chan_block_strs)
    return f'chan priority {channels_str};'


def chan_expr(printer, ast):
    """Prints a channel expression."""
    name_str = ast["name"]
    exprs_str = ''.join(map(lambda index: f'[{printer.ast_to_string(index)}]', ast["indices"]))
    return f'{name_str}{exprs_str}'


def chan_default(_printer, _ast):
    """Prints the default channel."""
    return f'default'


###

def variable(_printer, ast):
    """Prints a variable in an expression."""
    name_str = ast["name"]
    return f'{name_str}'


def integer(_printer, ast):
    """Prints an integer value."""
    return f'{ast["val"]}'


def double(_printer, ast):
    """Prints a double value."""
    return f'{ast["val"]}.0' if isinstance(ast["val"], int) else f'{ast["val"]}'


def boolean(_printer, ast):
    """Prints a boolean value."""
    return f'{"true" if ast["val"] else "false"}'


###

def bracket_expr(printer, ast):
    """Prints expression "(expr)"."""
    expr_str = printer.ast_to_string(ast["expr"])
    return f'({expr_str})'


def derivative_expr(printer, ast):
    """Prints expression "expr'"."""
    expr_str = printer.ast_to_string(ast["expr"])
    return f"{expr_str}'"


def post_incr_assign_expr(printer, ast):
    """Prints expression "expr++"."""
    expr_str = printer.ast_to_string(ast["expr"])
    return f'{expr_str}++'


def post_decr_assign_expr(printer, ast):
    """Prints expression "expr--"."""
    expr_str = printer.ast_to_string(ast["expr"])
    return f'{expr_str}--'


def pre_incr_assign_expr(printer, ast):
    """Prints expression "++expr"."""
    expr_str = printer.ast_to_string(ast["expr"])
    return f'++{expr_str}'


def pre_decr_assign_expr(printer, ast):
    """Prints expression "--expr"."""
    expr_str = printer.ast_to_string(ast["expr"])
    return f'--{expr_str}'


def assign_expr(printer, ast):
    """Prints expression "var = expr"."""
    return assign_to_string_funcs[ast["op"]](printer, ast)


def func_call_expr(printer, ast):
    """Prints expression "func(args)"."""
    func_name_str = ast["funcName"]
    args_str = ', '.join(map(lambda arg: printer.ast_to_string(arg), ast["args"]))
    return f'{func_name_str}({args_str})'


###

def unary_expr(printer, ast):
    """Prints a unary expression."""
    return unary_to_string_funcs[ast["op"]](printer, ast)


def binary_expr(printer, ast):
    """Prints a binary expression."""
    return binary_to_string_funcs[ast["op"]](printer, ast)


def ternary_expr(printer, ast):
    """Prints a ternary expression."""
    cond_str = printer.ast_to_string(ast["left"])  # printer.ast_to_string(ast["cond"])
    then_expr_str = printer.ast_to_string(ast["middle"])  # printer.ast_to_string(ast["thenExpr"])
    else_expr_str = printer.ast_to_string(ast["right"])  # printer.ast_to_string(ast["elseExpr"])
    return f'{cond_str} ? {then_expr_str} : {else_expr_str}'


def deadlock_expr(_printer, _ast):
    """Prints a deadlock expression."""
    return f'deadlock'


###

def for_all_expr(printer, ast):
    """Prints expression "forall (name:type) expr"."""
    var_name_str = ast["varName"]
    type_str = printer.ast_to_string(ast["type"])
    expr_str = printer.ast_to_string(ast["expr"])
    return f'forall ({var_name_str} : {type_str}) {expr_str}'


def exists_expr(printer, ast):
    """Prints expression "exists (name:type) expr"."""
    var_name_str = ast["varName"]
    type_str = printer.ast_to_string(ast["type"])
    expr_str = printer.ast_to_string(ast["expr"])
    return f'exists ({var_name_str} : {type_str}) {expr_str}'


def sum_expr(printer, ast):
    """Prints expression "sum (name:type) expr"."""
    var_name_str = ast["varName"]
    type_str = printer.ast_to_string(ast["type"])
    expr_str = printer.ast_to_string(ast["expr"])
    return f'sum ({var_name_str} : {type_str}) {expr_str}'


###

def invariant(printer, ast):
    """Prints an invariant "ti - tj <= c"."""
    expr_str = printer.ast_to_string(ast["expr"])
    return f'{expr_str}'


def select(printer, ast):
    """Prints a select statement "name : type"."""
    name_str = ast["name"]
    type_str = printer.ast_to_string(ast["type"])
    return f'{name_str} : {type_str}'


def guard(printer, ast):
    """Prints a guard "ti - tj <= c"."""
    expr_str = printer.ast_to_string(ast["expr"])
    return f'{expr_str}'


def sync(printer, ast):
    """Prints a synchronization "chan(!|?)"."""
    channel_str = printer.ast_to_string(ast["channel"])
    op_str = ast["op"]
    return f'{channel_str}{op_str}'


def update(printer, ast):
    """Prints an update "var = expr" or "func()"."""
    expr_str = printer.ast_to_string(ast["expr"])
    return f'{expr_str}'


################################
# Function Lookup Dictionaries #
################################

unary_to_string_funcs = {
    "Plus": plus,
    "Minus": minus,
    "LogNot": log_not,

}

binary_to_string_funcs = {
    "Dot": dot,
    "ArrayAccess": array_access,

    "Add": add,
    "Sub": sub,
    "Mult": mult,
    "Div": div,
    "Mod": mod,
    "LShift": l_shift,
    "RShift": r_shift,

    "LogAnd": log_and,
    "LogOr": log_or,
    "LogImply": log_imply,
    "BitAnd": bit_and,
    "BitOr": bit_or,
    "BitXor": bit_xor,

    "Minimum": minimum,
    "Maximum": maximum,
    "GreaterEqual": greater_equal,
    "GreaterThan": greater_than,
    "LessEqual": less_equal,
    "LessThan": less_than,
    "Equal": equal,
    "NotEqual": not_equal,
}

assign_to_string_funcs = {
    "Assign": assign,
    "AddAssign": add_assign,
    "SubAssign": sub_assign,
    "MultAssign": mult_assign,
    "DivAssign": div_assign,
    "ModAssign": mod_assign,
    "LShiftAssign": l_shift_assign,
    "RShiftAssign": r_shift_assign,
    "BitAndAssign": bit_and_assign,
    "BitOrAssign": bit_or_assign,
    "BitXorAssign": bit_xor_assign,
}

to_string_funcs = {
    "UppaalDeclaration": uppaal_declaration,
    "UppaalSystemDeclaration": uppaal_system_declaration,

    # "LineComment": line_comment,
    # "BlockComment": block_comment,

    "VariableDecls": variable_decls,
    "VariableID": variable_id,
    "InitialiserArray": initialiser_array,
    "TypeDecls": type_decls,

    "Type": type_,
    "BoundedIntType": bounded_int_type,
    "ScalarType": scalar_type,
    "StructType": struct_type,
    "CustomType": custom_type,
    "FieldDecl": field_decl,

    "FunctionDef": function_def,
    "StatementBlock": statement_block,
    "EmptyStatement": empty_statement,
    "ExprStatement": expr_statement,
    "ForLoop": for_loop,
    "Iteration": iteration,
    "WhileLoop": while_loop,
    "DoWhileLoop": do_while_loop,
    "IfStatement": if_statement,
    "ReturnStatement": return_statement,

    "Parameter": parameter,
    "System": system,
    "Process": process,
    "Instantiation": instantiation,
    # "ProgressDecl": progress_decl,

    # "GanttDecl": gantt_decl,
    # "GanttDef": gantt_def,
    # "GanttArgs": gantt_args,
    # "GanttEntryElem": gantt_entry_elem,
    # "GanttDeclSelect": gantt_decl_select,
    # "GanttExprList": gantt_expr_list,
    # "GanttExprSingle": gantt_expr_single,
    # "GanttExprSelect": gantt_expr_select,
    # "GanttEntrySelect": gantt_entry_select,

    # "ChanPriority": chan_priority,
    # "ChanExpr": chan_expr,
    # "ChanDefault": chan_default,

    "Variable": variable,
    "Integer": integer,
    "Double": double,
    "Boolean": boolean,

    "BracketExpr": bracket_expr,
    "DerivativeExpr": derivative_expr,
    "PostIncrAssignExpr": post_incr_assign_expr,
    "PostDecrAssignExpr": post_decr_assign_expr,
    "PreIncrAssignExpr": pre_incr_assign_expr,
    "PreDecrAssignExpr": pre_decr_assign_expr,
    "AssignExpr": assign_expr,
    "FuncCallExpr": func_call_expr,

    "UnaryExpr": unary_expr,
    "BinaryExpr": binary_expr,
    "TernaryExpr": ternary_expr,
    "DeadlockExpr": deadlock_expr,

    "ForAllExpr": for_all_expr,
    "ExistsExpr": exists_expr,
    "SumExpr": sum_expr,

    "Invariant": invariant,
    "Select": select,
    "Guard": guard,
    "Sync": sync,
    "Update": update,
}
