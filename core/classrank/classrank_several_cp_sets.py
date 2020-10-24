from core.classrank.classranker import ClassRanker, KEY_CLASS_POINTERS, \
    _S, _P, _O  # We accept octopus as domestic animal.... this is python!


class ClassRankerSeveralCpSets(ClassRanker):

    def __init__(self, digraph_parser, triple_yielder, classpointers_sets, classrank_formatter, set_target_classes,
                 damping_factor=0.85, max_iter_pagerank=100, max_edges=-1, pagerank_scores=None):
        super().__init__(digraph_parser=digraph_parser,
                         triple_yielder=triple_yielder,
                         classpointers_parser=None,  # there are different sets of classpointers known a priori
                         classrank_formatter=classrank_formatter,
                         damping_factor=damping_factor,
                         max_iter_pagerank=max_iter_pagerank,
                         threshold=1,  # Classes are known a priori as well
                         max_edges=max_edges,
                         pagerank_scores=pagerank_scores)

        self._classpointers_sets = classpointers_sets
        self.set_target_classes = set_target_classes

    def _detect_classes(self, triple_yielder, classpointers, threshold):
        result = self._generate_initial_class_result_dict()
        # Build dict of triples (object as primary key)
        for a_triple in triple_yielder.yield_triples(max_triples=self._max_edges):
            if a_triple[_P] in classpointers and a_triple[_O] in self.set_target_classes:
                if a_triple[_P] not in result[a_triple[_O]][KEY_CLASS_POINTERS]:  # Same with _P in _O dict
                    result[a_triple[_O]][KEY_CLASS_POINTERS][a_triple[_P]] = set()
                result[a_triple[_O]][KEY_CLASS_POINTERS][a_triple[_P]].add(a_triple[_S])
        return result

    def _generate_initial_class_result_dict(self):
        result = {}
        for a_class in self.set_target_classes:
            result[a_class] = {}
            result[a_class][KEY_CLASS_POINTERS] = {}
        return result

    # TODO:
    # -
    # - Build a set containing ALL the classpointers of every set.
    # - Annotate instances for them all in _detect_classes
    # - Produce a different classrank score for eahc set, considering for each set the corresponding
    #       classpointers and ignoring the rest
    #
    # DONE - Redefine as well the part in which the algorithm looks for classes. Classes are known a priori
    # DONE - Enjoy the life man!
    