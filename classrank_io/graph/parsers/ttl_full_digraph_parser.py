from classrank_io.graph.parsers.digraph_parser_inferface import DiGraphParserInterface
import networkx as nx
from rdflib import Graph, term
_SEPARATOR = " "


class TtlFullDigraphParser(DiGraphParserInterface):

    def __init__(self, source_file=None, string_graph=None, source_format="n3"):
        super(TtlFullDigraphParser, self).__init__()
        self._source_file = source_file
        self._string_graph = string_graph
        self._triple_count = 0
        self._error_count = 0
        self._ignored = 0
        self._format = source_format

    def parse_graph(self, max_edges=-1):
        self._reset_count()
        result = nx.DiGraph()
        rdfgraph = Graph()
        if self._source_file is not None:
            rdfgraph.parse(self._source_file, format=self._format)
        else:
            rdfgraph.parse(data=self._string_graph, format=self._format)

        for s,o in rdfgraph.subject_objects():
            if type(s) == term.URIRef and type(o) == term.URIRef:
                result.add_edge(str(s), str(o))
                self._triple_count += 1
                if self.parsed_triples == max_edges:
                    break
            else:
                self._ignored += 1
        return result



    @property
    def ignored_triples(self):  # Just in this parser... should it be in other ones?
        return self._ignored

    @property
    def parsed_triples(self):
        return self._triple_count

    @property
    def error_triples(self):
        return self._error_count

    def _reset_count(self):
        self._error_count = 0
        self._triple_count = 0
        self._ignored = 0
