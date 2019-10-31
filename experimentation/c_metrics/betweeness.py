from classrank_utils.g_paths import build_graph_for_paths, shortest_path
from classrank_utils.scores import normalize_score
from classrank_io.json_io import json_obj_to_string, write_obj_to_json


class BetweenessComp(object):

    def __init__(self, triples_yielder, target_nodes, normalize=False):
        self._triples_yielder = triples_yielder
        self._normalize = normalize
        self._target_nodes = target_nodes
        self._dict_count = None


    def run(self, string_return=True, out_path=None):
        self._init_dict_count()
        nxgraph = build_graph_for_paths(self._triples_yielder)
        every_path = shortest_path(graph=nxgraph)
        for a_node in self._dict_count:
            for a_path in every_path:
                if a_node in a_path:
                    self._dict_count[a_node] += 1
        if self._normalize:
            max_score = len(every_path)
            self._normalize_dict_count(max_score)
        return self._return_result(string_return, out_path)

    def _normalize_dict_count(self, max_score):
        for an_uri in self._dict_count:
            self._dict_count[an_uri] = normalize_score(score=self._dict_count[an_uri],
                                                       max_score=max_score)


    def _return_result(self, string_return, out_path):
        if out_path is not None:
            write_obj_to_json(target_obj=self._dict_count, out_path=out_path, indent=2)
        if string_return:
            return json_obj_to_string(target_obj=self._dict_count, indent=2)
        return None


    def _init_dict_count(self):
        self._dict_count = {}
        for a_node in self._target_nodes:
            self._dict_count[a_node] = 0

