"""The implementation of an evaluator for Uppaal C code ASTs."""

from uppyyl_simulator.backend.data_structures.ast.ast_code_evaluator import (
    ASTCodeEvaluator
)
from uppyyl_simulator.backend.data_structures.state.variable import UppaalVariable
from uppyyl_simulator.backend.data_structures.types.array import UppaalArray
from uppyyl_simulator.backend.data_structures.types.base import UppaalType
from uppyyl_simulator.backend.data_structures.types.bool import UppaalBool
from uppyyl_simulator.backend.data_structures.types.bounded_int import UppaalBoundedInt
from uppyyl_simulator.backend.data_structures.types.chan import UppaalChan
from uppyyl_simulator.backend.data_structures.types.clock import UppaalClock
from uppyyl_simulator.backend.data_structures.types.function import UppaalFunction
from uppyyl_simulator.backend.data_structures.types.int import UppaalInt
from uppyyl_simulator.backend.data_structures.types.reference import UppaalReference
from uppyyl_simulator.backend.data_structures.types.scalar import UppaalScalar
from uppyyl_simulator.backend.data_structures.types.struct import UppaalStruct
from uppyyl_simulator.backend.data_structures.types.void import UppaalVoid


######################
# Uppaal C Evaluator #
######################
class UppaalCEvaluator(ASTCodeEvaluator):
    """The Uppaal C code evaluator class."""

    def __init__(self, do_log_details=False):
        """Initializes UppaalCEvaluator.

        Args:
            do_log_details: Choose whether intermediate details of the evaluation should be printed.
        """
        super().__init__()
        self.do_log_details = do_log_details

    def eval_ast(self, ast, state):
        """Evaluates an AST in the context of a given system state.

        Args:
            ast: The AST that is evaluated.
            state: The system state context.

        Returns:
            The evaluation result (e.g, in case of expressions)
        """
        if ast is None or state is None:
            raise Exception("AST and state need to be defined.")

        if isinstance(ast, list):
            for elem in ast:
                self.eval_ast(ast=elem, state=state)
            return
        assert isinstance(ast, dict)

        if self.do_log_details:
            print(f'[ast_to_string] {ast["astType"]}: {list(ast.keys())}')
        if ast["astType"] in eval_funcs:
            res = eval_funcs[ast["astType"]](self, ast, state)
            if self.do_log_details:
                print(f'Result of {ast}: {res}')
            return res
        raise Exception("AST type \"" + ast["astType"] + "\" not supported by UppaalCEvaluator.")

    def initialize_parameters(self, param_asts, args, state):
        """Initializes the parameters of a template instance.

        Args:
            param_asts: A list of parameter ASTs
            args: A list of arguments.
            state: The system state context.
        """
        args = args if args else []
        assert len(args) == len(param_asts)

        for i in range(0, len(args)):
            param_ast = param_asts[i]
            param_name = param_ast["varData"]["varName"]
            arg = args[i]

            if not isinstance(arg, UppaalType) and not isinstance(arg, UppaalVariable):
                raise Exception(f'Argument for parameter "{param_name}" must be '
                                f'of type UppaalType or UppaalVariable (actual type: {type(arg)}).')

            if param_ast["isRef"]:  # If variable is a reference
                ref = UppaalReference(pointee_path=(arg.scope_path + arg.var_path))
                ref.init_pointee(state.program_state)
                ref_var = UppaalVariable(name=param_name, val=ref)
                state.set(param_name, ref_var, const=False)  # ('const' in param_ast["type"]["prefixes"]))

            else:  # If variable is not a reference
                # arg = self.eval_ast(arg, state)
                self.eval_ast(param_ast, state)  # Parameter evaluation creates variable in state
                state.assign(param_name, arg)


#####################
# Unary Expressions #
#####################
def plus(evaluator, ast, state):
    """Evaluates "+expr"."""
    return +evaluator.eval_ast(ast["expr"], state)


def minus(evaluator, ast, state):
    """Evaluates "-expr"."""
    return -evaluator.eval_ast(ast["expr"], state)


def log_not(evaluator, ast, state):
    """Evaluates "!expr"."""
    # Explicit UppaalBool required as "not" cannot be overridden for UppaalBool in Python
    return UppaalBool(not evaluator.eval_ast(ast["expr"], state))


