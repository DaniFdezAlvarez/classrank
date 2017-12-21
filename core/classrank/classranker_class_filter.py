__author__ = "Dani"
from classrank_utils.prefix import build_dict_of_prefixes_from_tuples
from core.classrank.classranker import ClassRanker, KEY_CLASS_POINTERS, \
    _S, _P, _O  # We accept octopus as domestic animal.... this is python!



class ClassrankerClassFilter(ClassRanker):
    def __init__(self, digraph_parser, triple_yielder, classpointers_parser, classrank_formatter,
                 prefix_tuples, list_of_target_classes, damping_factor=0.85, max_iter_pagerank=100,
                 instantiation_security_threshold=15, max_edges=-1):
        super(ClassrankerClassFilter, self).__init__(digraph_parser=digraph_parser,
                                                     triple_yielder=triple_yielder,
                                                     classpointers_parser=classpointers_parser,
                                                     classrank_formatter=classrank_formatter,
                                                     damping_factor=damping_factor,
                                                     max_iter_pagerank=max_iter_pagerank,
                                                     class_security_threshold=1,  # Classes are already known
                                                     instantiation_security_threshold=instantiation_security_threshold,
                                                     max_edges=max_edges)
        self._set_target_classes = set(list_of_target_classes)
        self._prefixes = build_dict_of_prefixes_from_tuples(prefix_tuples, inverse=False)
        self._inverse_prefixes = build_dict_of_prefixes_from_tuples(prefix_tuples, inverse=True)
        # self._number_of_classes = 0
        # self._number_of_entities = 0


    def _detect_classes(self, triple_yielder, classpointers, threshold):
        print "Eyyyyy look how I am being executed buddy!"
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

        # keys_to_remove = set()
        # for an_o_key in result:
        #     keep = False
        #     for a_p_key in result[an_o_key][KEY_CLASS_POINTERS]:
        #         if len(result[an_o_key][KEY_CLASS_POINTERS][a_p_key]) > threshold:
        #             keep = True
        #             break
        #     if not keep:
        #         keys_to_remove.add(an_o_key)
        #
        # for a_key in keys_to_remove:
        #     result.pop(a_key)

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

