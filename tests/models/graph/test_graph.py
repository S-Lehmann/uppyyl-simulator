import pprint

import pytest

from uppyyl_simulator.backend.models.graph.graph import Graph

pp = pprint.PrettyPrinter(indent=4, compact=True)
printExpectedResults = False
printActualResults = False


@pytest.fixture
def graph():
    graph = Graph(name="graph")
    graph.new_node(name="node1", id_="id-node-1")
    graph.new_node(name="node2", id_="id-node-2")
    return graph


#########
# Graph #
#########
def test_weighted_graph_new_edge_by_node_names(graph):
    graph.new_edge_by_node_names(source_name="node1", target_name="node2")
    assert len(graph.edges) == 1
    edge = list(graph.edges.values())[0]
    assert (edge.source.name, edge.target.name) == ("node1", "node2")


def test_weighted_graph_new_edge_by_node_ids(graph):
    graph.new_edge_by_node_ids(source_id="id-node-1", target_id="id-node-2")
    assert len(graph.edges) == 1
    edge = list(graph.edges.values())[0]
    assert (edge.source.id, edge.target.id) == ("id-node-1", "id-node-2")
