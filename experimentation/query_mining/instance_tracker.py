
_RDF_TYPE = "http://www.w3.org/1999/02/22-rdf-syntax-ns#type"  # type: str
_RDFS_SUBCLASS_OF = "http://www.w3.org/2000/01/rdf-schema#subClassOf"

_S = 0
_P = 1
_O = 2


class InstanceTracker(object):

    def __init__(self, target_classes_list, triples_yielder, instantiation_properties=None,
                 all_classes_mode=False):
        # self._instances_dict = self._build_instances_dict(target_classes, all_classes_mode)
        if instantiation_properties is None:
            instantiation_properties = [_RDF_TYPE]
        self._target_classes = set(target_classes_list)
        self._instances_dict = {}
        self._triples_yielder = triples_yielder
        self._instantiation_properties = instantiation_properties
        self._relevant_triples = 0
        self._not_relevant_triples = 0
        self._all_classes_mode = all_classes_mode
        # self._subclass_property = subclass_property
        # self._annotator = get_proper_anotator(track_hierarchies=track_hierarchies,
        #                                       instance_tracker_ref=self)

    @property
    def relevant_triples(self):
        return self._relevant_triples

    @property
    def not_relevant_triples(self):
        return self._not_relevant_triples


    def track_instances(self):
        self._reset_count()
        for a_revelant_triple in self._yield_relevant_triples():
            self._anotate_triple(a_revelant_triple)

        return self._instances_dict

    def _anotate_triple(self, a_triple):
        if a_triple[_S] not in self._instances_dict:
            self._instances_dict[_S] = []
        if self._instances_dict[_O] not in self._instances_dict[_S]:
            self._instances_dict[_S].append(self._instances_dict[_O])


    def _yield_relevant_triples(self):
        for a_triple in self._triples_yielder.yield_triples():
            if self._is_relevant_triple(a_triple):
                self._relevant_triples += 1
                yield a_triple
            else:
                self._not_relevant_triples += 1

    def _is_relevant_triple(self, a_triple):
        if a_triple[_P] in self._instantiation_properties:
            if self._all_classes_mode or a_triple[_O] in self._target_classes:
                return True
        return False


    def _reset_count(self):
        self._relevant_triples = 0
        self._not_relevant_triples = 0





