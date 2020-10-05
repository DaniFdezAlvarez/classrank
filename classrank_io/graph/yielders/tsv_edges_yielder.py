_SEPARATOR = "\t"

class _BaseTsvEdgesYielder(object):

    def yield_edges(self, max_edges=-1):
        raise NotImplementedError("")

class TsvEdgesYielder(_BaseTsvEdgesYielder):

    def __init__(self, triples_yielder):
        self._triples_yielder = triples_yielder
        self._edges_count = 0


    def yield_edges(self, max_edges=-1):
        for a_triple in self._triples_yielder.yield_triples(max_edges):
            self._edges_count += 1
            if self._edges_count == max_edges:
                break
            yield a_triple[0], a_triple[2]


    def _parse_edge(self, candidate):
        candidate = candidate.strip()
        if candidate != "":
            elems = candidate.split(_SEPARATOR)
            if len(elems) == 2:
                return (elems[0], elems[1])
            return None


class TsvEdgesFileYielder(_BaseTsvEdgesYielder):

    def __init__(self, source_path, separator='\t'):
        self._separator = separator
        self._source_path = source_path
        self._edges_count = 0

    def yield_edges(self, max_edges=-1):
        with open(self._source_path, "r") as in_stream:
            for a_line in in_stream:
                pieces = a_line.strip().split(self._separator)
                if len(pieces) == 2:
                    self._edges_count += 1
                    if self._edges_count == max_edges:
                        break
                    yield ((pieces[0], pieces[1]))


class TsvEdgesMultiFileReader(_BaseTsvEdgesYielder):

    def __init__(self, list_of_files, separator='\t'):
        self._list_of_files = list_of_files
        self._edges_count = 0
        self._separator = separator

    def yield_edges(self, max_edges=-1):
        for a_file in self._list_of_files:
            yielder = TsvEdgesFileYielder(source_path=a_file,
                                          separator=self._separator)
            for an_edge in yielder.yield_edges():
                self._edges_count += 1
                if self._edges_count == max_edges:
                    break
                yield an_edge
