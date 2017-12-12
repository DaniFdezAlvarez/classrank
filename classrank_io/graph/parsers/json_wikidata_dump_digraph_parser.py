from classrank_io.graph.yielders.json_wikidata_dump_triples_yielder import JsonWikidataDumpTriplesYielder
from classrank_io.graph.parsers.digraph_parser_inferface import DiGraphParserInterface
import networkx as nx


class JsonWikidataDumpDiGraphParser(DiGraphParserInterface):

    def __init__(self, source_file):
        super(JsonWikidataDumpDiGraphParser, self).__init__()
        # self._source_file = source_file
        self._yielder = JsonWikidataDumpTriplesYielder(source_file)

    def parse_graph(self, max_edges=-1):
        self._reset_count()
        result = nx.DiGraph()
        for a_triple in self._yielder.yield_triples(max_triples=max_edges):
            result.add_edge(a_triple[0], a_triple[2])  # subject, object
        return result

    @property
    def parsed_triples(self):
        return self._yielder.yielded_triples

    @property
    def error_triples(self):
        return self._yielder.error_triples

    @property
    def ignored_triples(self):
        return self._yielder.ignored_triples

    def _reset_count(self):
        self._yielder._reset_count()