from classrank_utils.g_paths import build_graph_for_paths
from classrank_utils.scores import normalize_score
from experimentation.c_metrics.base_c_metric import BaseCMetric, NX_COMPUTATION

class HarmonicCentralityComp(BaseCMetric):

    def __init__(self, triples_yielder, normalize=False, shortest_paths_dict=None,
                 shortest_paths_computation=NX_COMPUTATION, nxgraph=None, tunned_shortest_paths_dict=None):
        super().__init__(shortest_paths_dict=shortest_paths_dict,
                         shortest_paths_computation=shortest_paths_computation,
                         nxgraph=nxgraph,
                         tunned_shortest_paths_dict=tunned_shortest_paths_dict)
        self._triples_yielder = triples_yielder
        self._normalize = normalize
        self._harmonic_dict = {}

    def run(self, string_return=True, out_path=None):
        nxgraph = build_graph_for_paths(self._triples_yielder) if self._nxgraph is None else self._nxgraph
        tunned_paths = self._get_tunned_shortest_paths(graph=nxgraph)
        for a_node in nxgraph.nodes:
            # paths = shortest_path(graph=nxgraph,
            #                       origin=a_node)
            # self._fill_absent_paths_with_an_all_nodes_walk(paths_dict=paths,
            #                                                target_nodes=nxgraph.nodes,
            #                                                origin=a_node)
            # self._delete_auto_path(paths_dict=paths,
            #                        origin=a_node)
            denominator = sum([len(tunned_paths[a_path_key]) for a_path_key in tunned_paths])
            # denominator = 0
            # for a_node_2 in nxgraph.nodes:
            #     if a_node != a_node_2:
            #         s_path = shortest_path(origin=a_node,
            #                                destination=a_node_2,
            #                                graph=nxgraph)
            #
            #         denominator += len(s_path)
            self._harmonic_dict[a_node] = float(1) / denominator
        if self._normalize:
            # max_score = float(1) / (len(nxgraph) - 1)
            max_score = self._find_max_score()
            self._normalize_dict(max_score)
        return self._return_result(obj_result=self._harmonic_dict,
                                   string_return=string_return,
                                   out_path=out_path)

    def _find_max_score(self):
        return max([self._harmonic_dict[an_uri] for an_uri in self._harmonic_dict])

    def _normalize_dict(self, max_score):
        for an_uri in self._harmonic_dict:
            self._harmonic_dict[an_uri] = normalize_score(score=self._harmonic_dict[an_uri],
                                                          max_score=max_score)