######################
# Binary Expressions #
######################
def dot(evaluator, ast, state):
    """Evaluates "left.right"."""
    left = evaluator.eval_ast(ast["left"], state)
    right = ast["right"]["name"]
    # if isinstance(left, UppaalVariable):
    #     res = left.val[right]
    # else:
    res = left[right]
    return res


def array_access(evaluator, ast, state):
    """Evaluates "left[right]"."""
    left = evaluator.eval_ast(ast["left"], state)
    right = int(evaluator.eval_ast(ast["right"], state))
    # if isinstance(left, UppaalVariable):
    #     res = left.val[right]
    # else:
    res = left[right]
    return res


###

def add(evaluator, ast, state):
    """Evaluates "left + right"."""
    res = evaluator.eval_ast(ast["left"], state) + evaluator.eval_ast(ast["right"], state)
    return res


def sub(evaluator, ast, state):
    """Evaluates "left - right"."""
    res = evaluator.eval_ast(ast["left"], state) - evaluator.eval_ast(ast["right"], state)
    return res


def mult(evaluator, ast, state):
    """Evaluates "left * right"."""
    res = evaluator.eval_ast(ast["left"], state) * evaluator.eval_ast(ast["right"], state)
    return res


def div(evaluator, ast, state):
    """Evaluates "left / right"."""
    res = evaluator.eval_ast(ast["left"], state) / evaluator.eval_ast(ast["right"], state)
    return res


def mod(evaluator, ast, state):
    """Evaluates "left % right"."""
    res = evaluator.eval_ast(ast["left"], state) % evaluator.eval_ast(ast["right"], state)
    return res


def l_shift(evaluator, ast, state):
    """Evaluates "left << right"."""
    res = evaluator.eval_ast(ast["left"], state) << evaluator.eval_ast(ast["right"], state)
    return res


def r_shift(evaluator, ast, state):
    """Evaluates "left >> right"."""
    res = evaluator.eval_ast(ast["left"], state) >> evaluator.eval_ast(ast["right"], state)
    return res


###

def log_and(evaluator, ast, state):
    """Evaluates "left && right"."""
    # Explicit UppaalBool required as "and" cannot be overridden for UppaalBool in Python
    res = UppaalBool(evaluator.eval_ast(ast["left"], state) and evaluator.eval_ast(ast["right"], state))
    return res


def log_or(evaluator, ast, state):
    """Evaluates "left || right"."""
    # Explicit UppaalBool required as "or" cannot be overridden for UppaalBool in Python
    res = UppaalBool(evaluator.eval_ast(ast["left"], state) or evaluator.eval_ast(ast["right"], state))
    return res


def log_imply(evaluator, ast, state):
    """Evaluates "left imply right"."""
    # Explicit UppaalBool required as "or" and "not" cannot be overridden for UppaalBool in Python
    res = UppaalBool((evaluator.eval_ast(ast["right"], state)) or not (evaluator.eval_ast(ast["left"], state)))
    return res


def bit_and(evaluator, ast, state):
    """Evaluates "left & right"."""
    res = evaluator.eval_ast(ast["left"], state) & evaluator.eval_ast(ast["right"], state)
    return res


def bit_or(evaluator, ast, state):
    """Evaluates "left | right"."""
    res = evaluator.eval_ast(ast["left"], state) | evaluator.eval_ast(ast["right"], state)
    return res


def bit_xor(evaluator, ast, state):
    """Evaluates "left ^ right"."""
    res = evaluator.eval_ast(ast["left"], state) ^ evaluator.eval_ast(ast["right"], state)
    return res


###

def minimum(evaluator, ast, state):
    """Evaluates "min(left, right)"."""
    res = min(evaluator.eval_ast(ast["left"], state), evaluator.eval_ast(ast["right"], state))
    return res


def maximum(evaluator, ast, state):
    """Evaluates "max(left, right)"."""
    res = max(evaluator.eval_ast(ast["left"], state), evaluator.eval_ast(ast["right"], state))
    return res


def greater_equal(evaluator, ast, state):
    """Evaluates "left >= right"."""
    res = UppaalBool(evaluator.eval_ast(ast["left"], state) >= evaluator.eval_ast(ast["right"], state))
    return res


def greater_than(evaluator, ast, state):
    """Evaluates "left > right"."""
    res = UppaalBool(evaluator.eval_ast(ast["left"], state) > evaluator.eval_ast(ast["right"], state))
    return res


