
_S = 0
_P = 1
_O = 2


_DOMAIN_KEY = "D"
_RANGE_KEY = "R"

"""
Some expected models:
relevant_properties_dict --->
{
    prop1: {
        "D": [class1, class2,...],
        "R": [class1, class2,...]
    },
    prop2: {
        "D": [class1, class2,...]
    },
    prop1: {
        "R": [class1, class2,...]
    },
    ...
}

"""

class DomranTracker(object):

    def __init__(self, triples_yielder, relevant_properties_dict):
        self._relevnat_properties_dict = relevant_properties_dict
        self._triples_yielder = triples_yielder

        self._relevant_triples = 0
        self._not_relevant_triples = 0
        self._domran_dict = {}


    @property
    def relevant_triples(self):
        return self._relevant_triples

    @property
    def not_relevant_triples(self):
        return self._not_relevant_triples


    def track_domrans(self):
        self._reset_count()
        for a_revelant_triple in self._yield_relevant_triples():
            self._anotate_triple(a_revelant_triple)
        self._jsonize_domran_dict()

        return self._domran_dict

    def _jsonize_domran_dict(self):
        for a_domran_entity_key in self._domran_dict:
            self._domran_dict[a_domran_entity_key] = list(self._domran_dict[a_domran_entity_key])


    def _anotate_triple(self, a_triple):
        for a_key_dr, a_class_list in self._domran_dict[a_triple[_P]]:
            self._add_domran_to_result(a_key_dr, a_class_list, a_triple)


    def _add_domran_to_result(self, key_dr, class_list, triple):
        target_pos = _S if key_dr == _DOMAIN_KEY else _O
        if triple[target_pos] not in self._domran_dict:
            self._domran_dict[triple[target_pos]] = set()
        for a_class in class_list:
            self._domran_dict[triple[target_pos]].add(a_class)


    def _yield_relevant_triples(self):
        for a_triple in self._triples_yielder.yield_triples():
            if self._is_relevant_triple(a_triple):
                self._relevant_triples += 1
                yield a_triple
            else:
                self._not_relevant_triples += 1

    def _is_relevant_triple(self, a_triple):
        if a_triple[_P] in self._relevnat_properties_dict:
            return True
        return False


    def _reset_count(self):
        self._relevant_triples = 0
        self._not_relevant_triples = 0





