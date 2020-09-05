import pprint
import unittest

from uppyyl_simulator.backend.models.ta.labels.sync import Synchronization

pp = pprint.PrettyPrinter(indent=4, compact=True)
printExpectedResults = False
printActualResults = False


###################
# Synchronization #
###################
class TestSynchronization(unittest.TestCase):
    def setUp(self):
        print("")

    def test_code_to_ast(self):
        test_data = [{
            "info": "Synchronization code (1)",
            "input": "ch!",
            "output":
                {'astType': 'Sync',
                 'channel': {'astType': 'Variable', 'name': 'ch'},
                 'op': '!'},
        }, {
            "info": "Synchronization code (2)",
            "input": "ch?",
            "output":
                {'astType': 'Sync',
                 'channel': {'astType': 'Variable', 'name': 'ch'},
                 'op': '?'},
        }]
        for td in test_data:
            msg = f'Creating synchronization ({td["info"]}) ...'
            with self.subTest(msg=msg):
                print(msg)
                sync = Synchronization(td["input"])
                self.assertEqual(sync.ast, td["output"])

    def test_ast_to_code(self):
        test_data = [{
            "info": "Synchronization ast (1)",
            "input":
                {'astType': 'Sync',
                 'channel': {'astType': 'Variable', 'name': 'ch'},
                 'op': '!'},
            "output": "ch!",
        }, {
            "info": "Synchronization ast (2)",
            "input":
                {'astType': 'Sync',
                 'channel': {'astType': 'Variable', 'name': 'ch'},
                 'op': '?'},
            "output": "ch?",
        }]
        for td in test_data:
            msg = f'Creating synchronization ({td["info"]}) ...'
            with self.subTest(msg=msg):
                print(msg)
                sync = Synchronization(td["input"])
                self.assertEqual(sync.text, td["output"])

    def test_set_empty_text(self):
        sync = Synchronization("")
        self.assertIsNone(sync.ast)

    def test_copy(self):
        sync = Synchronization("ch!")
        sync_copy = sync.copy()
        self.assertEqual(sync.text, sync_copy.text)
        self.assertEqual(sync.ast, sync_copy.ast)

    def test_str(self):
        sync = Synchronization("ch!")
        res = str(sync)
        self.assertTrue(isinstance(res, str))


if __name__ == '__main__':
    unittest.main()