def less_equal(evaluator, ast, state):
    """Evaluates "left <= right"."""
    res = UppaalBool(evaluator.eval_ast(ast["left"], state) <= evaluator.eval_ast(ast["right"], state))
    return res


def less_than(evaluator, ast, state):
    """Evaluates "left < right"."""
    res = UppaalBool(evaluator.eval_ast(ast["left"], state) < evaluator.eval_ast(ast["right"], state))
    return res


def equal(evaluator, ast, state):
    """Evaluates "left == right"."""
    res = UppaalBool(evaluator.eval_ast(ast["left"], state) == evaluator.eval_ast(ast["right"], state))
    return res


def not_equal(evaluator, ast, state):
    """Evaluates "left != right"."""
    res = UppaalBool(evaluator.eval_ast(ast["left"], state) != evaluator.eval_ast(ast["right"], state))
    return res


###

def assign(evaluator, ast, state):
    """Evaluates "left = right"."""
    var = evaluator.eval_ast(ast["left"], state)
    val = evaluator.eval_ast(ast["right"], state)
    var.assign(val)
    return var.val


def add_assign(evaluator, ast, state):
    """Evaluates "left += right"."""
    var = evaluator.eval_ast(ast["left"], state)
    val = evaluator.eval_ast(ast["right"], state)
    var += val
    return var.val


def sub_assign(evaluator, ast, state):
    """Evaluates "left -= right"."""
    var = evaluator.eval_ast(ast["left"], state)
    val = evaluator.eval_ast(ast["right"], state)
    var -= val
    return var.val


def mult_assign(evaluator, ast, state):
    """Evaluates "left *= right"."""
    var = evaluator.eval_ast(ast["left"], state)
    val = evaluator.eval_ast(ast["right"], state)
    var *= val
    return var.val


def div_assign(evaluator, ast, state):
    """Evaluates "left /= right"."""
    var = evaluator.eval_ast(ast["left"], state)
    val = evaluator.eval_ast(ast["right"], state)
    var /= val
    return var.val


def mod_assign(evaluator, ast, state):
    """Evaluates "left %= right"."""
    var = evaluator.eval_ast(ast["left"], state)
    val = evaluator.eval_ast(ast["right"], state)
    var %= val
    return var.val


def l_shift_assign(evaluator, ast, state):
    """Evaluates "left <<= right"."""
    var = evaluator.eval_ast(ast["left"], state)
    val = evaluator.eval_ast(ast["right"], state)
    var <<= val
    return var.val


def r_shift_assign(evaluator, ast, state):
    """Evaluates "left >>= right"."""
    var = evaluator.eval_ast(ast["left"], state)
    val = evaluator.eval_ast(ast["right"], state)
    var >>= val
    return var.val


def bit_and_assign(evaluator, ast, state):
    """Evaluates "left &= right"."""
    var = evaluator.eval_ast(ast["left"], state)
    val = evaluator.eval_ast(ast["right"], state)
    var &= val
    return var.val


def bit_or_assign(evaluator, ast, state):
    """Evaluates "left |= right"."""
    var = evaluator.eval_ast(ast["left"], state)
    val = evaluator.eval_ast(ast["right"], state)
    var |= val
    return var.val


def bit_xor_assign(evaluator, ast, state):
    """Evaluates "left ^= right"."""
    var = evaluator.eval_ast(ast["left"], state)
    val = evaluator.eval_ast(ast["right"], state)
    var ^= val
    return var.val


##########
# Others #
##########
def uppaal_declaration(evaluator, ast, state):
    """Evaluates the Uppaal declaration."""
    for decl_ast in ast["decls"]:
        evaluator.eval_ast(decl_ast, state)


def uppaal_system_declaration(evaluator, ast, state):
    """Evaluates the Uppaal system declaration."""
    inst_data = {}
    for decl_ast in ast["decls"]:
        res = evaluator.eval_ast(decl_ast, state)
        if decl_ast["astType"] == "Instantiation":
            inst_data[res["instance_name"]] = res
    system_instances = evaluator.eval_ast(ast["systemDecl"], state)
    return {"system_instances": system_instances, "instance_data": inst_data}


###

# def empty_line(evaluator, ast, state):
#     return f'\n'

# def line_comment(_evaluator, _ast, _state):
#     return
#
#
# def block_comment(_evaluator, _ast, _state):
#     return


