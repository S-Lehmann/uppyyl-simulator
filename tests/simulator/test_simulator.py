import pprint
import unittest

from uppyyl_simulator.backend.data_structures.state.system_state import SystemState
from uppyyl_simulator.backend.simulator.simulator import (
    Simulator
)

pp = pprint.PrettyPrinter(indent=4, compact=True)
printExpectedResults = False
printActualResults = False

test_model_path = "./res/tests/transition-test.xml"


##################
# Test Simulator #
##################
class TestSimulator(unittest.TestCase):
    def setUp(self):
        self.uppaal_simulator = Simulator()
        self.uppaal_simulator.load_system(system_path=test_model_path)
        print("")

    def tearDown(self):
        print("")

    def test_simulate_1(self):
        self.uppaal_simulator.simulate(max_steps=20)
        self.assertLessEqual(len(self.uppaal_simulator.transition_trace), 21)

    def test_simulate_no_args(self):
        with self.assertRaises(Exception):
            self.uppaal_simulator.simulate()

    def test_simulate_steps(self):
        seq_len = 0
        for i in range(0, 100):
            _valid_trans_count = len(self.uppaal_simulator.transitions)
            _transition = self.uppaal_simulator.simulate_step()
            new_seq_len = len(self.uppaal_simulator.get_sequence())

            self.assertLessEqual(len(self.uppaal_simulator.transition_trace), i + 2)
            self.assertGreaterEqual(new_seq_len, seq_len)

            seq_len = new_seq_len

    def test_set_current_state(self):
        state = SystemState()
        self.uppaal_simulator.set_current_state(state=state)
        self.assertEqual(self.uppaal_simulator.system_state, state)

    def test_revert_to_state_by_index(self):
        self.uppaal_simulator.simulate(max_steps=10)
        self.uppaal_simulator.revert_to_state_by_index(idx=5)
        self.assertEqual(len(self.uppaal_simulator.transition_trace), 6)

    def test_get_valid_transitions(self):
        valid_transitions = self.uppaal_simulator.get_transitions()
        self.assertGreaterEqual(len(valid_transitions), 0)


if __name__ == '__main__':
    unittest.main()
