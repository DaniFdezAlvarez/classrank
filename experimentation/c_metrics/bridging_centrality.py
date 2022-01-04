from classrank_utils.scores import normalize_score
from experimentation.c_metrics.base_c_metric import BaseCMetric, NX_COMPUTATION


class BridgingCentralityComp(BaseCMetric):

    def __init__(self, triples_yielder, degree_dict, betweeness_dict, normalize=False, max_score_degree=0,
                 max_score_betweeness=0, shortest_paths_dict=None, shortest_paths_computation=NX_COMPUTATION,
                 tunned_shortest_paths_dict=None, nxgraph=None):
        super().__init__(shortest_paths_dict=shortest_paths_dict,
                         shortest_paths_computation=shortest_paths_computation,
                         tunned_shortest_paths_dict=tunned_shortest_paths_dict,
                         nxgraph=nxgraph)
        self._triples_yielder = triples_yielder
        self._degree_dict = degree_dict
        self._betweeness_dict = betweeness_dict
        self._normalize = normalize
        self._max_score_degree = max_score_degree
        self._max_score_betweeness = max_score_betweeness

        self._bridging_dict = {}
        self._neigborhoods = self._init_neighborhoods_dict()

    def run(self, string_return=False, out_path=None):
        self._compute_neighborhoods()
        for a_node in self._degree_dict:
            self._bridging_dict[a_node] = self._comp_bridging_coefficient(a_node) * self._betweeness_dict[a_node]
        if self._normalize:
            self._normalize_scores()
        return self._return_result(obj_result=self._bridging_dict,
                                   string_return=string_return,
                                   out_path=out_path)

    def _compute_neighborhoods(self):
        if self._nxgraph is not None:
            self._compute_neigh_nxgraph()
        else:
            self._compute_neigh_t_yielder()

    def _compute_neigh_t_yielder(self):
        for a_triple in self._triples_yielder.yield_triples():
            self._neigborhoods[a_triple[0]].add(a_triple[2])
            self._neigborhoods[a_triple[2]].add(a_triple[0])

    def _compute_neigh_nxgraph(self):
        for a_node in self._nxgraph.nodes:  # If we are here, nxgraph cant be None
            self._neigborhoods[a_node] = set(self._nxgraph.neighbors(a_node))

    def _init_neighborhoods_dict(self):
        result = {}
        for a_node in self._degree_dict:
            result[a_node] = set()
        return result



    def _comp_bridging_coefficient(self, node):
        if len(self._neigborhoods[node]) == 0:
            return 0
        numerator = float(1) / self._degree_dict[node]
        denominator = 0
        for a_neig in self._neigborhoods[node]:
            denominator += float(1) / self._degree_dict[a_neig]
        return numerator / denominator

    def _normalize_scores(self):
        # max_score = self._max_bridging_centrality() * self._max_score_betweeness
        max_score = max([self._bridging_dict[a_node] for a_node in self._bridging_dict])
        for a_node in self._bridging_dict:
            self._bridging_dict[a_node] = normalize_score(score=self._bridging_dict[a_node], max_score=max_score)


    def _max_bridging_centrality(self):
        return self._max_score_betweeness # TODO : is this really the max score for br_centrality?

