import pprint

import pytest
from uppyyl_simulator.backend.ast.parsers.generated.uppaal_c_language_parser import (
    UppaalCLanguageParser
)

from uppyyl_simulator.backend.ast.evaluators.uppaal_c_evaluator import UppaalCEvaluator
from uppyyl_simulator.backend.ast.parsers.uppaal_c_language_semantics import (
    UppaalCLanguageSemantics
)
from uppyyl_simulator.backend.data_structures.state.system_state import SystemState
from uppyyl_simulator.backend.data_structures.state.variable import UppaalVariable
from uppyyl_simulator.backend.data_structures.types.array import UppaalArray
from uppyyl_simulator.backend.data_structures.types.bool import UppaalBool
from uppyyl_simulator.backend.data_structures.types.function import UppaalFunction
from uppyyl_simulator.backend.data_structures.types.int import UppaalInt
from uppyyl_simulator.backend.data_structures.types.struct import UppaalStruct
from uppyyl_simulator.backend.data_structures.types.void import UppaalVoid
from tests.ast.uppaal_c_language_test_data import (
    test_expr_data, test_statement_data, test_return_statement_data, test_assign_data, test_declaration_data,
    test_system_declaration_data
)

pp = pprint.PrettyPrinter(indent=4, compact=True)
printExpectedResults = False
printActualResults = False

# Type definitions
array_1d_type = UppaalArray.make_new_type(name="array", dims=[10], clazz=UppaalInt)
array_2d_type = UppaalArray.make_new_type(name="array", dims=[3, 3], clazz=UppaalInt)
substruct_type = UppaalStruct.make_new_type(name="substruct", field_classes=[
    ("subval1", UppaalInt),
    ("subval2", UppaalInt),
])
struct_type = UppaalStruct.make_new_type(name="struct", field_classes=[
    ("val1", UppaalInt),
    ("val2", substruct_type)
])


@pytest.fixture
def parser():
    return UppaalCLanguageParser(semantics=UppaalCLanguageSemantics())


@pytest.fixture
def evaluator():
    return UppaalCEvaluator()


@pytest.fixture
def empty_state():
    return SystemState()


