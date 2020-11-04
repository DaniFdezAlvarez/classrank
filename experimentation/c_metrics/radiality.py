from classrank_utils.g_paths import build_graph_for_paths, graph_diameter
from classrank_utils.scores import normalize_score
from experimentation.c_metrics.base_c_metric import BaseCMetric, NX_COMPUTATION



class RadialityComp(BaseCMetric):

    def __init__(self, triples_yielder, normalize, shortest_paths_dict=None,
                 shortest_paths_computation=NX_COMPUTATION, nxgraph=None, tunned_shortest_paths_dict=None,
                 precomouted_diameter=None):
        super().__init__(shortest_paths_dict=shortest_paths_dict,
                         shortest_paths_computation=shortest_paths_computation,
                         nxgraph=nxgraph,
                         tunned_shortest_paths_dict=tunned_shortest_paths_dict)
        self._triples_yielder = triples_yielder
        self._normalize = normalize
        self._radiality_dict = {}
        self._precomputed_diameter = precomouted_diameter

    def run(self, string_return=True, out_path=None):
        nxgraph = build_graph_for_paths(self._triples_yielder) if self._nxgraph is None else self._nxgraph
        diameter = self._precomputed_diameter if self._precomputed_diameter is not None \
            else graph_diameter(self._get_shortest_paths(nxgraph))
        tunned_paths = self._get_tunned_shortest_paths()
        for a_node in nxgraph.nodes:
            # denominator = 0
            # paths = shortest_path(graph=nxgraph,
            #                       origin=a_node)
            # self._fill_absent_paths_with_an_all_nodes_walk(paths_dict=paths,
            #                                                target_nodes=nxgraph.nodes,
            #                                                origin=a_node)
            # self._delete_auto_path(paths_dict=paths,
            #                        origin=a_node)
            denominator = sum([diameter - (float(1) / len(tunned_paths[a_path_key])) for a_path_key in tunned_paths])
            # for a_node_2 in nxgraph.nodes:
            #     if a_node != a_node_2:
            #         s_path = shortest_path(origin=a_node,
            #                                destination=a_node_2,
            #                                graph=nxgraph)
            #
            #         denominator += graph_diameter - (float(1)/len(s_path))
            #
            self._radiality_dict[a_node] = float(1) / denominator
        if self._normalize:
            self._normalize_dict()
            # self._normalize_dict(n_nodes=len(nxgraph),
            #                      g_diameter=graph_diameter)
        return self._return_result(obj_result=self._radiality_dict,
                                   string_return=string_return,
                                   out_path=out_path)

    # def _compute_graph_diameter(self, net_graph):
    #     # return net_graph.diameter
    #     paths = self._get_shortest_paths(net_graph)
    #     max_p = 0
    #     for a_key_origin in paths:
    #         for a_key_destination in paths[a_key_origin]:
    #             print(a_key_origin, paths[a_key_origin])
    #             new_p = len(paths[a_key_origin][a_key_destination])
    #             if new_p > max_p:
    #                 max_p = new_p
    #     return max_p

    def _find_max_score(self):
        return max([self._radiality_dict[an_uri] for an_uri in self._radiality_dict])

    def _normalize_dict(self):
        # denominator = (n_nodes - 1) * (g_diameter - 1)
        # max_score = float(1) / denominator
        max_score = self._find_max_score()
        for an_uri in self._radiality_dict:
            self._radiality_dict[an_uri] = normalize_score(score=self._radiality_dict[an_uri],
                                                           max_score=max_score)
