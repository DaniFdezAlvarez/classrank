_SEPARATOR = "\t"

class TsvEdgesYielder(object):

    def __init__(self, triples_yielder):
        self._triples_yielder = triples_yielder


    def yield_edges(self, max_edges=-1):
        # yielding_func = self._yield_edges_from_file if self._source_file is not None \
        #     else self._yield_edges_from_raw_grpah
        #
        # for an_edge in yielding_func():
        #     yield an_edge
        for a_triple in self._triples_yielder.yield_triples(max_edges):
            yield a_triple[0], a_triple[2]


    # def _yield_edges_from_file(self):
    #     with open(self._source_file, "r") as in_stream:
    #         for a_line in in_stream:
    #             an_edge = self._parse_edge(a_line)
    #             if an_edge:
    #                 yield an_edge
    #
    # def _yield_edges_from_raw_grpah(self):
    #     target_edges = self._raw_graph.split("\n")
    #     for a_candidate in target_edges:
    #         an_edge = self._parse_edge(a_candidate)
    #         if an_edge:
    #             yield an_edge


    def _parse_edge(self, candidate):
        candidate = candidate.strip()
        if candidate != "":
            elems = candidate.split(_SEPARATOR)
            if len(elems) == 2:
                return (elems[0], elems[1])
            return None
