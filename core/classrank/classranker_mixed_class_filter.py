"""
This ClassRanker is thought to analyze a graphic in which there are classes in several workspaces.
The target classes are known a priori in some of those workspaces, but they are tracked through
the classpointers in some others.


"""
from core.classrank.classranker import ClassRanker, KEY_CLASS_POINTERS, \
    _S, _P, _O
from classrank_utils.prefix import build_dict_of_prefixes_from_tuples

_UNPREFIXED_URI_BEG = "http://"

class ClassRankerMixedClassFilter(ClassRanker):

    def __init__(self, digraph_parser, triple_yielder, classpointers_parser, classrank_formatter,
                 prefix_tuples, list_of_target_classes, known_namespaces_list,
                 damping_factor=0.85, max_iter_pagerank=100, threshold=15, max_edges=-1):
        super(ClassRankerMixedClassFilter, self).__init__(digraph_parser=digraph_parser,
                                                          triple_yielder=triple_yielder,
                                                          classpointers_parser=classpointers_parser,
                                                          classrank_formatter=classrank_formatter,
                                                          damping_factor=damping_factor,
                                                          max_iter_pagerank=max_iter_pagerank,
                                                          threshold=threshold,
                                                          max_edges=max_edges)
        self._known_namespaces = known_namespaces_list
        self._set_target_classes = set(list_of_target_classes)
        self._prefixes = build_dict_of_prefixes_from_tuples(prefix_tuples, inverse=False)
        self._inverse_prefixes = build_dict_of_prefixes_from_tuples(prefix_tuples, inverse=True)



    def _detect_classes(self, triple_yielder, classpointers, threshold):
        result = self._generate_initial_class_result_dict()
        for a_triple in triple_yielder.yield_triples(max_triples=self._max_edges):
            if a_triple[_P] in classpointers:
                if self._is_class_from_a_known_workspace(a_triple[_O]):
                    # print "CONOCIDA!!!", a_triple[_O]
                    self._manage_class_of_known_workspace(class_dict=result,
                                                          a_class=a_triple[_O],
                                                          a_prop=a_triple[_P],
                                                          a_subj=a_triple[_S])
                else:
                    # print "No conocida...", a_triple[_O]
                    self._manage_class_of_not_known_workspace(class_dict=result,
                                                              a_class=a_triple[_O],
                                                              a_prop=a_triple[_P],
                                                              a_subj=a_triple[_S])

        self._remove_classes_not_enough_relevant(result, threshold)
        return result


    def _manage_class_of_not_known_workspace(self, class_dict, a_class, a_prop, a_subj):
        canonized_target_class = self._canonize_target_class_if_is_target(a_class)
        if canonized_target_class is not None:
            # print("UNA ME PASO EL CORTE!", a_class)
            if a_prop not in class_dict[canonized_target_class][KEY_CLASS_POINTERS]:
                class_dict[canonized_target_class][KEY_CLASS_POINTERS][a_prop] = set()
            class_dict[canonized_target_class][KEY_CLASS_POINTERS][a_prop].add(a_subj)



    def _manage_class_of_known_workspace(self, class_dict, a_class, a_prop, a_subj):
        if a_class not in class_dict:  # Adding the O to the dict in case
            class_dict[a_class] = {}
            class_dict[a_class][KEY_CLASS_POINTERS] = {}
        if a_prop not in class_dict[a_class][KEY_CLASS_POINTERS]:  # Same with _P in _O dict
            class_dict[a_class][KEY_CLASS_POINTERS][a_prop] = set()
        class_dict[a_class][KEY_CLASS_POINTERS][a_prop].add(a_subj)



    def _is_class_from_a_known_workspace(self, a_class):
        if self._is_a_prefixed_element(a_class):
            a_class = self._unprefixize_class_if_possible(a_class)

        if a_class is None:
            return False

        for a_known_workspace in self._known_namespaces:
            if a_class.startswith(a_known_workspace):
                return True
        return False


    def _is_a_prefixed_element(self, a_class):
        return not a_class.startswith(_UNPREFIXED_URI_BEG)


    def _remove_classes_not_enough_relevant(self, class_dict, threshold):
        """
        It modifies the result received as param, no return
        :param class_dict:
        :param threshold:
        :return:
        """
        # Now, we have to remove objects that are not classes,
        # being as kind as possible with memory consume
        keys_to_remove = set()
        for an_o_key in class_dict:
            keep = False
            for a_p_key in class_dict[an_o_key][KEY_CLASS_POINTERS]:
                if len(class_dict[an_o_key][KEY_CLASS_POINTERS][a_p_key]) > threshold:
                    keep = True
                    break
            if not keep:
                keys_to_remove.add(an_o_key)

        for a_key in keys_to_remove:
            class_dict.pop(a_key)



    def _canonize_target_class_if_is_target(self, candidate_class):  # TODO refactor!
        # if "dbpedia" in candidate_class:
        #     print(candidate_class)
        if candidate_class in self._set_target_classes:
            return candidate_class

        modified_class = self._unprefixize_class_if_possible(candidate_class) \
            if self._is_a_prefixed_element(candidate_class) \
            else self._prefixize_class_if_possible(candidate_class)
        if modified_class is None:
            return None
        elif modified_class in self._set_target_classes:
            return modified_class
        return None



    def _prefixize_class_if_possible(self, a_class):
        """
        Return the class prefixed if the namespace is known.
        Otherwhise, return None
        :param a_class:
        :return:
        """
        index_key_char = a_class.index("#") if "#" in a_class else a_class.rindex("/")
        if a_class[:index_key_char + 1] in self._inverse_prefixes:
            return self._inverse_prefixes[a_class[:index_key_char + 1]] + ":" + a_class[index_key_char + 1:]
        return None


    def _unprefixize_class_if_possible(self, a_class):
        """
        Return the class with the whole namespace if the namespace is known.
        Otherwhise, return None
        :param a_class:
        :return:
        """
        index_key_char = a_class.index(":")
        if a_class[:index_key_char] in self._prefixes:
            return self._prefixes[a_class[:index_key_char]] + a_class[index_key_char + 1:]
        return a_class


    def _generate_initial_class_result_dict(self):  # TODO refactor, shared between classrankers
        result = {}
        for a_class in self._set_target_classes:
            result[a_class] = {}
            result[a_class][KEY_CLASS_POINTERS] = {}
        return result

