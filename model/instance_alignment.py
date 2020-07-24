import json

# from src.in_out.util.set_encoder import SetEncoder
from classrank_io.util.set_encoder import SetEncoder


class InstanceAlignment(object):



    def __init__(self):
        self._alignments = {}  # Dict key=entity, value=set of aligned elements


    def add_alignment(self, resource1, resource2):
        # It assumes that nobody is gonna add the same alignment twice
        self._add_alignment_to_recource(resource1, resource2)
        self._add_alignment_to_recource(resource2, resource1)


    def _add_alignment_to_recource(self, reference, target):
        if reference not in self._alignments:
            self._alignments[reference] = set()
        self._alignments[reference].add(target)


    def yield_alignments(self):
        # It returns tuples of elements (not repeated)
        already_sent = set()
        for an_id_reference in self._alignments:
            for an_id_target in self._alignments[an_id_reference]:
                if an_id_target not in already_sent:
                    yield (an_id_reference, an_id_target)
            already_sent.add(an_id_reference)

    def yield_resources_aligned_with(self, a_resource):
        if a_resource in self._alignments:
            for a_target_resource in self._alignments[a_resource]:
                yield a_target_resource


    def get_set_of_resources_aligned_with(self, target_resource):
        if target_resource in self._alignments:
            return self._alignments[target_resource]
        return set()


    def has_alignments(self, target_resource):
        return target_resource in self._alignments

    def serialize(self, target_path):
        with open(target_path, "w") as out_stream:
            json.dump(self._alignments, out_stream, cls=SetEncoder, indent=2)








