from experimentation.c_metrics.base_c_metric import BaseCMetric, NX_COMPUTATION
from classrank_utils.g_paths import build_graph_for_paths

class ClosenessComp(BaseCMetric):

    def __init__(self, triples_yielder, shortest_paths_dict=None, shortest_paths_computation=NX_COMPUTATION,
                 nxgraph=None, tunned_shortest_paths_dict=None):
        """
        Here we will used the normalized version of the algorithm in every case, which is the most common one
        :param triples_yielder:
        """
        super().__init__(shortest_paths_dict=shortest_paths_dict,
                         shortest_paths_computation=shortest_paths_computation,
                         nxgraph=nxgraph,
                         tunned_shortest_paths_dict=tunned_shortest_paths_dict)
        self._triples_yielder = triples_yielder
        self._dict_closeness = {}


    def run(self, string_return=True, out_path=None):
        nxgraph = build_graph_for_paths(self._triples_yielder) if self._nxgraph is None else self._nxgraph
        tunned_paths = self._get_tunned_shortest_paths(nxgraph)
        for a_node in nxgraph.nodes:
            # paths = self._get_shortest_paths(nxgraph)
            # self._fill_absent_paths_with_an_all_nodes_walk(paths_dict=paths,
            #                                                target_nodes=nxgraph.nodes,
            #                                                origin=a_node)
            # self._delete_auto_path(paths_dict=paths,
            #                        origin=a_node)
            denominator = sum([len(tunned_paths[a_path_key]) for a_path_key in tunned_paths])
            self._dict_closeness[a_node] = float(len(nxgraph) - 1) / denominator

        return self._return_result(obj_result=self._dict_closeness,
                                   string_return=string_return,
                                   out_path=out_path)



