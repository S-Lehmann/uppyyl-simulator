import pprint
import unittest

from uppyyl_simulator.backend.models.base.automaton import (
    Automaton
)

pp = pprint.PrettyPrinter(indent=4, compact=True)
printExpectedResults = False
printActualResults = False


######################
# Automaton Creation #
######################
class TestAutomatonCreation(unittest.TestCase):
    def setUp(self):
        print("")

    def test_create_automaton(self):
        test_data = [{
            "info": "Automaton (1)",
            "input": "",
            "output":
                {},
        }]
        for td in test_data:
            msg = f'Creating model ({td["info"]}) ...'
            with self.subTest(msg=msg):
                print(msg)
                autom = Automaton("A_Autom")
                print(autom.id)


if __name__ == '__main__':
    unittest.main()
