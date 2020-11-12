from rdflib.graph import Graph, URIRef, Literal, BNode
from classrank_io.graph.yielders.triples_yielder_interface import TriplesYielderInterface
from core.consts import N3, TURTLE, RDF_XML, NT, JSON_LD

_SUPPORTED_FORMATS = [N3, TURTLE, RDF_XML, NT, JSON_LD]

_XML_WRONG_URI = "http://www.w3.org/XML/1998/namespace"

class RdflibTripleYielder(TriplesYielderInterface):

    def __init__(self, input_format=TURTLE, source=None, allow_untyped_numbers=False,
                 raw_graph=None, namespaces_dict=None, filtering_function=None):
        """

        :param input_format:
        :param source: It can be local (a file path) or remote (an url to download some content)
        :param namespaces_to_ignore:
        :param allow_untyped_numbers:
        :param raw_graph:
        :param namespaces_dict:
        """
        super().__init__()
        self._check_input_format(input_format)

        self._input_format = input_format
        self._source = source
        self._allow_untyped_numbers = allow_untyped_numbers
        self._raw_graph = raw_graph
        self._namespaces_dict = namespaces_dict if namespaces_dict is not None else {}
                                              # This object can be modified (and will be consumed externaly)
                                              # when parse_namespaces in yiled_triples() is set to True

        self._triples_count = 0

        self._prefixes_parsed = False

        if filtering_function is not None:
            self._is_relevant_triple = filtering_function


    def yield_triples(self, parse_namespaces=True):
        self._reset_count()
        tmp_graph = self._get_tmp_graph()
        if parse_namespaces:
            self._integrate_namespaces_from_parsed_graph(tmp_graph, self._namespaces_dict)
            self._prefixes_parsed = True
        for sub,pred,obj in tmp_graph:
            if self._is_relevant_triple((sub, pred, obj)):
                yield (
                    str(sub), str(pred), str(obj)
                )
                self._triples_count += 1

    def _is_relevant_triple(self, triple):
        return True

    def _get_tmp_graph(self):
        result = Graph()
        if self._source is not None:
            result.parse(source=self._source, format=self._input_format)
        else:
            result.parse(data=self._raw_graph, format=self._input_format)
        return result

    @staticmethod
    def _integrate_namespaces_from_parsed_graph(a_graph, namespaces_dict):

        for a_prefix_namespace_tuple in a_graph.namespaces():
            candidate_uri = str(a_prefix_namespace_tuple[1])
            if candidate_uri not in namespaces_dict:
                if candidate_uri == _XML_WRONG_URI:  # XML fix...
                    candidate_uri += "/"             # XML fix...
                namespaces_dict[candidate_uri] = str(a_prefix_namespace_tuple[0])
            # There is no else here. In case of conflict between the parsed content and the dict provided by the user,
            # the user's one have priority


    @staticmethod
    def _check_input_format(input_format):
        if input_format not in _SUPPORTED_FORMATS:
            raise ValueError("Unsupported input format: " + input_format)

    @property
    def yielded_triples(self):
        return self._triples_count

    @property
    def error_triples(self):
        return 0  # With rdflib, a single error will cause to fail the parsing process


    @property
    def namespaces(self):
        if not self._prefixes_parsed:
            tmp_graph = self._get_tmp_graph()
            self._integrate_namespaces_from_parsed_graph(tmp_graph, self._namespaces_dict)
            self._prefixes_parsed = True
        return self._namespaces_dict


    def _reset_count(self):
        self._triples_count = 0