@pytest.fixture
def template_state(evaluator):
    state = SystemState()
    state.add(key="i1", var=UppaalVariable(name="i1", val=UppaalInt(5)))
    state.add(key="i2", var=UppaalVariable(name="i2", val=UppaalInt(7)))
    state.add(key="i3", var=UppaalVariable(name="i3", val=UppaalInt(9)))
    state.add(key="b_true", var=UppaalVariable(name="b1", val=UppaalBool(True)))
    state.add(key="b_false", var=UppaalVariable(name="b2", val=UppaalBool(False)))

    array_1d_val = array_1d_type(init=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
    state.add(key="arr_1d", var=UppaalVariable(name="arr_1d", val=array_1d_val))
    array_2d_val = array_2d_type(init=[[1, 2, 3], [4, 5, 6], [7, 8, 9]])
    state.add(key="arr_2d", var=UppaalVariable(name="arr_2d", val=array_2d_val))

    struct_val = struct_type(init=[10, [20, 30]])
    state.add(key="s", var=UppaalVariable(name="s", val=struct_val))

    func_ast = {
        'astType': 'FunctionDef',
        'body': {'astType': 'StatementBlock', 'decls': [], 'stmts': []},
        'name': 'func',
        'params': []
    }
    func = UppaalFunction(name="f", func_ast=func_ast, return_clazz=UppaalVoid, c_evaluator=evaluator)
    state.add(key="f", var=func, const=True)
    return state


def test_template_state(template_state):
    scope = template_state.program_state["variable"]["system"]

    assert "i1" in scope
    i1_val = scope["i1"].val
    assert isinstance(i1_val, UppaalInt)
    assert i1_val == UppaalInt(5)

    assert "i2" in scope
    i2_val = scope["i2"].val
    assert isinstance(i2_val, UppaalInt)
    assert i2_val == UppaalInt(7)

    assert "i3" in scope
    i3_val = scope["i3"].val
    assert isinstance(i3_val, UppaalInt)
    assert i3_val == UppaalInt(9)

    assert "arr_1d" in scope
    arr_1d_val = scope["arr_1d"].val
    assert isinstance(arr_1d_val, UppaalArray)
    assert arr_1d_val.get_raw_data() == [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

    assert "arr_2d" in scope
    arr_2d_val = scope["arr_2d"].val
    assert isinstance(arr_2d_val, UppaalArray)
    assert arr_2d_val.get_raw_data() == [[1, 2, 3], [4, 5, 6], [7, 8, 9]]

    assert "s" in scope
    struct_val = scope["s"].val
    assert isinstance(struct_val, UppaalStruct)
    assert struct_val.get_raw_data() == {
        "val1": 10,
        "val2": {
            "subval1": 20,
            "subval2": 30}}


###########
# General #
###########
def test_none_input(evaluator):
    with pytest.raises(Exception):
        evaluator.eval_ast(ast=None, state=None)


def test_list_input(evaluator):
    state = SystemState()
    evaluator.eval_ast(ast=[{'astType': 'Integer', 'val': 1}], state=state)


def test_unknown_ast_type(evaluator):
    test_data = {
        "info": "Dummy AST",
        "input": {'astType': 'NonExistingType'},
    }
    with pytest.raises(Exception):
        evaluator.eval_ast(ast=test_data["input"], state=SystemState())


def test_do_log_details(evaluator):
    test_data = {
        "info": "Dummy AST",
        "input": {'astType': 'Integer', 'val': 1},
    }
    evaluator.do_log_details = True
    evaluator.eval_ast(ast=test_data["input"], state=SystemState())


def test_initialize_parameters_1(template_state, evaluator, parser):
    test_data = {
        "input": {
            "params": ['int a', 'int &b'],
            "args": ['1', 'i1']
        },
    }
    state = template_state
    param_asts = list(map(lambda p: parser.parse(text=p, rule_name="Parameter"), test_data["input"]["params"]))
    arg_asts = list(map(lambda p: parser.parse(text=p, rule_name="Expression"), test_data["input"]["args"]))
    args = list(map(lambda arg_ast: evaluator.eval_ast(ast=arg_ast, state=state), arg_asts))
    evaluator.initialize_parameters(param_asts=param_asts, args=args, state=state)

    raw_variable_state = state.get_compact_variable_state()
    expected = {
        "i1": 5,
        "a": 1,
        "b": 5,
    }
    for key, val in expected.items():
        assert raw_variable_state["variable"]["system"][key] == val


def test_initialize_parameters_2(parser, evaluator):
    test_data = {
        "info": "Initialize unsupported parameters",
        "input": {
            "params": ['int a', 'int &b'],
            "args": ['1', '2']
        },
    }
    state = SystemState()
    param_asts = list(map(lambda p: parser.parse(text=p, rule_name="Parameter"), test_data["input"]["params"]))
    arg_asts = list(map(lambda p: parser.parse(text=p, rule_name="Expression"), test_data["input"]["args"]))
    args = list(map(lambda arg_ast: evaluator.eval_ast(ast=arg_ast, state=state), arg_asts))
    args[0] = None
    with pytest.raises(Exception):
        evaluator.initialize_parameters(param_asts=param_asts, args=args, state=SystemState())


###############
# Expressions #
###############
@pytest.mark.parametrize("data", test_expr_data.values(),
                         ids=list(map(lambda kv: f'{kv[0]}: {kv[1]["text"]}', test_expr_data.items())))
def test_expression(template_state, evaluator, data):
    state = template_state
    res = evaluator.eval_ast(ast=data["ast"], state=state)
    assert isinstance(res, type(data["val"]))
    assert res == data["val"]


@pytest.mark.parametrize("data", test_assign_data.values(),
                         ids=list(map(lambda kv: f'{kv[0]}: {kv[1]["text"]}', test_assign_data.items())))
def test_assign_expression(template_state, evaluator, data):
    state = template_state
    res = evaluator.eval_ast(ast=data["ast"], state=state)

    assert isinstance(res, type(data["val"]))
    assert res == data["val"]
    raw_variable_state = state.get_compact_variable_state()
    for key, val in data["res_state"].items():
        assert val == raw_variable_state["variable"]["system"][key]


################
# Declarations #
################
@pytest.mark.parametrize("data", test_declaration_data.values(),
                         ids=list(map(lambda kv: f'{kv[0]}: {kv[1]["text"]}', test_declaration_data.items())))
def test_declarations(template_state, evaluator, data):
    state = template_state
    for pre in data["pre"]:
        evaluator.eval_ast(ast=pre["ast"], state=state)
    evaluator.eval_ast(ast=data["ast"], state=state)

    raw_variable_state = state.get_compact_variable_state()
    for key, val in data["res_state"].items():
        assert val == raw_variable_state["variable"]["system"][key]


##############
# Statements #
##############
@pytest.mark.parametrize("data", test_statement_data.values(),
                         ids=list(map(lambda kv: f'{kv[0]}: {kv[1]["text"]}', test_statement_data.items())))
def test_statements(template_state, evaluator, data):
    state = template_state
    for pre in data["pre"]:
        evaluator.eval_ast(ast=pre["ast"], state=state)
    res, ret_status = evaluator.eval_ast(ast=data["ast"], state=state)

    assert not ret_status
    raw_variable_state = state.get_compact_variable_state()
    for key, val in data["res_state"].items():
        assert val == raw_variable_state["variable"]["system"][key]


@pytest.mark.parametrize("data", test_return_statement_data.values(),
                         ids=list(map(lambda kv: f'{kv[0]}: {kv[1]["text"]}', test_return_statement_data.items())))
def test_return_statements(template_state, evaluator, data):
    state = template_state
    for pre in data["pre"]:
        evaluator.eval_ast(ast=pre["ast"], state=state)
    res, ret_status = evaluator.eval_ast(ast=data["ast"], state=state)

    assert ret_status
    raw_variable_state = state.get_compact_variable_state()
    for key, val in data["res_state"].items():
        assert val == raw_variable_state["variable"]["system"][key]


######################
# System Declaration #
######################
@pytest.mark.parametrize("data", test_system_declaration_data.values(),
                         ids=list(map(lambda kv: f'{kv[0]}: {kv[1]["text"]}', test_system_declaration_data.items())))
def test_system_declarations(template_state, evaluator, data):
    state = template_state
    evaluator.eval_ast(ast=data["ast"], state=state)
    # TODO: Check results
