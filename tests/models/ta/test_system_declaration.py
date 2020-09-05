import pprint
import unittest

from uppyyl_simulator.backend.models.ta.system_declaration import SystemDeclaration

pp = pprint.PrettyPrinter(indent=4, compact=True)
printExpectedResults = False
printActualResults = False


######################
# System Declaration #
######################
class TestSystemDeclaration(unittest.TestCase):
    def setUp(self):
        print("")

    def test_set_empty_text(self):
        decl = SystemDeclaration("")
        self.assertIsNone(decl.ast)

    def test_copy(self):
        decl = SystemDeclaration("Inst = Tmpl();\nsystem Inst;")
        decl_copy = decl.copy()
        self.assertEqual(decl.text, decl_copy.text)
        self.assertEqual(decl.ast, decl_copy.ast)

    def test_str(self):
        decl = SystemDeclaration("Inst = Tmpl(); system Inst;")
        res = str(decl)
        self.assertTrue(isinstance(res, str))


if __name__ == '__main__':
    unittest.main()
