from classrank_utils.uri import remove_corners
from classrank_utils.scores import normalize_score
from experimentation.c_metrics.base_c_metric import BaseCMetric, NX_COMPUTATION
from classrank_utils.g_paths import build_graph_for_paths

_S = 0
_P = 1
_O = 2

class DegreeComp(BaseCMetric):

    def __init__(self, triples_yielder, target_nodes, normalize=False, shortest_paths_dict=None, shortest_paths_computation=NX_COMPUTATION,
                 nxgraph=None, tunned_shortest_paths_dict=None):
        super().__init__(shortest_paths_dict=shortest_paths_dict,
                         shortest_paths_computation=shortest_paths_computation,
                         nxgraph=nxgraph,
                         tunned_shortest_paths_dict=tunned_shortest_paths_dict)
        self._triples_yielder = triples_yielder
        self._target_nodes = [remove_corners(an_uri, raise_error=False) for an_uri in target_nodes]
        self._normalize = normalize
        self._dict_count = None
        self._max_score = 0  # TODO Really wrong until someone executes run()

    def _init_dict_count(self):
        self._dict_count = {}
        for a_node in self._target_nodes:
            self._dict_count[a_node] = 0

    @property
    def max_score(self):
        return self._max_score

    def run(self, string_return=True, out_path=None):
        self._init_dict_count()
        nxgraph = build_graph_for_paths(self._triples_yielder) if self._nxgraph is None else self._nxgraph
        # self._max_score = len(nxgraph) - 1  # Setting up max_score
        for a_node in nxgraph.nodes:
            self._dict_count[a_node] = nxgraph.degree[a_node]
        if self._normalize:
            self._max_score = self._find_max_score()
            self._normalize_dict_counts()
        return self._return_result(obj_result=self._dict_count,
                                   string_return=string_return,
                                   out_path=out_path)

        # different_nodes = set()
        # for a_triple in self._triples_yielder.yield_triples():
        #     if a_triple[_O] in self._dict_count:
        #         self._dict_count[a_triple[_O]] += 1
        #     if a_triple[_S] in self._dict_count:
        #         self._dict_count[a_triple[_S]] += 1
        #     if self._normalize:
        #         different_nodes.add(a_triple[_S])
        #         different_nodes.add(a_triple[_O])
        # if self._normalize:
        #     self._normalize_dict_counts(len(different_nodes))
        # return self._return_result(obj_result=self._dict_count,
        #                            string_return=string_return,
        #                            out_path=out_path)

    def _find_max_score(self):
        return max([self._dict_count[a_node] for a_node in self._dict_count])

    def _normalize_dict_counts(self):
        for an_uri in self._dict_count:
            self._dict_count[an_uri] = normalize_score(score=self._dict_count[an_uri],
                                                       max_score=self.max_score)


    # def _is_relevant_triple(self, a_triple):
    #     print(a_triple[_O], self._dict_count)
    #     if a_triple[_O] in self._dict_count or a_triple[_S] in self._dict_count:
    #         return True
    #     return False
