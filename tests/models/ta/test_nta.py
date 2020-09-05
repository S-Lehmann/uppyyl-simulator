import pprint
import unittest

from uppyyl_simulator.backend.ast.parsers.uppaal_xml_model_parser import uppaal_xml_to_system
from uppyyl_simulator.backend.data_structures.state.system_state import SystemState
from uppyyl_simulator.backend.models.ta.nta import (
    System
)

pp = pprint.PrettyPrinter(indent=4, compact=True)
printExpectedResults = False
printActualResults = False

test_model_path = './res/tests/uppaal_xml_testmodel.xml'


###################
# System Creation #
###################
class TestSystemCreation(unittest.TestCase):
    def setUp(self):
        print("")

    def test_create_automaton(self):
        test_data = [{
            "info": "System (1)",
            "input": "",
            "output":
                {},
        }]
        for td in test_data:
            msg = f'Creating system ({td["info"]}) ...'
            with self.subTest(msg=msg):
                print(msg)
                system = System()
                print(system)


####################
# System Functions #
####################
class TestSystemFunctions(unittest.TestCase):
    def setUp(self):
        print("")

    def test_get_templates(self):
        system = System()
        _tmpl_1 = system.new_template(name="Tmpl1", id_="tmpl-1")
        tmpl_2 = system.new_template(name="Tmpl2", id_="tmpl-2")
        get_tmpl = system.get_template_by_name(name="Tmpl2")
        self.assertEqual(tmpl_2, get_tmpl)
        get_tmpl = system.get_template_by_id(id_="tmpl-2")
        self.assertEqual(tmpl_2, get_tmpl)
        get_tmpl = system.get_template_by_index(index=1)
        self.assertEqual(tmpl_2, get_tmpl)

    def test_get_templates_exceptions(self):
        system = System()
        with self.assertRaises(Exception):
            _tmpl = system.get_template_by_name(name="Tmpl")
        with self.assertRaises(Exception):
            _tmpl = system.get_template_by_id(id_="tmpl")
        with self.assertRaises(Exception):
            _tmpl = system.get_template_by_index(index=0)

    def test_get_system_details(self):
        with open(test_model_path) as file:
            uppaal_test_model_str = file.read()
        system_xml_str = uppaal_test_model_str
        system = uppaal_xml_to_system(system_xml_str)

        state = SystemState()
        state.init_from_system(system)
        _system_details = system.get_system_details(state=state)

        # TODO: Assertions

    def test_str(self):
        system = System()
        system.new_template(name="Tmpl1", id_="tmpl-1")
        str(system)


if __name__ == '__main__':
    unittest.main()
