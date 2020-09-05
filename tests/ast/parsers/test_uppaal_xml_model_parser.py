import os
import pathlib
import pprint
import unittest

from uppyyl_simulator.backend.ast.parsers.uppaal_xml_model_parser import (
    uppaal_xml_to_dict, uppaal_dict_to_system, uppaal_system_to_dict, uppaal_dict_to_xml
)

pp = pprint.PrettyPrinter(indent=4, compact=True)
printExpectedResults = False
printActualResults = False

test_model_path = './res/tests/uppaal_xml_testmodel.xml'
generated_model_folder = './res/tests/created_models'


######################
# Uppaal XML to dict #
######################
class TestUppaalXMLToDict(unittest.TestCase):
    def setUp(self):
        with open(test_model_path) as file:
            uppaal_test_model_str = file.read()
        self.system_xml_str = uppaal_test_model_str
        print("")

    def test_uppaal_xml_to_dict(self):
        _dict_data = uppaal_xml_to_dict(self.system_xml_str)
        # print(dict_data)


#########################
# Uppaal dict to system #
#########################
class TestUppaalDictToSystem(unittest.TestCase):
    def setUp(self):
        with open(test_model_path) as file:
            uppaal_test_model_str = file.read()
        self.system_xml_str = uppaal_test_model_str
        print("")

    def test_uppaal_dict_to_system(self):
        dict_data = uppaal_xml_to_dict(self.system_xml_str)
        _system = uppaal_dict_to_system(dict_data)
        # print(system)


######################
# Uppaal dict to XML #
######################
class TestUppaalDictToXML(unittest.TestCase):
    def setUp(self):
        with open(test_model_path) as file:
            uppaal_test_model_str = file.read()
        self.system_xml_str = uppaal_test_model_str
        print("")

    def test_uppaal_dict_to_system(self):
        dict_data = uppaal_xml_to_dict(self.system_xml_str)
        system_xml_str = uppaal_dict_to_xml(dict_data)

        generated_model_name = 'testmodel.xml'
        generated_model_path = os.path.join(generated_model_folder, generated_model_name)
        pathlib.Path(generated_model_folder).mkdir(parents=True, exist_ok=True)
        with open(generated_model_path, 'w') as file:
            file.write(system_xml_str)
        # print(system_xml_str)


######################
# Uppaal dict to XML #
######################
class TestUppaalXMLFullCycle(unittest.TestCase):
    def setUp(self):
        with open(test_model_path) as file:
            uppaal_test_model_str = file.read()
        self.system_xml_str = uppaal_test_model_str
        print("")

    def test_uppaal_dict_to_system(self):
        dict_data = uppaal_xml_to_dict(self.system_xml_str)
        system = uppaal_dict_to_system(dict_data)
        dict_data_rev = uppaal_system_to_dict(system)
        system_xml_str_rev = uppaal_dict_to_xml(dict_data_rev)

        generated_model_name = 'testmodel_full_cycle.xml'
        generated_model_path = os.path.join(generated_model_folder, generated_model_name)
        pathlib.Path(generated_model_folder).mkdir(parents=True, exist_ok=True)
        with open(generated_model_path, 'w') as file:
            file.write(system_xml_str_rev)
        # print(system_xml_str_rev)


if __name__ == '__main__':
    unittest.main()
