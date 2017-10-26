"""
It expects an input file in which the first line is a non-parseable comment and the rest of
lines contain each one a triple of a graph in ttl format.
"""
from classrank_io.graph.yielders.triples_yielder_interface import TriplesYielderInterface
from classrank_utils.uri import remove_corners

_SEPARATOR = " "

class TtlExplicitSpoTriplesYielder(TriplesYielderInterface):

    def __init__(self, source_file):
        super(TtlExplicitSpoTriplesYielder, self).__init__()
        self._source_file = source_file
        self._triples_count = 0
        self._triples_ignored = 0
        self._error_count = 0

    def yield_triples(self, max_triples=-1):
        self._reset_count()
        with open(self._source_file, "r") as in_stream:
            in_stream.readline()  # Skipping the first line
            for a_line in in_stream:
                s,p,o = self._get_triple_from_line(a_line)
                if s is not None:  # Nor p and o
                    self._triples_count += 1
                    yield s,p,o
                    if self._triples_count == max_triples:
                        break
                    if self._triples_count %100000 == 0:
                        print self._triples_count


    def _get_triple_from_line(self, a_line):
        a_line = a_line.strip()
        a_line = a_line.strip()
        pieces = a_line.split(_SEPARATOR)
        if pieces[-1] != ".":
            print "Error line:", a_line
            self._error_count += 1
            return None, None, None
        elif len(pieces) != 4:
            self._triples_ignored += 1
            return None, None, None
        elif not self._is_relevant_triple(pieces[0:3]):
            self._triples_ignored += 1
            return None, None, None
        else:
            return remove_corners(pieces[0]), remove_corners(pieces[1]), remove_corners(pieces[2])

    def _is_relevant_triple(self, triple):
        for elem in triple:
            if not elem.startswith("<"):
                return False
            if not elem.endswith(">"):
                return False
        return True

    @property
    def yielded_triples(self):
        return self._triples_count

    @property
    def error_triples(self):
        return self._error_count

    @property
    def ignored_triples(self):
        return self._triples_ignored

    def _reset_count(self):
        self._error_count = 0
        self._triples_count = 0
        self._triples_ignored = 0