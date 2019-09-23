
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

        return self._domran_dict

    def _anotate_triple(self, a_triple):
        pass # todo
        # if a_triple[_S] not in self._instances_dict:
        #     self._instances_dict[a_triple[_S]] = []
        # if a_triple[_O] not in self._instances_dict[a_triple[_S]]:
        #     self._instances_dict[a_triple[_S]].append(a_triple[_O])


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





