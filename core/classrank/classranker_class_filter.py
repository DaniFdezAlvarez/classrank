__author__ = "Dani"
from classrank_utils.prefix import build_dict_of_prefixes_from_tuples
from core.classrank.classranker import ClassRanker, KEY_CLASS_POINTERS, \
    _S, _P, _O  # We accept octopus as domestic animal.... this is python!



class ClassrankerClassFilter(ClassRanker):
    def __init__(self, digraph_parser, triple_yielder, classpointers_parser, classrank_formatter,
                 prefix_tuples, list_of_target_classes, damping_factor=0.85, max_iter_pagerank=100, max_edges=-1, pagerank_scores=None):
        super(ClassrankerClassFilter, self).__init__(digraph_parser=digraph_parser,
                                                     triple_yielder=triple_yielder,
                                                     classpointers_parser=classpointers_parser,
                                                     classrank_formatter=classrank_formatter,
                                                     damping_factor=damping_factor,
                                                     max_iter_pagerank=max_iter_pagerank,
                                                     threshold=1,  # Classes are already known
                                                     max_edges=max_edges,
                                                     pagerank_scores=pagerank_scores)
        self._set_target_classes = set(list_of_target_classes)
        self._prefixes = build_dict_of_prefixes_from_tuples(prefix_tuples, inverse=False)
        self._inverse_prefixes = build_dict_of_prefixes_from_tuples(prefix_tuples, inverse=True)
        # self._number_of_classes = 0
        # self._number_of_entities = 0


    def _detect_classes(self, triple_yielder, classpointers, threshold):
        result = self._generate_initial_class_result_dict()
        # Build dict of triples (object as primary key)
        for a_triple in triple_yielder.yield_triples(max_triples=self._max_edges):
            if a_triple[_P] in classpointers:
                canonized_target_class = self._canonize_target_class_if_is_target(a_triple[_O])
                if canonized_target_class is not None:
                    if a_triple[_P] not in result[canonized_target_class][
                        KEY_CLASS_POINTERS]:  # Same with _P in _O dict
                        result[canonized_target_class][KEY_CLASS_POINTERS][a_triple[_P]] = set()
                    result[canonized_target_class][KEY_CLASS_POINTERS][a_triple[_P]].add(a_triple[_S])

        # No need to remove any keys. Classes have already been positively identified

        # The result contains all the classes with all the instances
        # (and not instances but using classpointers) which point to them
        return result

    def _canonize_target_class_if_is_target(self, candidate_class):
        if candidate_class in self._set_target_classes:
            return candidate_class

        if candidate_class.startswith("http://"):
            index_key_char = candidate_class.index("#") if "#" in candidate_class else candidate_class.rindex("/")
            if candidate_class[:index_key_char + 1] in self._inverse_prefixes:
                class_with_prefix = self._inverse_prefixes[
                                        candidate_class[:index_key_char + 1]] + ":" + candidate_class[
                                                                                      index_key_char + 1:]
                if class_with_prefix in self._set_target_classes:
                    return class_with_prefix
            return None
        else:  # it starts with a prefix
            index_key_char = candidate_class.index(":")
            if candidate_class[:index_key_char] in self._prefixes:
                whole_class = self._prefixes[candidate_class[:index_key_char]] + candidate_class[index_key_char + 1:]
                if whole_class in self._set_target_classes:
                    return whole_class
            return None


    def _generate_initial_class_result_dict(self):
        result = {}
        for a_class in self._set_target_classes:
            result[a_class] = {}
            result[a_class][KEY_CLASS_POINTERS] = {}
        return result

