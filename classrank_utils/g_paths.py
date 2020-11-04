import networkx as nx
import multiprocessing as mp

_S = 0
_O = 2


def build_graph_for_paths(triples_yielder):
    result = nx.DiGraph()
    for a_triple in triples_yielder.yield_triples(max_triples=20000):  # TODO remove!
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

def fill_absent_paths_with_an_all_nodes_walk(paths_dict, target_nodes):
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

    for a_node_origin in target_nodes:
        partial_paths_dict = paths_dict[a_node_origin]
        for a_node_dest in target_nodes:
            if a_node_origin != a_node_dest:
                if a_node_dest not in partial_paths_dict:
                    partial_paths_dict[a_node_dest] = infinity_path


def shortests_paths_to_tunned_shortest_paths(shortest_paths, nxgraph):
    """"
    Warning!!! It modifies the shortest_paths object
    """
    fill_absent_paths_with_an_all_nodes_walk(paths_dict=shortest_paths,
                                             target_nodes=nxgraph.nodes)
    delete_auto_path(paths_dict=shortest_paths)
    return shortest_paths


def graph_diameter(paths):
    max_p = 0
    for a_key_origin in paths:
        for a_key_destination in paths[a_key_origin]:
            new_p = len(paths[a_key_origin][a_key_destination])
            if new_p > max_p:
                max_p = new_p
    return max_p


def delete_auto_path(paths_dict):
    """

    It expect a dict with this format:

    {'d': ['e', 'd'], 'b': ['e', 'b'], 'f': ['e', 'd', 'f'], 'e': ['e'], 'c': ['e', 'b', 'c']}

    key: destination_node from a given_source
    value: path from origin to reach the destination

    :param paths_dict:
    :param origin: node from which the path start
    :return:
    """
    for a_origin_key in paths_dict:
        if a_origin_key in paths_dict[a_origin_key]:
            del paths_dict[a_origin_key][a_origin_key]


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

    @staticmethod
    def _shortest_path_from_a_node(graph, a_node):
        # print("Ini", a_node)
        result = nx.shortest_path(graph,
                                  source=a_node,
                                  target=None)
        # print("End", a_node)
        return result

    def _g_copy_and_ranges(self, n_threads):
        node_groups = []
        current_group = []
        avg = len(self._g) / float(n_threads)
        next = avg

        i = 0
        for a_node in self._g.nodes:
            current_group.append(a_node)
            i += 1
            if i > next:
                node_groups.append(current_group)
                current_group = []
                next += avg + 1
        if len(current_group) >= 1:
            node_groups.append(current_group)
        for a_group in node_groups:
            yield self._g.copy(as_view=True), a_group

    def _compute_section_shortests_paths(self, g_view, node_section, list_result):
        list_result.append({a_node: self._shortest_path_from_a_node(graph=g_view, a_node=a_node) for a_node in node_section})

    def _compute_shortest_paths(self):
        manager = mp.Manager()
        list_result = manager.list()
        processes = [mp.Process(target=self._compute_section_shortests_paths,
                                args=(g_view, node_section, list_result))
                     for g_view, node_section in self._g_copy_and_ranges(self._n_threads)]
        for p in processes:
            p.start()
        for p in processes:
            p.join()
        self._s_paths_dict = self._integrate_list_results_into_single_dict(list_result)
        # Process(target=f, args=('bob',))

        # pool = mp.Pool(self._n_threads)
        # result = {a_node: pool.apply(self._shortest_path_from_a_node, args=(self._g.copy(as_vire=True), a_node))
        #           for a_node in self._g.nodes}
        # pool.close()
        # return result
        # return {self._target_node(a_result_path) : a_result_path for a_result_path in result_paths}
        # result = {a_node: pool.apply(self._shortest_path_from_a_node, args=a_node) for a_node in self._g.nodes}

    def _integrate_list_results_into_single_dict(self, target_list):
        result = {}
        for a_dict in target_list:
            for a_key, a_value in a_dict.items():
                result[a_key] = a_value
        return result

    def _target_node(self, result_path):
        for a_path in result_path.values():
            return a_path[0]
                # print(a_path, "----")
                # return a_path[0]  # not a nested for, just a random access to the first element in any of the paths



