from rdflib import Graph, RDF, OWL, RDFS
from experimentation.dbpedia.query_mining.domran_tracker import _DOMAIN_KEY, _RANGE_KEY


class OntologyAnalyser(object):

    def __init__(self, ontology_source_file):
        self._source_file = ontology_source_file
        self._onto_graph = self._load_onto_graph()

    def list_of_classes(self, strings=True):
        result = []
        for s, p, o in self._onto_graph.triples((None, RDF.type, OWL.Class)):
            result.append(s)
        if strings:
            result = self._stringify_obj_list(result)
        return result

    def domrans_of_target_classes(self, target_classes):
        result = {}
        for a_target_class in target_classes:
            self._add_doms_of_class(result_dict=result,
                                    target_class=a_target_class)
            self._add_rans_of_class(result_dict=result,
                                    target_class=a_target_class)
        self._jsonize_obj_dict(result)
        return result

    def _add_doms_of_class(self, result_dict, target_class):
        self._add_domran_of_class(result_dict=result_dict,
                                  dom_or_ran_key=_DOMAIN_KEY,
                                  dom_or_ran_property=RDFS.domain,
                                  target_class=target_class)

    def _add_rans_of_class(self, result_dict, target_class):
        self._add_domran_of_class(result_dict=result_dict,
                                  dom_or_ran_key=_RANGE_KEY,
                                  dom_or_ran_property=RDFS.range,
                                  target_class=target_class)

    def _jsonize_obj_dict(self, target_dict):
        for a_target_prop, domran_dict in target_dict.items():
            for a_domran_key in domran_dict:
                domran_dict[a_domran_key] = list(domran_dict[a_domran_key])

    def _add_domran_of_class(self, result_dict, dom_or_ran_key, dom_or_ran_property, target_class):
        for s, p, o in self._onto_graph.triples((None, dom_or_ran_property, target_class)):
            target_prop = str(s)
            if target_prop not in result_dict:
                self._initialize_prop_entry(result_dict, target_prop)
            result_dict[target_prop][dom_or_ran_key].add(str(target_class))

    def _initialize_prop_entry(self, result_dict, target_prop):
        result_dict[str(target_prop)] = {_RANGE_KEY: set(),
                                         _DOMAIN_KEY: set()}

    def _stringify_obj_list(self, target_list):
        return [str(elem) for elem in target_list]

    def _load_onto_graph(self):
        result = Graph()
        result.parse(self._source_file, format="turtle")
        return result
