__author__ = "Dani"
from classrank_io.graph.yielders.triples_yielder_interface import TriplesYielderInterface

_SEPARATOR = "\t"


class TsvSpoTriplesYielder(TriplesYielderInterface):
    def __init__(self, source_file):
        super(TsvSpoTriplesYielder, self).__init__()
        self._source_file = source_file
        self._triples_count = 0
        self._error_count = 0

    def yield_triples(self, max_triples=-1):
        self._reset_count()
        with open(self._source_file, "r") as input_io:
            for a_line in input_io:
                s, p, o = self._get_spo_from_line(a_line)  # TODO
                if s is not None:  # Neither p and o will be None
                    yield s, p, o
                    self._triples_count += 1
                else:
                    self._error_count += 1

    @staticmethod
    def _get_spo_from_line(a_line):
        a_line = a_line.strip()
        pieces = a_line.split(_SEPARATOR)
        if len(pieces) != 3:
            return None, None, None
        for a_piece in pieces:
            if a_piece in ["", None]:
                return None, None, None
        return pieces[0], pieces[1], pieces[2]

    @property
    def parsed_triples(self):
        return self._triples_count

    @property
    def error_triples(self):
        return self._error_count

    def _reset_count(self):
        self._error_count = 0
        self._triples_count = 0
