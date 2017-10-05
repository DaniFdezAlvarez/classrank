from classrank_io.graph.parsers.digraph_parser_inferface import DiGraphParserInterface
from classrank_utils.uri import remove_corners
import networkx as nx
_SEPARATOR = " "


class TtlSimpleDigraphParser(DiGraphParserInterface):

    def __init__(self, source_file):
        super(TtlSimpleDigraphParser, self).__init__()
        self._source_file = source_file
        self._triple_count = 0
        self._error_count = 0

    def parse_graph(self, max_edges=-1):
        self._reset_count()
        result = nx.DiGraph()
        with open(self._source_file, "r") as in_stream:
            in_stream.readline() # Just to skip the first one
            for a_line in in_stream:
                s, o = self._get_subject_and_object_from_line(a_line)
                if s is not None:  # (the 0 should not be None)
                    self._triple_count += 1
                    result.add_edge(s, o)
                    if self._triple_count == max_edges:
                        break
                    if self._triple_count % 100000 == 0:
                        print self._triple_count
                else:
                    self._error_count += 1
        return result

    def _get_subject_and_object_from_line(self, a_line):
        a_line = a_line.strip()
        pieces = a_line.split(_SEPARATOR)
        if len(pieces) != 4:
            return None, None
        elif pieces[3] != ".":
            return None, None
        else:
            return remove_corners(pieces[0]), remove_corners(pieces[2])

    @property
    def parsed_triples(self):
        return self._triple_count

    @property
    def error_triples(self):
        return self._error_count

    def _reset_count(self):
        self._error_count = 0
        self._triple_count = 0
