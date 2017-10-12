"""
It expects an input file in some RDF format recognized by rdflib and yields
all triple in which the subject and the object are both URIs.

CAUTION!! the graph is completely located in main memory. This parser may not
work with huge files.
"""
from classrank_io.graph.yielders.triples_yielder_interface import TriplesYielderInterface
from rdflib import Graph, term


class TtlFullTriplesYielder(TriplesYielderInterface):

    def __init__(self, source_file, source_format="n3"):
        super(TtlFullTriplesYielder, self).__init__()
        self._source_file = source_file
        self._triples_count = 0
        self._error_count = 0
        self._ignored = 0
        self._source_format = source_format

    def yield_triples(self, max_triples=-1):
        self._reset_count()
        rdfgraph = Graph()
        rdfgraph.parse(source=self._source_file,
                       format=self._source_format)
        for s,p,o in rdfgraph.triples((None, None, None)):
            if type(s) == term.URIRef and type(o) == term.URIRef:
                yield str(s), str(p), str(o)
                self._triples_count += 1
                if self._triples_count == max_triples:
                    break
            else:
                self._ignored += 1


    @property
    def yielded_triples(self):
        return self._triples_count

    @property
    def error_triples(self):
        return self._error_count

    @property
    def ignored_triples(self):
        return self._ignored

    def _reset_count(self):
        self._error_count = 0
        self._triples_count = 0
        self._ignored = 0