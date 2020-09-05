import pprint

import pytest
from uppyyl_simulator.backend.ast.printers.uppaal_c_language_printer import UppaalCPrinter
from tests.ast.uppaal_c_language_test_data import (
    test_expr_data, test_statement_data, test_return_statement_data, test_assign_data, test_declaration_data,
    test_system_declaration_data
)

pp = pprint.PrettyPrinter(indent=4, compact=True)
printExpectedResults = False
printActualResults = False


@pytest.fixture
def printer():
    return UppaalCPrinter()


###############
# Expressions #
###############
@pytest.mark.parametrize("data", test_expr_data.values(),
                         ids=list(map(lambda kv: f'{kv[0]}: {kv[1]["text"]}', test_expr_data.items())))
def test_expression(printer, data):
    res = printer.ast_to_string(ast=data["ast"])
    res_without_whitespace = ''.join(res.split())
    expected_without_whitespace = ''.join(data["text"].split())
    assert res_without_whitespace == expected_without_whitespace


@pytest.mark.parametrize("data", test_assign_data.values(),
                         ids=list(map(lambda kv: f'{kv[0]}: {kv[1]["text"]}', test_assign_data.items())))
def test_assign_expression(printer, data):
    res = printer.ast_to_string(ast=data["ast"])
    res_without_whitespace = ''.join(res.split())
    expected_without_whitespace = ''.join(data["text"].split())
    assert res_without_whitespace == expected_without_whitespace


################
# Declarations #
################
@pytest.mark.parametrize("data", test_declaration_data.values(),
                         ids=list(map(lambda kv: f'{kv[0]}: {kv[1]["text"]}', test_declaration_data.items())))
def test_declarations(printer, data):
    res = printer.ast_to_string(ast=data["ast"])
    res_without_whitespace = ''.join(res.split())
    expected_without_whitespace = ''.join(data["text"].split())
    assert res_without_whitespace == expected_without_whitespace


##############
# Statements #
##############
@pytest.mark.parametrize("data", test_statement_data.values(),
                         ids=list(map(lambda kv: f'{kv[0]}: {kv[1]["text"]}', test_statement_data.items())))
def test_statements(printer, data):
    res = printer.ast_to_string(ast=data["ast"])
    res_without_whitespace = ''.join(res.split())
    expected_without_whitespace = ''.join(data["text"].split())
    assert res_without_whitespace == expected_without_whitespace


@pytest.mark.parametrize("data", test_return_statement_data.values(),
                         ids=list(map(lambda kv: f'{kv[0]}: {kv[1]["text"]}', test_return_statement_data.items())))
def test_return_statements(printer, data):
    res = printer.ast_to_string(ast=data["ast"])
    res_without_whitespace = ''.join(res.split())
    expected_without_whitespace = ''.join(data["text"].split())
    assert res_without_whitespace == expected_without_whitespace


######################
# System Declaration #
######################
@pytest.mark.parametrize("data", test_system_declaration_data.values(),
                         ids=list(map(lambda kv: f'{kv[0]}: {kv[1]["text"]}', test_system_declaration_data.items())))
def test_system_declarations(printer, data):
    res = printer.ast_to_string(ast=data["ast"])
    res_without_whitespace = ''.join(res.split())
    expected_without_whitespace = ''.join(data["text"].split())
    assert res_without_whitespace == expected_without_whitespace
