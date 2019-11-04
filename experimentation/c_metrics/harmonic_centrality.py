from classrank_utils.g_paths import build_graph_for_paths, shortest_path
from classrank_utils.scores import normalize_score
from experimentation.c_metrics.base_c_metric import BaseCMetric

class HarmonicCentralityComp(BaseCMetric):

    def __init__(self, triples_yielder, normalize=False):
        self._triples_yielder = triples_yielder
        self._normalize = normalize
        self._harmonic_dict = {}



    def run(self, string_return=True, out_path=None):
        nxgraph = build_graph_for_paths(self._triples_yielder)
        for a_node in nxgraph.nodes:
            denominator = 0
            for a_node_2 in nxgraph.nodes:
                if a_node != a_node_2:
                    s_path = shortest_path(origin=a_node,
                                           destination=a_node_2,
                                           graph=nxgraph)
                    denominator += len(s_path)
            self._harmonic_dict[a_node] = float(1) / denominator
        if self._normalize:
            max_score = float(1) / (len(nxgraph) - 1)
            self._normalize_dict(max_score)
        return self._return_result(obj_result=self._harmonic_dict,
                                   string_return=string_return,
                                   out_path=out_path)


    def _normalize_dict(self, max_score):
        for an_uri in self._harmonic_dict:
            self._harmonic_dict[an_uri] = normalize_score(score=self._harmonic_dict[an_uri],
                                                          max_score=max_score)


