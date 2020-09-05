import pprint
import unittest

from uppyyl_simulator.backend.ast.parsers.uppaal_xml_model_parser import uppaal_xml_to_system

pp = pprint.PrettyPrinter(indent=4, compact=True)
printExpectedResults = False
printActualResults = False

test_model_path = "./res/tests/uppaal_model_modifier_testmodel.xml"


################
# NTA Modifier #
################
class TestNTAModifier(unittest.TestCase):
    def setUp(self):
        with open(test_model_path) as file:
            uppaal_test_model_str = file.read()
        self.system = uppaal_xml_to_system(uppaal_test_model_str)
        print("")

    def tearDown(self):
        pass

    def test_move_sys_vars_to_global_decl(self):
        pass  # TODO: Test implementation


if __name__ == '__main__':
    unittest.main()
