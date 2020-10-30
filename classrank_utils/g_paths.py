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

def fill_absent_paths_with_an_all_nodes_walk(paths_dict, target_nodes, origin):
    """
    It expect a dict with this format:

    {'d': ['e', 'd'], 'b': ['e', 'b'], 'f': ['e', 'd', 'f'], 'e': ['e'], 'c': ['e', 'b', 'c']}

    key: destination_node from a given_source
    value: path from origin to reach the destination

    :param paths_dict:
    :param target_nodes: list of every node in the graph
    :param origin: node from which the path start
    :return:
    """
    infinity_path = [an_elem for an_elem in target_nodes]  # just a copy
    for a_node in target_nodes:
        if a_node != origin:
            if a_node not in paths_dict:
                paths_dict[a_node] = infinity_path


def shortests_paths_to_tunned_shortest_paths(shortest_paths, nxgraph):
    """"
    Warning!!! It modifies the shortest_paths object
    """
    for a_node in nxgraph.nodes:
        fill_absent_paths_with_an_all_nodes_walk(paths_dict=shortest_paths,
                                                 target_nodes=nxgraph.nodes,
                                                 origin=a_node)
        delete_auto_path(paths_dict=shortest_paths,
                         origin=a_node)
    return shortest_paths


def delete_auto_path(paths_dict, origin):
    """

    It expect a dict with this format:

    {'d': ['e', 'd'], 'b': ['e', 'b'], 'f': ['e', 'd', 'f'], 'e': ['e'], 'c': ['e', 'b', 'c']}

    key: destination_node from a given_source
    value: path from origin to reach the destination

    :param paths_dict:
    :param origin: node from which the path start
    :return:
    """
    if origin in paths_dict:
        del paths_dict[origin]


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
        result = {a_node: pool.apply(self._shortest_path_from_a_node, args=(a_node,)) for a_node in self._g.nodes}
        pool.close()
        return result
        # return {self._target_node(a_result_path) : a_result_path for a_result_path in result_paths}
        # result = {a_node: pool.apply(self._shortest_path_from_a_node, args=a_node) for a_node in self._g.nodes}

    def _target_node(self, result_path):
        for a_path in result_path.values():
            return a_path[0]
                # print(a_path, "----")
                # return a_path[0]  # not a nested for, just a random access to the first element in any of the paths



