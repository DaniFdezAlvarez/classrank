import networkx as nx
import multiprocessing as mp

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


MAX_AVAILABLE = -1


class EfficientShortPathCalculator(object):

    def __init__(self, nx_graph, n_threads=MAX_AVAILABLE):
        self._g = nx_graph
        self._s_paths_dict = None
        self._n_threads = n_threads if n_threads != MAX_AVAILABLE else mp.cpu_count()


    def get_shortest_path_between_nodes(self, origin, dest):
        if self._s_paths_dict is None:
            self._compute_shortest_paths()
        if origin in self._s_paths_dict and dest in self._s_paths_dict[origin]:
            return self._s_paths_dict[origin][dest]
        return None

    def get_shortests_paths(self):
        if self._s_paths_dict is None:
            self._compute_shortest_paths()
        return self._s_paths_dict

    def _shortest_path_from_a_node(self, a_node):
        return nx.shortest_path(self._g,
                                source=a_node,
                                target=None)

    def _compute_shortest_paths(self):
        pool = mp.Pool(self._n_threads)
        result = {a_node: pool.apply(self._shortest_path_from_a_node, args=a_node) for a_node in self._g.nodes}
        pool.close()
        return result



