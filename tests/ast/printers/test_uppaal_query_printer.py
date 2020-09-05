import pprint

import pytest

from uppyyl_simulator.backend.ast.printers.uppaal_query_language_printer import UppaalQueryPrinter
from tests.ast.uppaal_query_language_test_data import test_uppaal_query_data, test_uppaal_smc_query_data

pp = pprint.PrettyPrinter(indent=4, compact=True)
printExpectedResults = False
printActualResults = False


@pytest.fixture
def printer():
    return UppaalQueryPrinter()


###########
# Queries #
###########
@pytest.mark.parametrize("data", test_uppaal_query_data.values(),
                         ids=list(map(lambda kv: f'{kv[0]}: {kv[1]["text"]}', test_uppaal_query_data.items())))
def test_uppaal_queries(printer, data):
    res = printer.ast_to_string(ast=data["ast"])
    res_without_whitespace = ''.join(res.split())
    expected_without_whitespace = ''.join(data["text"].split())
    assert res_without_whitespace == expected_without_whitespace


@pytest.mark.parametrize("data", test_uppaal_smc_query_data.values(),
                         ids=list(map(lambda kv: f'{kv[0]}: {kv[1]["text"]}', test_uppaal_smc_query_data.items())))
def test_uppaal_queries(printer, data):
    res = printer.ast_to_string(ast=data["ast"])
    res_without_whitespace = ''.join(res.split())
    expected_without_whitespace = ''.join(data["text"].split())
    assert res_without_whitespace == expected_without_whitespace
