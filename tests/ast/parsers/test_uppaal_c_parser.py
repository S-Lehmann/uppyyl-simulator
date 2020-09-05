import pprint

import pytest
from uppyyl_simulator.backend.ast.parsers.generated.uppaal_c_language_parser import (
    UppaalCLanguageParser
)
from tatsu.exceptions import ParseError

from uppyyl_simulator.backend.ast.parsers.uppaal_c_language_semantics import (
    UppaalCLanguageSemantics
)
from tests.ast.uppaal_c_language_test_data import test_expr_data, test_statement_data, test_return_statement_data, \
    test_assign_data, \
    test_declaration_data, test_system_declaration_data, all_c_language_rules

pp = pprint.PrettyPrinter(indent=4, compact=True)
printExpectedResults = False
printActualResults = False


@pytest.fixture
def parser():
    return UppaalCLanguageParser(semantics=UppaalCLanguageSemantics())


################
# Parse Errors #
################
@pytest.mark.parametrize("rule", all_c_language_rules, ids=all_c_language_rules)
def test_tatsu_parse_errors(parser, rule):
    with pytest.raises(ParseError):
        parser.parse(text="/$<--->$/", rule_name=rule)


###############
# Expressions #
###############
@pytest.mark.parametrize("data", test_expr_data.values(),
                         ids=list(map(lambda kv: f'{kv[0]}: {kv[1]["text"]}', test_expr_data.items())))
def test_expression(parser, data):
    res = parser.parse(text=data["text"], rule_name=data["rule"])
    assert res == data["ast"]


@pytest.mark.parametrize("data", test_assign_data.values(),
                         ids=list(map(lambda kv: f'{kv[0]}: {kv[1]["text"]}', test_assign_data.items())))
def test_assign_expression(parser, data):
    res = parser.parse(text=data["text"], rule_name=data["rule"])
    assert res == data["ast"]


################
# Declarations #
################
@pytest.mark.parametrize("data", test_declaration_data.values(),
                         ids=list(map(lambda kv: f'{kv[0]}: {kv[1]["text"]}', test_declaration_data.items())))
def test_declarations(parser, data):
    res = parser.parse(text=data["text"], rule_name=data["rule"])
    assert res == data["ast"]


##############
# Statements #
##############
@pytest.mark.parametrize("data", test_statement_data.values(),
                         ids=list(map(lambda kv: f'{kv[0]}: {kv[1]["text"]}', test_statement_data.items())))
def test_statements(parser, data):
    res = parser.parse(text=data["text"], rule_name=data["rule"])
    assert res == data["ast"]


@pytest.mark.parametrize("data", test_return_statement_data.values(),
                         ids=list(map(lambda kv: f'{kv[0]}: {kv[1]["text"]}', test_return_statement_data.items())))
def test_return_statements(parser, data):
    res = parser.parse(text=data["text"], rule_name=data["rule"])
    assert res == data["ast"]


######################
# System Declaration #
######################
@pytest.mark.parametrize("data", test_system_declaration_data.values(),
                         ids=list(map(lambda kv: f'{kv[0]}: {kv[1]["text"]}', test_system_declaration_data.items())))
def test_system_declarations(parser, data):
    res = parser.parse(text=data["text"], rule_name=data["rule"])
    assert res == data["ast"]
