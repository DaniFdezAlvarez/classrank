
_S = 0
_P = 1
_O = 2

from classrank_io.graph.yielders.triples_yielder_interface import TriplesYielderInterface
class GraphsJoinedOwlSameAsYielder(TriplesYielderInterface):

    def __init__(self, yielder1, yielder2, alignments_parser):
        super(GraphsJoinedOwlSameAsYielder, self).__init__()
        self._yielder1 = yielder1
        self._yielder2 = yielder2
        self._alignments_parser = alignments_parser
        self._alignment = self._build_alignment()
        # self._yielded_triples = 0
        # self._error_triples = 0
        # self._ignored_triples = 0


    def _build_alignment(self):
        return self._alignments_parser.parse_alignments()

    def yield_triples(self, max_triples=-1):
        """
        It returns a set of triples. If max_triples has a positive value,
        it returns $max_triples triples as most.

        :return:
        """
        self._reset_count()
        for a_triple in self._yielder1.yield_triples(max_triples=max_triples):
            yield a_triple
        if max_triples == -1:
            for a_triple in self._yield_triples_checking_alignments(max_triples):
                yield a_triple
        else:
            pending_triples = max_triples - self.yielded_triples
            if pending_triples > 0:
                for a_triple in self._yield_triples_checking_alignments(pending_triples):
                    yield a_triple


    def _yield_triples_checking_alignments(self, max_triples):
        for a_triple in self._yielder2.yielded_triples(max_triples):
            subjects = self._get_alignments_of_elem_or_self_if_there_are_not(a_triple[_S])
            objects = self._get_alignments_of_elem_or_self_if_there_are_not(a_triple[_O])

            if len(subjects) == 1 == len(objects):
                yield (subjects[0], a_triple[_P], objects[0])
            else:
                for a_subject in subjects:
                    for an_object in objects:
                        yield (a_subject, a_triple[_P], an_object)


    def _get_alignments_of_elem_or_self_if_there_are_not(self, elem):
        result = [aligned for aligned in self._alignment.yield_resources_aligned_with(elem)]
        if len(result) == 0:
            return [elem]
        return result


    @property
    def yielded_triples(self):
        return self._yielder1.yielded_triples + self._yielder2.yielded_triples


    @property
    def error_triples(self):
        return self._yielder1.error_triples + self._yielder2.error_triples


    @property
    def ignored_triples(self):
        return self._yielder1.ignored_triples + self._yielder2.ignored_triples


    def _reset_count(self):
        """
        Just to remember that the counts may be managed if the object is used to parse
        more than one time
        :return:
        """
        self._yielder1.reset_count()
        self._yielder2.reset_count()