from classrank_io.graph.parsers.digraph_parser_inferface import DiGraphParserInterface
from classrank_utils.uri import remove_corners, is_valid_uri
from classrank_utils.log import log_to_error
import networkx as nx

_SEPARATOR = " "


class TtlExplicitSpoDigraphParser(DiGraphParserInterface):
    def __init__(self, source_file, there_are_corners=True):
        super(TtlExplicitSpoDigraphParser, self).__init__()
        self._source_file = source_file
        self._there_are_corners = there_are_corners
        self._triple_count = 0
        self._error_count = 0
        self._ignored = 0

    def parse_graph(self, max_edges=-1):
        self._reset_count()
        result = nx.DiGraph()
        with open(self._source_file, "r", errors='ignore', encoding="utf-8") as in_stream:
            in_stream.readline()  # Just to skip the first one
            for a_line in in_stream:
                s, o = self._get_subject_and_object_from_line(a_line)
                if s is not None:  # (the 0 should not be None)
                    result.add_edge(s, o)
                    if self._triple_count == max_edges:
                        break
                    if self._triple_count % 100000 == 0:
                        print(self._triple_count)
        return result

    def _get_subject_and_object_from_line(self, a_line):
        a_line = a_line.strip()
        pieces = a_line.split(_SEPARATOR)
        if pieces[-1] != ".":
            print("Error line:", a_line)
            self._error_count += 1
            return None, None
        elif len(pieces) != 4:
            self._ignored += 1
            return None, None
        elif not self._is_relevant_triple(pieces[0:3]):
            self._ignored += 1
            return None, None
        elif not is_valid_uri(pieces[0], there_are_corners=self._there_are_corners) or not is_valid_uri(pieces[2],
                                                                                                        there_are_corners=self._there_are_corners):
            log_to_error("WARNING: ignoring invalid triple: ( " + str(pieces[0]) + " , " + str(pieces[1]) + " , " + str(
                pieces[2]) + " )")
            self._error_count += 1
            return None, None
        else:
            self._triple_count += 1
            return remove_corners(pieces[0]), remove_corners(pieces[2])

    def _is_relevant_triple(self, triple):
        for elem in triple:
            if not elem.startswith("<"):
                return False
            if not elem.endswith(">"):
                return False
        return True

    @property
    def parsed_triples(self):
        return self._triple_count

    @property
    def error_triples(self):
        return self._error_count

    @property
    def ignored_triples(self):
        return self._ignored

    def _reset_count(self):
        self._error_count = 0
        self._triple_count = 0
        self._ignored = 0
