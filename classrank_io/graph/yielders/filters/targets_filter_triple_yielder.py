from classrank_io.graph.yielders.triples_yielder_interface import TriplesYielderInterface


class TargetsFilterTripleYielder(TriplesYielderInterface):

    def __init__(self, triple_yielder, target_nodes):
        super().__init__()
        self._triple_yielder = triple_yielder
        self._target_nodes = target_nodes if type(target_nodes) == set else set(target_nodes)

        self._yielded = 0
        self._ignored = 0


    def yield_triples(self, max_triples=-1):
        """
        It returns a set of triples. If max_triples has a positive value,
        it returns $max_triples triples as most.

        :return:
        """
        self._reset_count()
        for a_triple in self._triple_yielder.yield_triples(max_triples=max_triples):
            if self._is_a_relevant_triple(a_triple):
                yield a_triple
                self._yielded += 1
            else:
                self._ignored += 1

    def _is_a_relevant_triple(self, a_triple):
        if a_triple[0] in self._target_nodes and a_triple[2] in self._target_nodes:
            return True
        return False

    @property
    def yielded_triples(self):
        return self._yielded

    @property
    def error_triples(self):
        return self._triple_yielder.error_triples

    @property
    def ignored_triples(self):
        return self._ignored + self._triple_yielder.ignored_triples

    def _reset_count(self):
        """
        Just to remember that the counts may be managed if the object is used to parse
        more than one time
        :return:
        """
        self._yielded = 0
        self._ignored = 0