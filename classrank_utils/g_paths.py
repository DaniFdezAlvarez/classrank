import networkx as nx

_S = 0
_O = 2

def build_graph_for_paths(triples_yielder):
    result = nx.DiGraph()
    for a_triple in triples_yielder.yield_triples():
        result.add_edge(a_triple[_S], a_triple[_O])
    return result

def shortest_path(graph, origin=None, destination=None):
    """
    When not provided both origin and source will be interpreted as "all nodes in the graph".
    origin: None, destination: v ---> shortest paths between all nodes and v
    origin: u, destination: None ---> shortest paths between u and all nodes
    origin: None, destination: None ---> shortest paths between all nodes and all others.
    :param origin:
    :param destination:
    :return:
    """
    return nx.shortest_path(graph,
                            source=origin,
                            target=destination)