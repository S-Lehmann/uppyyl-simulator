import pprint
import unittest

from uppyyl_simulator.backend.models.ta.labels.select import Select

pp = pprint.PrettyPrinter(indent=4, compact=True)
printExpectedResults = False
printActualResults = False


##########
# Select #
##########
class TestSelect(unittest.TestCase):
    def setUp(self):
        print("")

    def test_code_to_ast(self):
        test_data = [{
            "info": "Select code (1)",
            "input": "x : int[0, 10]",
            "output":
                {'astType': 'Select',
                 'name': 'x',
                 'type': {'astType': 'Type',
                          'prefixes': [],
                          'typeId': {'astType': 'BoundedIntType',
                                     'lower': {'astType': 'Integer', 'val': 0},
                                     'upper': {'astType': 'Integer', 'val': 10}}}},
        }]
        for td in test_data:
            msg = f'Creating select ({td["info"]}) ...'
            with self.subTest(msg=msg):
                print(msg)
                sel = Select(td["input"])
                self.assertEqual(sel.ast, td["output"])

    def test_ast_to_code(self):
        test_data = [{
            "info": "Select ast (1)",
            "input":
                {'astType': 'Select',
                 'name': 'x',
                 'type': {'astType': 'Type',
                          'prefixes': [],
                          'typeId': {'astType': 'BoundedIntType',
                                     'lower': {'astType': 'Integer', 'val': 0},
                                     'upper': {'astType': 'Integer', 'val': 10}}}},
            "output": "x : int[0, 10]",
        }]
        for td in test_data:
            msg = f'Creating select ({td["info"]}) ...'
            with self.subTest(msg=msg):
                print(msg)
                sel = Select(td["input"])
                self.assertEqual(sel.text, td["output"])

    def test_set_empty_text(self):
        sel = Select("")
        self.assertIsNone(sel.ast)

    def test_copy(self):
        sel = Select("x : int[0, 10]")
        sel_copy = sel.copy()
        self.assertEqual(sel.text, sel_copy.text)
        self.assertEqual(sel.ast, sel_copy.ast)

    def test_str(self):
        sel = Select("x : int[0, 10]")
        res = str(sel)
        self.assertTrue(isinstance(res, str))


if __name__ == '__main__':
    unittest.main()
