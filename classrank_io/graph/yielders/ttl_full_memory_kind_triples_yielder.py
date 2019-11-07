"""
CAUTION! This yielder is able to parse a huge file without loading the whole graphic in memory,
but it is expecting a perfectly well-formed ttl. Syntax errors may cause unpredicted failures.

Also, it is ignoring b-nodes, which does not neccesarily make sense for all the sources.
If you want to include bnodes in your classrank computation, you should use/implement
a different yielder.

"""
import re
from classrank_io.graph.yielders.triples_yielder_interface import TriplesYielderInterface
from classrank_utils.uri import remove_corners, add_prefix_if_possible, is_valid_triple
from classrank_utils.log import log_to_error

_SEVERAL_BLANKS = re.compile("[ \r\n\t][ \r\n\t]+")
_RDF_TYPE = "rdf:type"
_BOOLEANS = ["true", "false"]


class TtlFullMemoryKindTriplesYielder(TriplesYielderInterface):
    def __init__(self, source_file):
        super(TtlFullMemoryKindTriplesYielder, self).__init__()
        self._source_file = source_file
        self._triples_count = 0
        self._error_triples = 0
        self._ignored_triples = 0

        # Support
        self._prefixes = {}

        # To be used while parsing
        self._tmp_s = None
        self._tmp_p = None
        self._tmp_o = None
        self._last_triple_jump = None

        self._triple_ready = False

    def yield_triples(self, max_triples=-1):
        with open(self._source_file, "r") as in_stream:
            for a_line in in_stream:
                print(a_line)
                self._process_line(a_line)
                if self._triple_ready:
                    if is_valid_triple(self._tmp_s, self._tmp_p, self._tmp_o, there_are_corners=False):
                        self._triples_count += 1
                        yield (self._tmp_s, self._tmp_p, self._tmp_o)
                        # print("gooood")
                    else:
                        log_to_error(msg="WARNING: ignoring invalid triple: ( " + str(self._tmp_s) + " , " + str(
                            self._tmp_p) + " , " + str(self._tmp_o) + " )",
                                     source=self._source_file)
                        # print("BAAAAAAAAAD",(self._tmp_s, self._tmp_p, self._tmp_o))
                        self._error_triples += 1
                    self._triple_ready = False
                # if self._triples_count % 1000000 == 0:
                #     print self._triples_count, self._tmp_s, self._tmp_p, self._tmp_o
                if self._triples_count == max_triples:
                    break

    def _clean_line(self, str_line):
        result = str_line.strip()
        return _SEVERAL_BLANKS.sub(" ", result)

    def _process_line(self, str_line):
        str_line = self._clean_line(str_line)
        if str_line in ["", " "]:
            self._process_empty_line(str_line)
        elif '"' in str_line:
            self._process_line_with_literal(str_line)
        elif str_line.startswith("@prefix"):
            self._process_prefix_line(str_line)
        elif str_line.startswith("#"):
            self._process_comment_line(str_line)
        elif str_line[-1] in [",", ".", ";"]:
            if ", " in str_line[:-1]:  # If there is a comma in a literal, it was discarded in a previous if clause
                # If there is a comma in a URI, it can't be followed by a blank
                self._process_multi_triple_line_commas(str_line)
            else:
                self._process_single_triple_line(str_line)
        elif " " not in str_line:
            if len(str_line) > 1:  # We are ensuring that this is not a single char, such as "," or "."
                self._process_isolated_subject(str_line)
        else:
            self._process_unknown_line(str_line)

    def _process_line_with_literal(self, line):
        self._ignored_triples += 1

    def _process_prefix_line(self, line):
        pieces = line.split(" ")
        prefix = pieces[1] if not pieces[1].endswith(":") else pieces[1][: - 1]
        base_url = remove_corners(pieces[2])
        self._prefixes[prefix] = base_url

    def _process_comment_line(self, line):
        pass  # At this point, just ignore it.

    def _process_empty_line(self, line):
        pass  # At this point, just ignore it.

    def _process_unknown_line(self, line):
        self._error_triples += 1
        log_to_error(msg="WARNING: ignoring error line: " + line,
                     source=self._source_file)

    def _process_multi_triple_line_commas(self, line):
        pieces = line.split(" ")
        index_first_comma = 0
        for i in range(0, len(pieces)):
            if pieces[i] == ",":
                index_first_comma = i
                break
        if index_first_comma == 3:
            self._tmp_s = self._parse_elem(pieces[0])
            self._tmp_p = self._parse_elem(pieces[1])
            self._tmp_o = self._parse_elem(pieces[2])
        elif index_first_comma == 2:
            self._tmp_p = self._parse_elem(pieces[0])
            self._tmp_o = self._parse_elem(pieces[1])
        elif index_first_comma == 1:
            self._tmp_o = self._parse_elem(pieces[0])
        # else impossible?
        self._decide_current_triple()

        for i in range(index_first_comma + 2, len(pieces), 2):
            self._tmp_o = self._parse_elem(pieces[i - 1])
            self._decide_current_triple()

    def _process_single_triple_line(self, line):
        pieces = line.split(" ")
        if len(pieces) == 4:
            self._tmp_s = self._parse_elem(pieces[0])
            self._tmp_p = self._parse_elem(pieces[1])
            self._tmp_o = self._parse_elem(pieces[2])

        elif len(pieces) == 3:
            self._tmp_p = self._parse_elem(pieces[0])
            self._tmp_o = self._parse_elem(pieces[1])
        elif len(pieces) == 2:
            self._tmp_o = self._parse_elem(pieces[0])
        self._decide_current_triple()

    def _process_isolated_subject(self, line):
        # No splitt. Line is expected to contain a line with no blanks (isolated subject)
        self._tmp_s = self._parse_elem(line)
        # No need to decide triple now, incomplete element

    def _decide_current_triple(self):
        if self._is_bnode(self._tmp_s):
            self._ignored_triples += 1
        elif self._is_bnode(self._tmp_o):
            self._ignored_triples += 1
        elif self._is_num_literal(self._tmp_o):
            self._ignored_triples += 1
        elif self._is_boolean(self._tmp_o):
            self._ignored_triples += 1
        else:
            self._triple_ready = True

    def _is_boolean(self, raw_element):
        return True if raw_element in _BOOLEANS else False

    def _is_bnode(self, a_elem):
        if a_elem[0] == "_":
            return True
        return False

    def _is_num_literal(self, elem):
        try:
            float(elem)
            return True
        except ValueError:
            return False

    def _parse_elem(self, raw_elem):
        if raw_elem[0] == "<":
            return add_prefix_if_possible(remove_corners(raw_elem), self._prefixes)
        elif raw_elem == "a":
            return _RDF_TYPE
        elif ":" in raw_elem or raw_elem in _BOOLEANS or self._is_num_literal(raw_elem):
            return raw_elem
            # else?? shouldnt happen, let it break with a nullpoitner

    @property
    def yielded_triples(self):
        return self._triples_count

    @property
    def error_triples(self):
        return self._error_triples

    @property
    def ignored_triples(self):
        return self._ignored_triples

    def _reset_count(self):
        self._error_triples = 0
        self._triples_count = 0
        self._ignored_triples = 0
