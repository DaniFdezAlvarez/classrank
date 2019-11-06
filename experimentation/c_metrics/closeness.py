from experimentation.c_metrics.base_c_metric import BaseCMetric
from classrank_utils.g_paths import build_graph_for_paths, shortest_path

class ClosenessComp(BaseCMetric):

    def __init__(self, triples_yielder):
        """
        Here we will used the normalized version of the algorithm in every case, which is the most common one
        :param triples_yielder:
        """
        self._triples_yielder = triples_yielder
        self._dict_closeness = {}


    def run(self, string_return=True, out_path=None):
        nxgraph = build_graph_for_paths(self._triples_yielder)
        for a_node in nxgraph.nodes:
            paths = shortest_path(graph=nxgraph,
                                  origin=a_node)
            print(a_node, paths)
            self._fill_absent_paths_with_an_all_nodes_walk(paths_dict=paths,
                                                           target_nodes=nxgraph.nodes,
                                                           origin=a_node)
            self._delete_auto_path(paths_dict=paths,
                                   origin=a_node)
            denominator = sum([len(paths[a_path_key]) for a_path_key in paths])
            self._dict_closeness[a_node] = float(len(nxgraph) - 1) / denominator

        return self._return_result(obj_result=self._dict_closeness,
                                   string_return=string_return,
                                   out_path=out_path)



