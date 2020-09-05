import pprint
import unittest

from uppyyl_simulator.backend.models.ta.labels.guard import VariableGuard, ClockGuard

pp = pprint.PrettyPrinter(indent=4, compact=True)
printExpectedResults = False
printActualResults = False


##################
# Variable Guard #
##################
class TestVariableGuard(unittest.TestCase):
    def setUp(self):
        print("")

    def test_code_to_ast(self):
        test_data = [{
            "info": "Variable guard code (1)",
            "input": "a == 2",
            "output":
                {'astType': 'Guard',
                 'expr': {'astType': 'BinaryExpr',
                          'left': {'astType': 'Variable', 'name': 'a'},
                          'op': 'Equal',
                          'right': {'astType': 'Integer', 'val': 2}}},
        }]
        for td in test_data:
            msg = f'Creating variable guard ({td["info"]}) ...'
            with self.subTest(msg=msg):
                print(msg)
                grd = VariableGuard(td["input"])

                res = grd.ast
                expected_res = td["output"]
                self.assertEqual(res, expected_res)

    def test_ast_to_code(self):
        test_data = [{
            "info": "Variable guard ast (1)",
            "input":
                {'astType': 'Guard',
                 'expr': {'astType': 'BinaryExpr',
                          'left': {'astType': 'Variable', 'name': 'a'},
                          'op': 'Equal',
                          'right': {'astType': 'Integer', 'val': 2}}},
            "output": "a == 2",
        }]
        for td in test_data:
            msg = f'Creating variable guard ({td["info"]}) ...'
            with self.subTest(msg=msg):
                print(msg)
                grd = VariableGuard(td["input"])
                self.assertEqual(grd.text, td["output"])

    def test_set_empty_text(self):
        grd = VariableGuard("")
        self.assertIsNone(grd.ast)

    def test_copy(self):
        grd = VariableGuard("cond")
        grd_copy = grd.copy()
        self.assertEqual(grd.text, grd_copy.text)
        self.assertEqual(grd.ast, grd_copy.ast)

    def test_str(self):
        grd = VariableGuard("cond")
        res = str(grd)
        self.assertTrue(isinstance(res, str))


###############
# Clock Guard #
###############
class TestClockGuard(unittest.TestCase):
    def setUp(self):
        print("")

    def test_code_to_ast(self):
        test_data = [{
            "info": "Clock guard code (1)",
            "input": "t >= 2",
            "output":
                {'astType': 'Guard',
                 'expr': {'astType': 'BinaryExpr',
                          'left': {'astType': 'Variable', 'name': 't'},
                          'op': 'GreaterEqual',
                          'right': {'astType': 'Integer', 'val': 2}}},
        }]
        for td in test_data:
            msg = f'Creating clock guard ({td["info"]}) ...'
            with self.subTest(msg=msg):
                print(msg)
                grd = ClockGuard(td["input"])
                self.assertEqual(grd.ast, td["output"])

    def test_ast_to_code(self):
        test_data = [{
            "info": "Clock guard ast (1)",
            "input":
                {'astType': 'Guard',
                 'expr': {'astType': 'BinaryExpr',
                          'left': {'astType': 'Variable', 'name': 't'},
                          'op': 'GreaterEqual',
                          'right': {'astType': 'Integer', 'val': 2}}},
            "output": "t >= 2",
        }]
        for td in test_data:
            msg = f'Creating clock guard ({td["info"]}) ...'
            with self.subTest(msg=msg):
                print(msg)
                grd = ClockGuard(td["input"])
                self.assertEqual(grd.text, td["output"])

    def test_set_empty_text(self):
        grd = ClockGuard("")
        self.assertIsNone(grd.ast)

    def test_copy(self):
        grd = ClockGuard("t >= 10")
        grd_copy = grd.copy()
        self.assertEqual(grd.text, grd_copy.text)
        self.assertEqual(grd.ast, grd_copy.ast)

    def test_str(self):
        grd = ClockGuard("t >= 10")
        res = str(grd)
        self.assertTrue(isinstance(res, str))


if __name__ == '__main__':
    unittest.main()
