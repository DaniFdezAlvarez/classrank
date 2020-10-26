import sys
from core.classrank.classranker import ClassRanker, KEY_CLASS_POINTERS, \
    _S, _P, _O, KEY_INSTANCES, KEY_CLASSRANK, KEY_UNDER_T_CLASS_POINTERS


class ClassRankerSeveralCpSets(ClassRanker):

    def __init__(self, triple_yielder, classpointers_sets, classrank_formatter, set_target_classes,
                 pagerank_scores, max_edges=-1):
        super().__init__(digraph_parser=None,  # Not needed, thats for pagerank.
                         triple_yielder=triple_yielder,
                         classpointers_parser=None,  # there are different sets of classpointers known a priori
                         classrank_formatter=classrank_formatter,
                         damping_factor=0.85,  # wont be used
                         max_iter_pagerank=100,  #  wont be used
                         threshold=1,  # Classes are known a priori as well
                         max_edges=max_edges,
                         pagerank_scores=pagerank_scores)

        self._classpointers_sets = classpointers_sets
        self.set_target_classes = set_target_classes


    def generate_classrank(self):
        ### Collecting inputs
        self._pagerank_scores
        classpointers_set = self._build_cp_superset()
        # damping factor (self)
        # threshold (self)


        ### Stage 1 - PageRank

        # Already known
        self._number_of_entities = len(self._pagerank_scores)

        ### Stage 2 - ClassDetection
        print("Stage 2")
        sys.stdout.flush()
        # We must free that memory
        classes_dict = self._detect_classes(self._triple_yielder, classpointers_set, self._threshold)
        self._number_of_classes = len(classes_dict)

        ###  Stage 3 - ClassRank calculations
        print("stage 3")
        sys.stdout.flush()
        self._calculate_classrank(classes_dict=classes_dict,
                                  raw_pagerank=self._pagerank_scores,
                                  threshold=self._threshold)

        ###  Outputs
        print("Outputs")
        sys.stdout.flush()
        result = self._classrank_formatter.format_classrank_dict(classes_dict, raw_pagerank)

        return result

    def _calculate_classrank(self, classes_dict, raw_pagerank, threshold):
        for a_class in classes_dict:
            # Add new keys
            # classes_dict[a_class][KEY_INSTANCES] = set()
            classes_dict[a_class][KEY_CLASSRANK] = 0
            classes_dict[a_class][KEY_UNDER_T_CLASS_POINTERS] = {}
            under_threshold_props = []
            for a_p in classes_dict[a_class][KEY_CLASS_POINTERS]:
                # If it has more instances than threshold, its pagerank is added to the c's classrank
                if len(classes_dict[a_class][KEY_CLASS_POINTERS][a_p]) >= threshold:
                    for an_s in classes_dict[a_class][KEY_CLASS_POINTERS][a_p]:
                        # Each instance add its score just once
                        if an_s not in classes_dict[a_class][KEY_INSTANCES]:
                            classes_dict[a_class][KEY_INSTANCES].add(an_s)
                            classes_dict[a_class][KEY_CLASSRANK] += raw_pagerank[an_s]
                # else:
                #
                #     # print(a_p, classes_dict[a_class][KEY_CLASS_POINTERS][a_p])
                #     under_threshold_props.append((a_p, classes_dict[a_class][KEY_CLASS_POINTERS][a_p]))
                #     # target_obj = classes_dict[a_class][KEY_CLASS_POINTERS][a_p]
                #     # del classes_dict[a_class][KEY_CLASS_POINTERS][a_p]
                #     # classes_dict[a_class][KEY_UNDER_T_CLASS_POINTERS][a_p] = target_obj

            for a_low_p in under_threshold_props:
                del classes_dict[a_class][KEY_CLASS_POINTERS][a_low_p[0]]
                classes_dict[a_class][KEY_UNDER_T_CLASS_POINTERS][a_low_p[0]] = a_low_p[1]

            # The set of instances in no more useful. Change it by the total number of instances.
            classes_dict[a_class][KEY_INSTANCES] = len(classes_dict[a_class][KEY_INSTANCES])
        # No return needed, modyfying received param

    def _build_cp_superset(self):
        result = set()
        for a_cp_list in self._classpointers_sets:
            for a_cp in a_cp_list:
                result.add(a_cp)
        return result

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
    # - DONE Build a set containing ALL the classpointers of every set.
    # - Annotate instances for them all in _detect_classes
    # - Produce a different classrank score for eahc set, considering for each set the corresponding
    #       classpointers and ignoring the rest
    #
    # DONE - Redefine as well the part in which the algorithm looks for classes. Classes are known a priori
    # DONE - Enjoy the life man!

