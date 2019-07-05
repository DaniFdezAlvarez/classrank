import networkx as nx

from classrank_io.graph.parsers.digraph_parser_inferface import DiGraphParserInterface
from classrank_utils.uri import is_valid_uri
from classrank_utils.log import log_to_error


class TsvSoGraphParser(DiGraphParserInterface):
    def __init__(self, source_file):
        DiGraphParserInterface.__init__(self)
        self._source_file = source_file
        self._error_count = 0
        self._line_count = 0

    def parse_graph(self, max_edges=-1):
        self._reset_count()
        result = nx.DiGraph()
        with open(self._source_file, "r") as input_io:
            for a_line in input_io:
                if self._line_count == max_edges:
                    break
                a_subject, an_object = self._get_subject_and_object_from_line(a_line)
                if a_subject is not None and an_object is not None:
                    self._line_count += 1
                    result.add_edge(a_subject, an_object)
                else:
                    self._error_count += 1
                    log_to_error("WARNING: ignoring invalid triple: ( " + a_line + " )")

        return result

    def _get_subject_and_object_from_line(self, a_line):
        a_line = a_line.strip()
        pieces = a_line.split("\t")
        if len(pieces) != 2:
            self._error_count += 1
            return

        return pieces[0], pieces[1]

    @property
    def parsed_triples(self):
        return self._line_count

    @property
    def error_triples(self):
        return self._error_count

    @property
    def ignored_triples(self):
        return 0

    def _reset_count(self):
        self._error_count = 0
        self._line_count = 0
