import pprint

import pytest

from uppyyl_simulator.backend.data_structures.state.system_state import SystemState
from uppyyl_simulator.backend.models.ta import Location, Edge
from uppyyl_simulator.backend.models.ta.transition import Transition

pp = pprint.PrettyPrinter(indent=4, compact=True)
printExpectedResults = False
printActualResults = False


@pytest.fixture
def transition():
    state = SystemState()
    loc1 = Location(name="loc1")
    loc2 = Location(name="loc2")
    edge = Edge(source=loc1, target=loc2)
    state.location_state = {"Inst1": loc1}
    trans = Transition(source_state=state, target_state=state, triggered_edges={"Inst1": None, "Inst2": edge})
    return trans


@pytest.fixture
def transition2():
    trans = Transition(source_state=None, target_state=None, triggered_edges=None)
    return trans


##############
# Transition #
##############
def test_transition_short_string_1(transition):
    assert isinstance(transition.short_string(), str)


def test_transition_short_string_2(transition2):
    assert isinstance(transition2.short_string(), str)


def test_transition_str_1(transition):
    assert isinstance(str(transition), str)


def test_transition_str_2(transition2):
    assert isinstance(str(transition2), str)
