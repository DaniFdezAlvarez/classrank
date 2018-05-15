from model.instance_alignment import InstanceAlignment
from classrank_utils.uri import remove_corners

_OWL_SAME_AS = "<http://www.w3.org/2002/07/owl#sameAs>"

_S = 0
_P = 1
_O = 2

class ParserInstanceAlignments(object):

    def __init__(self, source_path):
        self._source_path = source_path


    def parse_alignments(self):
        result = InstanceAlignment()
        for a_triple in self._yield_valid_triples():
            result.add_alignment(remove_corners(str(a_triple[_S])), remove_corners(str(a_triple[_O])))
        return result

    def _yield_valid_triples(self):
        with open(self._source_path, "r") as in_stream:
            for line in in_stream:
                if not line.startswith("#"):
                    pieces = line.strip().split(" ")  # We assume that the file is well built.
                    if str(pieces[1]) == _OWL_SAME_AS:
                        yield (str(pieces[0]), str(pieces[1]), str(pieces[2]))

