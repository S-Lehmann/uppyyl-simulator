import pprint

import pytest
from uppyyl_simulator.backend.ast.parsers.generated.uppaal_c_language_parser import (
    UppaalCLanguageParser
)

from uppyyl_simulator.backend.ast.parsers.uppaal_c_language_semantics import (
    UppaalCLanguageSemantics
)
from tests.ast.uppaal_query_language_test_data import test_uppaal_query_data, test_uppaal_smc_query_data

pp = pprint.PrettyPrinter(indent=4, compact=True)
printExpectedResults = False
printActualResults = False


@pytest.fixture
def parser():
    return UppaalCLanguageParser(semantics=UppaalCLanguageSemantics())


###########
# Queries #
###########
@pytest.mark.parametrize("data", test_uppaal_query_data.values(),
                         ids=list(map(lambda kv: f'{kv[0]}: {kv[1]["text"]}', test_uppaal_query_data.items())))
def test_uppaal_queries(parser, data):
    res = parser.parse(text=data["text"], rule_name=data["rule"])
    assert res == data["ast"]


@pytest.mark.parametrize("data", test_uppaal_smc_query_data.values(),
                         ids=list(map(lambda kv: f'{kv[0]}: {kv[1]["text"]}', test_uppaal_smc_query_data.items())))
def test_uppaal_smc_queries(parser, data):
    res = parser.parse(text=data["text"], rule_name=data["rule"])
    assert res == data["ast"]
