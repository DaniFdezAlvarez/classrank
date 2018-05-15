from model.instance_alignment import InstanceAlignment
from classrank_utils.uri import remove_corners
from classrank_io.alignments.parser_instance_alignments import ParserInstanceAlignments, _S, _O


_CYC_BASE = "http://sw.cyc.com/concept/"
_OPENCYC_BASE = "http://sw.opencyc.org/concept/"

class ParserInstanceAlignmentsOpencycFix(ParserInstanceAlignments):

    def __init__(self, source_path):
        super(ParserInstanceAlignmentsOpencycFix, self).__init__(source_path)


    def parse_alignments(self):
        result = InstanceAlignment()
        for a_triple in self._yield_valid_triples():
            result.add_alignment(self._tune_elem(a_triple[_S]), self._tune_elem(a_triple[_O]))
        return result


    def _tune_elem(self, target_elem):
        result = remove_corners(str(target_elem))
        if _CYC_BASE in result:
            result = result.replace(_CYC_BASE, _OPENCYC_BASE)

        return result