###

# ---

def variable_decls(evaluator, ast, state):
    """Evaluates "type varName [= initData]"."""
    prefixes, clazz = evaluator.eval_ast(ast["type"], state)
    if issubclass(clazz, UppaalVoid):
        return
    for var_ast in ast["varData"]:
        var_clazz = clazz
        var_id_data = evaluator.eval_ast(var_ast, state)
        var_name = var_id_data["varName"]

        array_dims = var_id_data["arrayDecl"]
        if len(array_dims) > 0:
            var_clazz = UppaalArray.make_new_type(name="array", dims=array_dims, clazz=var_clazz)

        # Create new value and variable object
        new_val = var_clazz()
        new_var = UppaalVariable(name=None, val=new_val)

        # Add variable object to program state (and optionally set initial values)
        if issubclass(clazz, UppaalClock):
            state.add(var_name, new_var, const=True)
        elif issubclass(clazz, UppaalChan):
            state.add(var_name, new_var, const=True)
        else:
            if var_id_data["initData"] is not None:
                new_val.assign(var_id_data["initData"])
            state.add(var_name, new_var, const=("const" in prefixes or "meta" in prefixes))


# ---

def variable_id(evaluator, ast, state):
    """Evaluates "varName [= initData]"."""
    var_name = ast["varName"]
    array_decl = list(map(lambda decl: evaluator.eval_ast(decl, state), ast["arrayDecl"]))
    init_data = evaluator.eval_ast(ast["initData"], state) if ast.get("initData") else None
    return {"varName": var_name, "arrayDecl": array_decl, "initData": init_data}


def initialiser_array(evaluator, ast, state):
    """Evaluates initial values "= { ... }"."""
    vals = list(map(lambda var: evaluator.eval_ast(var, state), ast["vals"]))
    return vals


def type_decls(evaluator, ast, state):
    """Evaluates "typedef ..."."""
    prefixes, clazz = evaluator.eval_ast(ast["type"], state)
    for name_ast in ast["names"]:
        var_name = name_ast["varName"]
        uppaal_clazz_name = f'{var_name}'  # f'Uppaal_{var_name}'
        new_clazz = type(uppaal_clazz_name, (clazz,), {})
        state.add(uppaal_clazz_name, new_clazz, const=True)


###

def type_(evaluator, ast, state):
    """Evaluates "[const|meta|...] type"."""
    prefixes = ast["prefixes"]
    clazz = evaluator.eval_ast(ast["typeId"], state)
    clazz.const = "const" in prefixes  # TODO: Implement another concept to handle type quantifiers
    clazz.meta = "meta" in prefixes
    clazz.broadcast = "broadcast" in prefixes
    clazz.urgent = "urgent" in prefixes
    return prefixes, clazz


def bounded_int_type(evaluator, ast, state):
    """Evaluates "int[a,b]"."""
    uppaal_clazz_name = f'bounded_int'  # f'Uppaal_bounded_int'
    lower_val = evaluator.eval_ast(ast["lower"], state)
    upper_val = evaluator.eval_ast(ast["upper"], state)

    new_clazz = UppaalBoundedInt.make_new_type(name=uppaal_clazz_name, bounds=(lower_val, upper_val))
    return new_clazz


def scalar_type(evaluator, ast, state):
    """Evaluates "scalar[n]"."""
    uppaal_clazz_name = f'scalar'  # f'Uppaal_scalar'
    size = evaluator.eval_ast(ast["expr"], state)

    new_clazz = UppaalScalar.make_new_type(name=uppaal_clazz_name, size=size)
    return new_clazz


def struct_type(evaluator, ast, state):
    """Evaluates "struct {...}"."""
    uppaal_clazz_name = f'struct'  # f'Uppaal_struct'
    field_classes = []
    for field_ast in ast["fields"]:
        field_vars_data = evaluator.eval_ast(field_ast, state)
        field_classes.extend(field_vars_data)

    new_clazz = UppaalStruct.make_new_type(name=uppaal_clazz_name, field_classes=field_classes)
    return new_clazz


