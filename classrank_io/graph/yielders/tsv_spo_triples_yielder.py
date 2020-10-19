__author__ = "Dani"
from classrank_io.graph.yielders.triples_yielder_interface import TriplesYielderInterface
from classrank_utils.uri import is_valid_triple


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
        if not is_valid_triple(pieces[0], pieces[1], pieces[2], there_are_corners=False):
            # log_to_error("WARNING: ignoring invalid triple: ( " + str(pieces[0]) + " , " + str(pieces[1]) + " , " + str(pieces[2]) + " )")
            return None, None, None
        return pieces[0], pieces[1], pieces[2]

    @property
    def yielded_triples(self):
        return self._triples_count

    @property
    def error_triples(self):
        return self._error_count

    @property
    def ignored_triples(self):
        return 0

    def _reset_count(self):
        self._error_count = 0
        self._triples_count = 0


class MultiFileTsvSpoTriplesYielder(TriplesYielderInterface):
    def __init__(self, list_of_files):
        super(MultiFileTsvSpoTriplesYielder, self).__init__()
        self._list_of_files = list_of_files
        self._triples_count = 0
        self._error_count = 0

        self._current_yielder = None

    def yield_triples(self, max_triples=-1):
        self._reset_count()
        for a_file in self._list_of_files:
            self._current_yielder = TsvSpoTriplesYielder(source_file=a_file)
            for a_triple in self._current_yielder.yield_triples(max_triples=max_triples):
                yield a_triple
            max_triples -= self._current_yielder.yielded_triples
            self._update_triples_count()

    def _update_triples_count(self):
        self._error_count += self._current_yielder.error_triples
        self._triples_count += self._current_yielder.yielded_triples

    @property
    def yielded_triples(self):
        return self._triples_count

    @property
    def error_triples(self):
        return self._error_count

    @property
    def ignored_triples(self):
        return 0

    def _reset_count(self):
        self._error_count = 0
        self._triples_count = 0
