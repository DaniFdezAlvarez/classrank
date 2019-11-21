__author__ = "Dani"
from core.pagerank.pagerank_nx import calculate_pagerank


class PageRanker(object):
    def __init__(self, graph_parser, pagerank_formatter, damping_factor=0.85, max_edges=-1, max_iter=100):
        self._graph_parser = graph_parser
        self._pagerank_formatter = pagerank_formatter
        self._damping_factor = damping_factor
        self._max_edges = max_edges
        self._number_of_entities = 0
        self._max_iter = max_iter

    # @profile
    def generate_pagerank(self, raw=False):
        graph = self._graph_parser.parse_graph(max_edges=self._max_edges)
        raw_pagerank = calculate_pagerank(graph=graph,
                                          damping_factor=self._damping_factor,
                                          max_iter=self._max_iter)
        self._number_of_entities = len(raw_pagerank)
        if raw:
            return raw_pagerank
        return self._pagerank_formatter.format_pagerank_dict(raw_pagerank)


    @property
    def triples_analized(self):
        return self._graph_parser.yielded_triples

    @property
    def triples_with_error(self):
        return self._graph_parser.error_triples
