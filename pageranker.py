__author__ = "Dani"
from core.pagerank_nx import calculate_pagerank


class PageRanker(object):


    def __init__(self, graph_parser, pagerank_formatter, damping_factor=0.85):
        self._graph_parser = graph_parser
        self._pagerank_formatter = pagerank_formatter
        self._damping_factor = damping_factor

    def generate_pagerank(self):
        graph = self._graph_parser.parse_graph()
        raw_pagerank = calculate_pagerank(graph, damping_factor=self._damping_factor)
        return self._pagerank_formatter.format_pagerank_dict(raw_pagerank)