def custom_type(_evaluator, ast, state):
    """Evaluates int, bool, ... type."""
    custom_type_name = ast["type"]
    base_clazz_name = f'{custom_type_name}'  # f'Uppaal_{custom_type_name}'
    base_clazz = state.get(base_clazz_name)

    # TODO: Implement another concept to handle type quantifiers (so that copying classes each time is not required)
    # new_clazz = base_clazz.make_new_type(name=base_clazz_name)
    new_clazz = type(base_clazz_name, (base_clazz,), {})

    return new_clazz  # base_clazz


def field_decl(evaluator, ast, state):
    """Evaluates field declaration for struct type."""
    prefixes, clazz = evaluator.eval_ast(ast["type"], state)
    variables = []
    for var in ast["varData"]:
        variable_id_data = evaluator.eval_ast(var, state)
        var_name = variable_id_data["varName"]

        array_dims = variable_id_data["arrayDecl"]
        if len(array_dims) > 0:
            clazz = UppaalArray.make_new_type(name="array", dims=array_dims, clazz=clazz)

        variables.append((var_name, clazz))
    return variables


###

def function_def(evaluator, ast, state):
    """Evaluates "type func_name(....) { ... }"."""
    func_name = ast["name"]
    prefixes, clazz = evaluator.eval_ast(ast["type"], state)
    func_obj = UppaalFunction(func_name, ast, clazz, evaluator)
    state.add(func_name, func_obj, const=True)


def statement_block(evaluator, ast, state):
    """Evaluates statement block "{ ... }"."""
    state.new_local_scope()
    for decl in ast["decls"]:
        evaluator.eval_ast(decl, state)
    for stmt in ast["stmts"]:
        res, do_return = evaluator.eval_ast(stmt, state)
        if do_return:
            state.remove_local_scope()
            return res, True
    state.remove_local_scope()
    return None, False


def empty_statement(_evaluator, _ast, _state):
    """Evaluates empty statement."""
    return None, False


def expr_statement(evaluator, ast, state):
    """Evaluates "expr;"."""
    res = evaluator.eval_ast(ast["expr"], state)
    return res, False


def for_loop(evaluator, ast, state):
    """Evaluates "for (init; cond; after) {body}"."""
    evaluator.eval_ast(ast["init"], state)
    while evaluator.eval_ast(ast["cond"], state):
        res, do_return = evaluator.eval_ast(ast["body"], state)
        if do_return:
            return res, True
        evaluator.eval_ast(ast["after"], state)
    return None, False


def iteration(evaluator, ast, state):
    """Evaluates "for (name : type) {body}"."""
    var_name = ast["name"]
    prefixes, clazz = evaluator.eval_ast(ast["type"], state)

    state.new_local_scope()
    state.define(var_name, clazz)
    for val in clazz:
        state.assign(var_name, val)
        res, do_return = evaluator.eval_ast(ast["body"], state)
        if do_return:
            return res, True
    state.remove_local_scope()
    return None, False


def while_loop(evaluator, ast, state):
    """Evaluates "while (cond) {body}"."""
    while evaluator.eval_ast(ast["cond"], state):
        res, do_return = evaluator.eval_ast(ast["body"], state)
        if do_return:
            return res, True
    return None, False


def do_while_loop(evaluator, ast, state):
    """Evaluates "do {body} while (cond)"."""
    while True:
        res, do_return = evaluator.eval_ast(ast["body"], state)
        if do_return:
            return res, True
        if not evaluator.eval_ast(ast["cond"], state):
            break
    return None, False


def if_statement(evaluator, ast, state):
    """Evaluates "if (cond) {thenBody} [else {elseBody}]"."""
    if evaluator.eval_ast(ast["cond"], state):
        res, do_return = evaluator.eval_ast(ast["thenBody"], state)
        if do_return:
            return res, True
    else:
        if ast.get("elseBody"):
            res, do_return = evaluator.eval_ast(ast["elseBody"], state)
            if do_return:
                return res, True
    return None, False


def return_statement(evaluator, ast, state):
    """Evaluates "return expr;"."""
    if ast.get("expr"):
        res = evaluator.eval_ast(ast["expr"], state)
    else:
        res = None
    return res, True  # Second entry represents "do_return" state, and propagates upwards through statements


###

