import pprint
import unittest

from uppyyl_simulator.backend.models.ta.labels.parameter import Parameter

pp = pprint.PrettyPrinter(indent=4, compact=True)
printExpectedResults = False
printActualResults = False


#############
# Parameter #
#############
class TestParameter(unittest.TestCase):
    def setUp(self):
        print("")

    def test_set_empty_text(self):
        param = Parameter("")
        self.assertIsNone(param.ast)

    def test_copy(self):
        param = Parameter("int x")
        param_copy = param.copy()
        self.assertEqual(param.text, param_copy.text)
        self.assertEqual(param.ast, param_copy.ast)

    def test_str(self):
        param = Parameter("int x")
        res = str(param)
        self.assertTrue(isinstance(res, str))


if __name__ == '__main__':
    unittest.main()
