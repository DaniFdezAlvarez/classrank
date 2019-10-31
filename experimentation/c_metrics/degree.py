from classrank_utils.uri import remove_corners
from classrank_io.json_io import json_obj_to_string, write_obj_to_json
from classrank_utils.scores import normalize_score

_S = 0
_P = 1
_O = 2

class DegreeComp(object):

    def __init__(self, triples_yielder, target_nodes, normalize=False):
        self._triples_yielder = triples_yielder
        self._target_nodes = [remove_corners(an_uri, raise_error=False) for an_uri in target_nodes]
        self._normalize = normalize
        self._dict_count = None

    def _init_dict_count(self):
        self._dict_count = {}
        for a_node in self._target_nodes:
            self._dict_count[a_node] = 0

    def run(self, string_return=True, out_path=None):
        self._init_dict_count()
        different_nodes = set()
        for a_triple in self._triples_yielder.yield_triples():
            if self._is_relevant_triple(a_triple):
                self._dict_count[a_triple[_O]] += 1
            if self._normalize:
                different_nodes.add(a_triple[_S])
                different_nodes.add(a_triple[_O])
        if self._normalize:
            self._normalize_dict_counts(len(different_nodes))
        return self._return_result(string_return, out_path)

    def _normalize_dict_counts(self, max_score):
        for an_uri in self._dict_count:
            self._dict_count[an_uri] = normalize_score(score=self._dict_count[an_uri],
                                                       max_score=max_score)

    def _return_result(self, string_return, out_path):
        if out_path is not None:
            write_obj_to_json(target_obj=self._dict_count, out_path=out_path, indent=2)
        if string_return:
            return json_obj_to_string(target_obj=self._dict_count, indent=2)
        return None

    def _is_relevant_triple(self, a_triple):
        if a_triple[_O] in self._dict_count:
            return True
        return False