def parameter(evaluator, ast, state):
    """Evaluates a function parameter."""
    var_ast = ast["varData"]
    var_id_data = evaluator.eval_ast(var_ast, state)
    var_name = var_id_data["varName"]

    if ast["isRef"] == '&':  # If parameter is a reference
        state.add(var_name, None)
    else:  # If parameter is NOT a reference
        prefixes, clazz = evaluator.eval_ast(ast["type"], state)
        var_clazz = clazz

        new_val = var_clazz()
        new_var = UppaalVariable(name=var_name, val=new_val)
        state.add(var_name, new_var, const=("const" in prefixes or "meta" in prefixes))


def system(_evaluator, ast, _state):
    """Evaluates the instance system initialization."""
    return ast["processNames"]  # TODO: Implementation


def process(_evaluator, ast, _state):
    """Evaluates a single process."""
    return ast  # TODO: Implementation


def instantiation(evaluator, ast, state):
    """Evaluates "Inst(params) = Tmpl(args)"."""
    instance_name = ast["instanceName"]
    if ast.get("params"):
        params = list(map(lambda param: evaluator.eval_ast(param, state), ast["params"]))
    else:
        params = []
    template_name = ast["templateName"]
    args = ast["args"]  # list(map(lambda arg: evaluator.eval_ast(arg, state), ast["args"]))
    return {"instance_name": instance_name, "params": params, "template_name": template_name,
            "args": args}


# def progress_decl(_evaluator, _ast, _state):
#     """Evaluates progress declaration."""
#     return  # TODO: Implementation


###

# def gantt_decl(_evaluator, _ast, _state):
#     return  # TODO: Implementation
#
#
# def gantt_def(_evaluator, _ast, _state):
#     return  # TODO: Implementation
#
#
# def gantt_args(_evaluator, _ast, _state):
#     return  # TODO: Implementation
#
#
# def gantt_entry_elem(_evaluator, _ast, _state):
#     return  # TODO: Implementation
#
#
# def gantt_decl_select(_evaluator, _ast, _state):
#     return  # TODO: Implementation
#
#
# def gantt_expr_list(_evaluator, _ast, _state):
#     return  # TODO: Implementation
#
#
# def gantt_expr_single(_evaluator, _ast, _state):
#     return  # TODO: Implementation
#
#
# def gantt_expr_select(_evaluator, _ast, _state):
#     return  # TODO: Implementation
#
#
# def gantt_entry_select(_evaluator, _ast, _state):
#     return  # TODO: Implementation


###

# def chan_priority(_evaluator, _ast, _state):
#     return  # TODO: Implementation
#
#
# def chan_expr(_evaluator, _ast, _state):
#     return  # TODO: Implementation
#
#
# def chan_default(_evaluator, _ast, _state):
#     return  # TODO: Implementation


###

def variable(_evaluator, ast, state):
    """Evaluates a variable in an expression."""
    name_str = ast["name"]
    var = state.get(name_str)
    if isinstance(var.val, UppaalReference):
        var = var.val.pointee
    return var


def integer(_evaluator, ast, _state):
    """Evaluates an integer value."""
    return UppaalInt(ast["val"])


def double(_evaluator, _ast, _state):
    """Evaluates a double value."""
    return  # TODO: Uppaal_double(float(ast["val"]))


def boolean(_evaluator, ast, _state):
    """Evaluates a boolean value."""
    return UppaalBool(ast["val"])


###

def bracket_expr(evaluator, ast, state):
    """Evaluates expression "(expr)"."""
    res = evaluator.eval_ast(ast["expr"], state)
    return res


def derivative_expr(_evaluator, _ast, _state):
    """Evaluates expression "expr'"."""
    return  # TODO: Implementation


def post_incr_assign_expr(evaluator, ast, state):
    """Evaluates expression "expr++"."""
    var = evaluator.eval_ast(ast["expr"], state)
    ret = var.val.copy()
    var += 1
    return ret


def post_decr_assign_expr(evaluator, ast, state):
    """Evaluates expression "expr--"."""
    var = evaluator.eval_ast(ast["expr"], state)
    ret = var.val.copy()
    var -= 1
    return ret


def pre_incr_assign_expr(evaluator, ast, state):
    """Evaluates expression "++expr"."""
    var = evaluator.eval_ast(ast["expr"], state)
    var += 1
    return var.val


def pre_decr_assign_expr(evaluator, ast, state):
    """Evaluates expression "--expr"."""
    var = evaluator.eval_ast(ast["expr"], state)
    var -= 1
    return var.val


def assign_expr(evaluator, ast, state):
    """Evaluates expression "var = expr"."""
    return assign_eval_funcs[ast["op"]](evaluator, ast, state)


