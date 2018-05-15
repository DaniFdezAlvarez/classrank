import networkx as nx

from classrank_io.graph.parsers.digraph_parser_inferface import DiGraphParserInterface
from classrank_io.graph.yielders.graphs_joined_owl_same_as_yielder import GraphsJoinedOwlSameAsYielder

class TtlFullSamAsFilterDigraphParser(DiGraphParserInterface):

    def __init__(self, yielder1, yielder2, alignments_parser):
        super(TtlFullSamAsFilterDigraphParser, self).__init__()
        self._base_yielder = GraphsJoinedOwlSameAsYielder(yielder1=yielder1,
                                                          yielder2=yielder2,
                                                          alignments_parser=alignments_parser)


    def parse_graph(self, max_edges=-1):
        result = nx.DiGraph()
        for a_triple in self._base_yielder.yield_triples(max_triples=max_edges):
            result.add_edge(a_triple[0], a_triple[2])
        return result


    @property
    def parsed_triples(self):
        return self._base_yielder.yielded_triples


    @property
    def error_triples(self):
        return self._base_yielder.error_triples


    @property
    def ignored_triples(self):
        return self._base_yielder.ignored_triples


    def _reset_count(self):
        pass  # The base_yielder will initiate this task when needed (whenever the generator is called).
