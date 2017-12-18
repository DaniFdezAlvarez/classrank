from classrank_io.graph.yielders.triples_yielder_interface import TriplesYielderInterface
from classrank_io.graph.yielders.ttl_full_memory_kind_triples_yielder import TtlFullMemoryKindTriplesYielder

#  several_ttl_full_files_memory_kind_triples_yielder


class SeveralTtlFullFilesMemoryKindTriplesYielder(TriplesYielderInterface):

    def __init__(self, list_of_files, source_format="n3"):
        super(SeveralTtlFullFilesMemoryKindTriplesYielder, self).__init__()
        self._list_of_files = list_of_files
        self._source_format = source_format
        self._current_yielder = None  # It will be used to access the triple counts of an object
                                      # which is yielding elements
        self._triples_count_of_finished_yielders = 0
        self._error_triples_of_finished_yielders = 0
        self._ignored_triples_of_finished_yielders = 0


    def yield_triples(self, max_triples=-1):
        """
        It returns a set of triples. If max_triples has a positive value,
        it returns $max_triples triples as most.

        :return:
        """
        self._reset_count()
        max_triples_reached = False
        for a_path in self._list_of_files:
            if max_triples_reached:
                break
            if self._current_yielder is not None:
                self._triples_count_of_finished_yielders += self._current_yielder.yielded_triples
                self._error_triples_of_finished_yielders += self._current_yielder.error_triples
                self._ignored_triples_of_finished_yielders += self._current_yielder.ignored_triples
                print "Mira como si que hago esto marmeluco!"
            self._current_yielder = TtlFullMemoryKindTriplesYielder(a_path)
            print "EYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYY New yielder!"
            for a_triple in self._current_yielder.yield_triples():
                yield a_triple
                if self.yielded_triples == max_triples:
                    max_triples_reached = True
                    break


    @property
    def yielded_triples(self):
        return self._triples_count_of_finished_yielders + self._current_yielder.yielded_triples

    @property
    def error_triples(self):
        return self._error_triples_of_finished_yielders + self._current_yielder.error_triples

    @property
    def ignored_triples(self):
        return self._ignored_triples_of_finished_yielders + self._current_yielder.ignored_triples

    def _reset_count(self):
        """
        Just to remember that the counts may be managed if the object is used to parse
        more than one time
        :return:
        """
        self._triples_count_of_finished_yielders = 0
        self._error_triples_of_finished_yielders = 0
        self._ignored_triples_of_finished_yielders = 0

