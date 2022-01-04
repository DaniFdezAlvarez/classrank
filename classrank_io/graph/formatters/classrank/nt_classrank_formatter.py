"""
It avoids using rdflib serialization

"""

from rdflib.term import URIRef, Literal, BNode

from classrank_io.graph.formatters.classrank.ttl_classrank_formatter import TtlClassrankFormatter



class NtClassRankFormatter(TtlClassrankFormatter):

    def __init__(self, target_file=None, string_output=False, link_instances=True, serialize_pagerank=False):
        super(NtClassRankFormatter, self).__init__(target_file=target_file,
                                                   string_output=string_output,
                                                   link_instances=link_instances,
                                                   serialize_pagerank=serialize_pagerank)
        self._wrong_triples = []

    def _serialize(self, result_graph):

        if self._string_output:
            string_triples = []
            for a_triple in result_graph.triples((None, None, None)):
                try:
                    string_triples.append(self._serialize_triple(a_triple))
                except ValueError:
                    self._wrong_triples.append(str(a_triple))
                return "\n".join(string_triples)

        else:
            with open(self._target_file, "w") as out_stream:
                for a_triple in result_graph.triples((None, None, None)):
                    try:
                        out_stream.write(self._serialize_triple(a_triple) + "\n")
                    except ValueError as e:
                        self._wrong_triples.append(str(a_triple))
            return "ClassRank serialized: " + self._target_file


    def _serialize_triple(self, a_triple):
        return " ".join([self._serialize_elem(a_triple[0]),
                         self._serialize_elem(a_triple[1]),
                         self._serialize_elem(a_triple[2]),
                         "."])

    def _serialize_elem(self, an_elem):
        if isinstance(an_elem, URIRef):
            return "<" + str(an_elem) + ">"
        elif isinstance(an_elem, BNode):
            return "_:" + str(an_elem)
        elif isinstance(an_elem, Literal):
            return str(an_elem)
        else:
            raise ValueError("Unknown triple")



