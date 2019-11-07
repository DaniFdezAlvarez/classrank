from classrank_utils.g_paths import build_graph_for_paths, shortest_path
from classrank_utils.scores import normalize_score

from experimentation.c_metrics.base_c_metric import BaseCMetric

class RadialityComp(BaseCMetric):

    def __init__(self, triples_yielder, normalize):
        self._triples_yielder = triples_yielder
        self._normalize = normalize
        self._radiality_dict = {}


    def run(self, string_return=True, out_path=None):
        nxgraph = build_graph_for_paths(self._triples_yielder)
        graph_diameter = self._compute_graph_diameter(nxgraph)
        for a_node in nxgraph.nodes:
            # denominator = 0
            paths = shortest_path(graph=nxgraph,
                                  origin=a_node)
            self._fill_absent_paths_with_an_all_nodes_walk(paths_dict=paths,
                                                           target_nodes=nxgraph.nodes,
                                                           origin=a_node)
            self._delete_auto_path(paths_dict=paths,
                                   origin=a_node)
            denominator = sum([graph_diameter - (float(1) / len(paths[a_path_key])) for a_path_key in paths])
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
            self._normalize_dict(n_nodes=len(nxgraph),
                                 g_diameter=graph_diameter)
        return self._return_result(obj_result=self._radiality_dict,
                                   string_return=string_return,
                                   out_path=out_path)

    def _compute_graph_diameter(self, net_graph):
        paths = shortest_path(graph=net_graph,
                              origin=None,
                              destination=None)
        max_p = 0
        for a_key_origin in paths:
            for a_key_destination in paths[a_key_origin]:
                new_p = len(paths[a_key_origin][a_key_destination])
                if new_p > max_p:
                    max_p = new_p
        return max_p


    def _normalize_dict(self, g_diameter, n_nodes):
        denominator = (n_nodes - 1) * (g_diameter - 1)


        max_score = float(1) / denominator  # TODO MAX SCORE
        for an_uri in self._radiality_dict:
            self._radiality_dict[an_uri] = normalize_score(score=self._radiality_dict[an_uri],
                                                           max_score=max_score)

