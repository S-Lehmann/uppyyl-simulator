import pprint

import pytest

from uppyyl_simulator.backend.models.graph.weighted_graph import WeightedGraph

pp = pprint.PrettyPrinter(indent=4, compact=True)
printExpectedResults = False
printActualResults = False


@pytest.fixture
def w_graph():
    w_graph = WeightedGraph(name="w_graph")
    w_graph.new_node(name="node1", id_="id-node-1")
    w_graph.new_node(name="node2", id_="id-node-2")
    return w_graph


##################
# Weighted Graph #
##################
def test_weighted_graph_new_edge_by_node_names(w_graph):
    w_graph.new_edge_by_node_names(source_name="node1", target_name="node2", weight=10)
    assert len(w_graph.edges) == 1
    edge = list(w_graph.edges.values())[0]
    assert (edge.source.name, edge.target.name, edge.weight) == ("node1", "node2", 10)


def test_weighted_graph_new_edge_by_node_ids(w_graph):
    w_graph.new_edge_by_node_ids(source_id="id-node-1", target_id="id-node-2", weight=10)
    assert len(w_graph.edges) == 1
    edge = list(w_graph.edges.values())[0]
    assert (edge.source.id, edge.target.id, edge.weight) == ("id-node-1", "id-node-2", 10)


########
# Edge #
########
@pytest.fixture
def wedge():
    w_graph = WeightedGraph(name="w_graph")
    node1 = w_graph.new_node(name="node1", id_="id-node-1")
    node2 = w_graph.new_node(name="node2", id_="id-node-2")
    edge = w_graph.new_edge(source=node1, target=node2, weight=10)
    return edge


@pytest.fixture
def wedge2():
    w_graph = WeightedGraph(name="w_graph")
    node1 = w_graph.new_node(name="node1", id_="id-node-1")
    node2 = w_graph.new_node(name="node2", id_="id-node-2")
    edge = w_graph.new_edge(source=node1, target=node2, weight=20)
    return edge


def test_edge_set_weight(wedge):
    wedge.set_weight(20)
    assert wedge.weight == 20


def test_edge_assign_from(wedge, wedge2):
    wedge.assign_from(wedge2)
    assert wedge.weight == 20


def test_edge_str(wedge):
    assert isinstance(str(wedge), str)
