
from classrank_io.graph.formatters.classrank.classrank_formatter_interface import ClassRankFormatterInterface, \
    KEY_ELEM, KEY_RANK_POSITION
from classranker import KEY_CLASSRANK, KEY_CLASS_POINTERS, KEY_INSTANCES
from rdflib import Namespace, RDF, Graph, URIRef, Literal, BNode, XSD

CR = Namespace("http://weso.es/classrank/")
# CR_ELEMS = Namespace("http://weso.es/classrank/entity/")
PROP_CR_SCORE = CR.score
PROP_CR_RANK = CR.rank_position
PROP_CR_N_INSTANCES = CR.num_instances
TYPE_CR_CLASS = CR.Class
TYPE_CP_HUB = CR.Classpointer_relation_hub
PROP_CLASS_HUB = CR.class_of_hub
PROP_CP_HUB = CR.classpointer_of_hub
PROP_INSTANCE_HUB = CR.instance_of_hub




class TtlClassrankFormatter(ClassRankFormatterInterface):

    def __init__(self, target_file=None, string_output=False):
        super(TtlClassrankFormatter, self).__init__()
        self._target_file = target_file
        self._string_output = string_output


    def format_classrank_dict(self, a_dict):
        sorted_list = self._sort_dict_and_add_rank(a_dict)
        self._turn_cp_dicts_into_lists(sorted_list)
        result_ttl_graph = self._build_result_ttl_graph(sorted_list)
        if self._string_output:
            return result_ttl_graph.serialize(format='turtle')
        else:
            with open(self._target_file, "w") as out_stream:
                out_stream.write(result_ttl_graph.serialize(format='turtle'))
            return "ClassRank serialized: " + self._target_file


    def _build_result_ttl_graph(self, sorted_list):
        g = Graph()
        for a_class_dict in sorted_list:
            self._add_triples_of_class_dict(g, a_class_dict)
        self._bind_namespaces(g)
        return g

    def _bind_namespaces(self, g):
        g.bind("cr", CR)
        # g.bind("cre", CR_ELEMS)

    def _add_triples_of_class_dict(self, g, class_dict):
        main_elem = URIRef(class_dict[KEY_ELEM])
        # class
        g.add( (main_elem, RDF.type, TYPE_CR_CLASS))
        # score
        g.add( (main_elem, PROP_CR_SCORE, Literal(class_dict[KEY_CLASSRANK], datatype=XSD.float)) )
        # n instances
        g.add( (main_elem, PROP_CR_N_INSTANCES, Literal(class_dict[KEY_INSTANCES], datatype=XSD.integer) ) )
        # relative rank
        g.add( (main_elem, PROP_CR_RANK, Literal(class_dict[KEY_RANK_POSITION], datatype=XSD.integer)) )
        # classpointers and instances
        self.add_triples_of_classpointers(g, main_elem, class_dict)


    def add_triples_of_classpointers(self, g, main_element, class_dict):
        for a_cp in class_dict[KEY_CLASS_POINTERS]:
            tmp = BNode()
            # class
            g.add( (tmp, PROP_CLASS_HUB, main_element) )
            # classpointer
            g.add( (tmp, PROP_CP_HUB, URIRef(a_cp)) )
            # instances
            for an_instance in class_dict[KEY_CLASS_POINTERS][a_cp]:
                g.add( (tmp, PROP_INSTANCE_HUB, URIRef(an_instance)) )


    def _turn_cp_dicts_into_lists(self, sorted_list):
        for a_class_dict in sorted_list:
            for a_cp in a_class_dict[KEY_CLASS_POINTERS]:
                a_class_dict[KEY_CLASS_POINTERS][a_cp] = list(a_class_dict[KEY_CLASS_POINTERS][a_cp])


    def _sort_dict_and_add_rank(self, classes_dict):
        for a_key in classes_dict:
            classes_dict[a_key][KEY_ELEM] = a_key
        result = list(classes_dict.values())
        result.sort(reverse=True, key=lambda x:x[KEY_CLASSRANK])
        rank_counter = 1
        for a_dict in result:
            a_dict[KEY_RANK_POSITION] = rank_counter
            rank_counter += 1
        return result

