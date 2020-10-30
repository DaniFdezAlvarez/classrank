from classrank_utils.g_paths import build_graph_for_paths
from classrank_utils.scores import normalize_score
from experimentation.c_metrics.base_c_metric import BaseCMetric, NX_COMPUTATION


class BetweenessComp(BaseCMetric):

    def __init__(self, triples_yielder, target_nodes, normalize=False, shortest_paths_dict=None,
                 shortest_paths_computation=NX_COMPUTATION, nxgraph=None, tunned_shortest_paths_dict=None):
        super().__init__(shortest_paths_dict=shortest_paths_dict,
                         shortest_paths_computation=shortest_paths_computation,
                         nxgraph=nxgraph,
                         tunned_shortest_paths_dict=tunned_shortest_paths_dict)
        self._triples_yielder = triples_yielder
        self._normalize = normalize
        self._target_nodes = target_nodes
        self._dict_count = None
        self._max_score = 0  # TODO Really wrong until someone executes run()

    @property
    def max_score(self):
        return self._max_score


    def run(self, string_return=True, out_path=None):
        self._init_dict_count()
        nxgraph = build_graph_for_paths(self._triples_yielder) if self._nxgraph is None else self._nxgraph
        every_path_dict = self._get_shortest_paths(nxgraph)
        every_path = self._list_of_relevant_paths(every_path_dict)
        for a_node in self._dict_count:
            for a_path in every_path:
                if a_node in a_path:
                    self._dict_count[a_node] += 1
        if self._normalize:
            self._max_score = self._find_max_score()
            self._normalize_dict_count()
        return self._return_result(obj_result=self._dict_count,
                                   string_return=string_return,
                                   out_path=out_path)

    def _find_max_score(self):
        return max([self._dict_count[an_uri] for an_uri in self._dict_count])

    def _normalize_dict_count(self):
        for an_uri in self._dict_count:
            self._dict_count[an_uri] = normalize_score(score=self._dict_count[an_uri],
                                                       max_score=self._max_score)

    def _init_dict_count(self):
        self._dict_count = {}
        for a_node in self._target_nodes:
            self._dict_count[a_node] = 0

    def _list_of_relevant_paths(self, every_path_dict):
        result = []
        for origin_key in every_path_dict:
            for destination_key in every_path_dict[origin_key]:
                a_path = every_path_dict[origin_key][destination_key]
                if len(a_path) > 2:
                    result.append(a_path[1:-1])
        return result

