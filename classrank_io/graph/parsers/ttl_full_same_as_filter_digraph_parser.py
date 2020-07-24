from classrank_io.graph.parsers.ttl_full_memory_kind_digraph_parser import TtlFullMemoryKindDigraphParser
from classrank_io.graph.yielders.ttl_full_same_as_filter_triples_yielder import TtlFullSamAsFilterTriplesYielder

class TtlFullSamAsFilterDigraphParser(TtlFullMemoryKindDigraphParser):

    def __init__(self, source_file):
        super(TtlFullSamAsFilterDigraphParser, self).__init__(source_file=source_file)
        self._base_yielder = TtlFullSamAsFilterTriplesYielder(source_file=source_file)