def func_call_expr(evaluator, ast, state):
    """Evaluates expression "func(args)"."""
    func_name = ast["funcName"]
    func_obj = state.get(func_name)
    args = list(map(lambda arg: evaluator.eval_ast(arg, state), ast["args"]))
    res = func_obj(arg_asts=args, state=state)
    return res


###

def unary_expr(evaluator, ast, state):
    """Evaluates a unary expression."""
    res = unary_eval_funcs[ast["op"]](evaluator, ast, state)
    return res


def binary_expr(evaluator, ast, state):
    """Evaluates a binary expression."""
    res = binary_eval_funcs[ast["op"]](evaluator, ast, state)
    return res


def ternary_expr(evaluator, ast, state):
    """Evaluates a ternary expression."""
    if evaluator.eval_ast(ast["left"], state):  # evaluator.eval_ast(ast["cond"], state):
        res = evaluator.eval_ast(ast["middle"], state)  # evaluator.eval_ast(ast["thenExpr"], state)
        return res
    else:
        res = evaluator.eval_ast(ast["right"], state)  # evaluator.eval_ast(ast["elseExpr"], state)
        return res


# def deadlock_expr(_evaluator, _ast, _state):
#     """Evaluates a deadlock expression."""
#     return


###

def for_all_expr(evaluator, ast, state):
    """Evaluates expression "forall (name:type) expr"."""
    var_name = ast["varName"]
    prefixes, clazz = evaluator.eval_ast(ast["type"], state)

    state.new_local_scope()
    state.define(var_name, clazz)
    for val in clazz:
        state.assign(var_name, val)
        bool_res = evaluator.eval_ast(ast["expr"], state)
        if not bool_res:
            state.remove_local_scope()
            return UppaalBool(False)
    state.remove_local_scope()
    return UppaalBool(True)


def exists_expr(evaluator, ast, state):
    """Evaluates expression "exists (name:type) expr"."""
    var_name = ast["varName"]
    prefixes, clazz = evaluator.eval_ast(ast["type"], state)

    state.new_local_scope()
    state.define(var_name, clazz)
    for val in clazz:
        state.assign(var_name, val)
        bool_res = evaluator.eval_ast(ast["expr"], state)
        if bool_res:
            state.remove_local_scope()
            return UppaalBool(True)
    state.remove_local_scope()
    return UppaalBool(False)


def sum_expr(evaluator, ast, state):
    """Evaluates expression "sum (name:type) expr"."""
    var_name = ast["varName"]
    prefixes, clazz = evaluator.eval_ast(ast["type"], state)

    state.new_local_scope()
    state.define(var_name, clazz)
    res = UppaalInt(0)
    for val in clazz:
        state.assign(var_name, val)
        int_res = evaluator.eval_ast(ast["expr"], state)
        res += int_res
    state.remove_local_scope()
    return res


###

def invariant(_evaluator, _ast, _state):
    """Evaluates an invariant "ti - tj <= c"."""
    return  # TODO: Implementation


def select(evaluator, ast, state):
    """Evaluates a select statement "name : type"."""
    var_name = ast["name"]
    prefixes, clazz = evaluator.eval_ast(ast["type"], state)
    var = UppaalVariable(name=var_name, val=clazz())
    state.add(var_name, var)


def guard(_evaluator, _ast, _state):
    """Evaluates a guard "ti - tj <= c"."""
    return  # TODO: Implementation


def sync(_evaluator, _ast, _state):
    """Evaluates a synchronization "chan(!|?)"."""
    return  # TODO: Implementation


def update(evaluator, ast, state):
    """Evaluates an update "var = expr" or "func()"."""
    evaluator.eval_ast(ast["expr"], state)


################################
# Function Lookup Dictionaries #
################################

unary_eval_funcs = {
    "Plus": plus,
    "Minus": minus,
    "LogNot": log_not,

}

binary_eval_funcs = {
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

assign_eval_funcs = {
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

eval_funcs = {
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
    # "DeadlockExpr": deadlock_expr,

    "ForAllExpr": for_all_expr,
    "ExistsExpr": exists_expr,
    "SumExpr": sum_expr,

    "Invariant": invariant,
    "Select": select,
    "Guard": guard,
    "Sync": sync,
    "Update": update,
}
