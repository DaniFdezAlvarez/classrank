# from classrank_utils.g_paths import build_graph_for_paths
# from experimentation.c_metrics.base_c_metric import BaseCMetric
#
# class EgoCentralutyComp(BaseCMetric):
#
#     def __init__(self, triples_yielder, normalize=False):
#         self._triples_yielder = triples_yielder
#         self._normalize = normalize
#         self._dict_ego_centrality = {}
#
#
#     def run(self):
#         nxgraph = build_graph_for_paths(self._triples_yielder)
#
#         for a_node in nxgraph.nodes:
#             self._dict_ego_centrality[a_node] = self._comp_ego_centrality_of_a_node(node=a_node,
#                                                                                     graph=nxgraph)
