import pprint
import unittest

from uppyyl_simulator.backend.models.ta.labels.invariant import Invariant

pp = pprint.PrettyPrinter(indent=4, compact=True)
printExpectedResults = False
printActualResults = False


##############
# Invariants #
##############
class TestInvariant(unittest.TestCase):
    def setUp(self):
        print("")

    def test_code_to_ast(self):
        test_data = [{
            "info": "Invariant code (1)",
            "input": "t <= 2",
            "output":
                {'astType': 'Invariant',
                 'expr': {'astType': 'BinaryExpr',
                          'left': {'astType': 'Variable', 'name': 't'},
                          'op': 'LessEqual',
                          'right': {'astType': 'Integer', 'val': 2}}},
        }]
        for td in test_data:
            msg = f'Creating invariant ({td["info"]}) ...'
            with self.subTest(msg=msg):
                print(msg)
                inv = Invariant(td["input"])
                self.assertEqual(inv.ast, td["output"])

    def test_ast_to_code(self):
        test_data = [{
            "info": "Invariant ast (1)",
            "input":
                {'astType': 'Invariant',
                 'expr': {'astType': 'BinaryExpr',
                          'left': {'astType': 'Variable', 'name': 't'},
                          'op': 'LessEqual',
                          'right': {'astType': 'Integer', 'val': 2}}},
            "output": "t <= 2",
        }]
        for td in test_data:
            msg = f'Creating invariant ({td["info"]}) ...'
            with self.subTest(msg=msg):
                print(msg)
                inv = Invariant(td["input"])
                self.assertEqual(inv.text, td["output"])

    def test_set_empty_text(self):
        inv = Invariant("")
        self.assertIsNone(inv.ast)

    def test_copy(self):
        inv = Invariant("t <= 10")
        inv_copy = inv.copy()
        self.assertEqual(inv.text, inv_copy.text)
        self.assertEqual(inv.ast, inv_copy.ast)
        
    def test_str(self):
        inv = Invariant("t <= 10")
        res = str(inv)
        self.assertTrue(isinstance(res, str))


if __name__ == '__main__':
    unittest.main()
