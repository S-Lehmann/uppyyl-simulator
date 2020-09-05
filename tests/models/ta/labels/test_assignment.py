import pprint
import unittest

from uppyyl_simulator.backend.models.ta.labels.assignment import Reset, Update

pp = pprint.PrettyPrinter(indent=4, compact=True)
printExpectedResults = False
printActualResults = False


##########
# Update #
##########
class TestUpdate(unittest.TestCase):
    def setUp(self):
        print("")

    def test_code_to_ast(self):
        test_data = [{
            "info": "Update code (1)",
            "input": "x = 2",
            "output":
                {'astType': 'Update',
                 'expr': {'astType': 'AssignExpr',
                          'left': {'astType': 'Variable', 'name': 'x'},
                          'op': 'Assign',
                          'right': {'astType': 'Integer', 'val': 2}}},
        }]
        for td in test_data:
            msg = f'Creating update ({td["info"]}) ...'
            with self.subTest(msg=msg):
                print(msg)
                updt = Update(td["input"])
                self.assertEqual(updt.ast, td["output"])

    def test_ast_to_code(self):
        test_data = [{
            "info": "Update ast (1)",
            "input":
                {'astType': 'Update',
                 'expr': {'astType': 'AssignExpr',
                          'left': {'astType': 'Variable', 'name': 'x'},
                          'op': 'Assign',
                          'right': {'astType': 'Integer', 'val': 2}}},
            "output": "x = 2",
        }]
        for td in test_data:
            msg = f'Creating update ({td["info"]}) ...'
            with self.subTest(msg=msg):
                print(msg)
                updt = Update(td["input"])
                self.assertEqual(updt.text, td["output"])

    def test_set_empty_text(self):
        updt = Update("")
        self.assertIsNone(updt.ast)

    def test_copy(self):
        updt = Update("x = 10")
        updt_copy = updt.copy()
        self.assertEqual(updt.text, updt_copy.text)
        self.assertEqual(updt.ast, updt_copy.ast)

    def test_str(self):
        updt = Update("x = 10")
        res = str(updt)
        self.assertTrue(isinstance(res, str))


#########
# Reset #
#########
class TestReset(unittest.TestCase):
    def setUp(self):
        print("")

    def test_code_to_ast(self):
        test_data = [{
            "info": "Update code (1)",
            "input": "t = 0",
            "output":
                {'astType': 'Update',
                 'expr': {'astType': 'AssignExpr',
                          'left': {'astType': 'Variable', 'name': 't'},
                          'op': 'Assign',
                          'right': {'astType': 'Integer', 'val': 0}}},
        }]
        for td in test_data:
            msg = f'Creating reset ({td["info"]}) ...'
            with self.subTest(msg=msg):
                print(msg)
                rst = Reset(td["input"])
                self.assertEqual(rst.ast, td["output"])

    def test_ast_to_code(self):
        test_data = [{
            "info": "Update ast (1)",
            "input":
                {'astType': 'Update',
                 'expr': {'astType': 'AssignExpr',
                          'left': {'astType': 'Variable', 'name': 't'},
                          'op': 'Assign',
                          'right': {'astType': 'Integer', 'val': 0}}},
            "output": "t = 0",
        }]
        for td in test_data:
            msg = f'Creating reset ({td["info"]}) ...'
            with self.subTest(msg=msg):
                print(msg)
                rst = Reset(td["input"])
                self.assertEqual(rst.text, td["output"])

    def test_set_empty_text(self):
        rst = Reset("")
        self.assertIsNone(rst.ast)

    def test_copy(self):
        rst = Reset("t = 0")
        rst_copy = rst.copy()
        self.assertEqual(rst.text, rst_copy.text)
        self.assertEqual(rst.ast, rst_copy.ast)

    def test_str(self):
        rst = Reset("t = 0")
        res = str(rst)
        self.assertTrue(isinstance(res, str))


if __name__ == '__main__':
    unittest.main()
