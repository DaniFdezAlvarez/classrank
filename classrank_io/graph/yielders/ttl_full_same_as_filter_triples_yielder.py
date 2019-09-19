"""
CAUTION! This yielder is able to parse a huge file without loading the whole graphic in memory,
but it is expecting a perfectly well-formed ttl. Syntax errors may cause unpredicted failures.

Also, it is ignoring b-nodes, which does not neccesarily make sense for all the sources.
If you want to include bnodes in your classrank computation, you should use/implement
a different yielder.

"""

from classrank_io.graph.yielders.ttl_full_memory_kind_triples_yielder import TtlFullMemoryKindTriplesYielder
from classrank_utils.uri import is_valid_triple
from classrank_utils.log import log_to_error

_OWL_SAME_AS = "http://www.w3.org/2002/07/owl#sameAs"

class TtlFullSamAsFilterTriplesYielder(TtlFullMemoryKindTriplesYielder):


    def __init__(self, source_file):
        super(TtlFullSamAsFilterTriplesYielder, self).__init__(source_file=source_file)
        self._owl_same_as_triples = 0


    def yield_triples(self, max_triples=-1):
        with open(self._source_file, "r") as in_stream:
            for a_line in in_stream:
                self._process_line(a_line)
                if self._triple_ready:
                    if self._is_valid_triple(self._tmp_s, self._tmp_p, self._tmp_o, there_are_corners=False):
                        self._triples_count += 1
                        yield (self._tmp_s, self._tmp_p, self._tmp_o)
                    else:
                        if self._is_owl_same_as(self._tmp_p):
                            self._owl_same_as_triples += 1
                        else:
                            log_to_error(msg="WARNING: ignoring invalid triple: ( " + str(self._tmp_s) + " , " + str(
                                self._tmp_p) + " , " + str(self._tmp_o) + " )",
                                         source=self._source_file)
                        self._error_triples += 1
                    self._triple_ready = False
                if self._triples_count == max_triples:
                    break


    def _is_valid_triple(self, s,p,o, there_are_corners):
        return is_valid_triple(s,p,o, there_are_corners) and not self._is_owl_same_as(p)

    @staticmethod
    def _is_owl_same_as(p):
        return str(p) == _OWL_SAME_AS

    @property
    def owl_same_as_triples(self):
        return self._owl_same_as_triples