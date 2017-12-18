import networkx as nx
from classrank_io.graph.parsers.digraph_parser_inferface import DiGraphParserInterface
from classrank_io.graph.yielders.several_ttl_full_files_memory_kind_triples_yielder import \
    SeveralTtlFullFilesMemoryKindTriplesYielder


class SeveralTtlFullFilesMemoryKindDigraphParser(DiGraphParserInterface):

    def __init__(self, list_of_files, source_format="n3"):
        super(SeveralTtlFullFilesMemoryKindDigraphParser, self).__init__()
        self._yielder = SeveralTtlFullFilesMemoryKindTriplesYielder(list_of_files=list_of_files,
                                                                    source_format=source_format)


    def parse_graph(self, max_edges=-1):
        """
        It returns an object networkx.DiGraph() containing edges between the s and o of every
        triple (s, p, o)

        If max_edges has a posotive value, the returned graph should contain just the first
        $max_edges in the source as most
        :param max_edges:
        :return:
        """
        result = nx.DiGraph()
        for a_triple in self._yielder.yield_triples(max_triples=max_edges):
            result.add_edge(a_triple[0], a_triple[2])
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
        self._yielder._reset_count()  # That brave we are!
