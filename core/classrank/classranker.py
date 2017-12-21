__author__ = "Dani"
from core.pagerank.pagerank_nx import calculate_pagerank

_S = 0
_P = 1
_O = 2

KEY_INSTANCES = "INSTANCES"
KEY_CLASSRANK = "CR_score"
KEY_CLASS_POINTERS = "cps"


class ClassRanker(object):
    def __init__(self, digraph_parser, triple_yielder, classpointers_parser, classrank_formatter, damping_factor=0.85,
                 max_iter_pagerank=100, class_security_threshold=15, instantiation_security_threshold=15, max_edges=-1):
        self._graph_parser = digraph_parser
        self._triple_yielder = triple_yielder
        self._classpointer_parser = classpointers_parser
        self._damping_factor = damping_factor
        self._class_security_threshold = class_security_threshold
        self._instantiation_security_threshold = instantiation_security_threshold
        self._classrank_formatter = classrank_formatter
        self._max_edges = max_edges
        self._number_of_classes = 0
        self._number_of_entities = 0
        self._max_iter_pagerank = max_iter_pagerank

    def generate_classrank(self):
        ### Collecting inputs
        graph = self._graph_parser.parse_graph(max_edges=self._max_edges)
        classpointers_set = self._classpointer_parser.parse_classpointers()
        # damping factor (self)
        # class_threshold(self
        # inst_threshold (self)


        ### Stage 1 - PageRank
        print "stage 1"
        raw_pagerank = calculate_pagerank(graph=graph,
                                          damping_factor=self._damping_factor,
                                          max_iter=self._max_iter_pagerank)
        self._number_of_entities = len(raw_pagerank)

        ### Stage 2 - ClassDetection
        print "Stage 2"
        graph = None  # Here we do not need anymore the directed graph.
        # We must free that memory
        classes_dict = self._detect_classes(self._triple_yielder, classpointers_set, self._class_security_threshold)
        self._number_of_classes = len(classes_dict)

        ###  Stage 3 - ClassRank calculations
        print "stage 3"
        self._calculate_classrank(classes_dict, raw_pagerank, self._instantiation_security_threshold)

        ###  Outputs
        print "Outputs"
        result = self._classrank_formatter.format_classrank_dict(classes_dict, raw_pagerank)

        return result

    def _detect_classes(self, triple_yielder, classpointers, threshold):
        result = {}
        # Build dict of triples (object as primary key)
        for a_triple in triple_yielder.yield_triples(max_triples=self._max_edges):
            if a_triple[_P] in classpointers:
                if a_triple[_O] not in result:  # Adding the O to the dict in case
                    # it was not already there
                    result[a_triple[_O]] = {}
                    result[a_triple[_O]][KEY_CLASS_POINTERS] = {}
                if a_triple[_P] not in result[a_triple[_O]][KEY_CLASS_POINTERS]:  # Same with _P in _O dict
                    result[a_triple[_O]][KEY_CLASS_POINTERS][a_triple[_P]] = set()
                result[a_triple[_O]][KEY_CLASS_POINTERS][a_triple[_P]].add(a_triple[_S])

        # Now, we have to remove objects that are not classes,
        # being as kind as possible with memory consume
        keys_to_remove = set()
        for an_o_key in result:
            keep = False
            for a_p_key in result[an_o_key][KEY_CLASS_POINTERS]:
                if len(result[an_o_key][KEY_CLASS_POINTERS][a_p_key]) > threshold:
                    keep = True
                    break
            if not keep:
                keys_to_remove.add(an_o_key)

        for a_key in keys_to_remove:
            result.pop(a_key)

        # The result contains all the classes with all the instances
        # (and not instances but using classpointers) which point to them
        return result

    def _calculate_classrank(self, classes_dict, raw_pagerank, threshold):
        for a_class in classes_dict:
            # Add new keys
            classes_dict[a_class][KEY_INSTANCES] = set()
            classes_dict[a_class][KEY_CLASSRANK] = 0
            for a_p in classes_dict[a_class][KEY_CLASS_POINTERS]:
                # If it has more instances than threshold, its pagerank is added to the c's classrank
                if len(classes_dict[a_class][KEY_CLASS_POINTERS][a_p]) >= threshold:
                    for an_s in classes_dict[a_class][KEY_CLASS_POINTERS][a_p]:
                        # Each instance add its score just once
                        if an_s not in classes_dict[a_class][KEY_INSTANCES]:
                            classes_dict[a_class][KEY_INSTANCES].add(an_s)
                            classes_dict[a_class][KEY_CLASSRANK] += raw_pagerank[an_s]  # It must be there! KeyError?

            # The set of instances in no more useful. Change it by the total number of instances.
            classes_dict[a_class][KEY_INSTANCES] = len(classes_dict[a_class][KEY_INSTANCES])
        # No return needed, modyfying received param

    @property
    def triples_analized(self):
        return self._triple_yielder.yielded_triples

    @property
    def triples_with_error(self):
        return self._triple_yielder.error_triples

    @property
    def number_of_classes(self):
        return self._number_of_classes

    @property
    def number_of_entities(self):
        return self._number_of_entities
