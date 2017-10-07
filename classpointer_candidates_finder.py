
_SUBJEct = 0
_PERDICATE = 1
_OBJECT = 2

class CpCandidatesFinder(object):

    def __init__(self, triple_yielder, classpointers_formater, max_triples=-1, class_security_threshold=15):
        self._triple_yielder = triple_yielder
        self._classpointers_formatter = classpointers_formater
        self._class_security_threshold = class_security_threshold
        self._max_triples = max_triples

    def generate_classpointer_candidates(self):
        set_result = set()
        classes_dict = {}
        for a_triple in self._triple_yielder.yield_triples(max_triples=self._max_triples):
            if a_triple[_PERDICATE] not in set_result:
                if a_triple[_OBJECT] not in classes_dict:
                    classes_dict[a_triple[_OBJECT]] = {}
                if a_triple[_PERDICATE] not in classes_dict[a_triple[_OBJECT]]:
                    classes_dict[a_triple[_OBJECT]][a_triple[_PERDICATE]] = 0
                classes_dict[a_triple[_OBJECT]][a_triple[_PERDICATE]] += 1
                if classes_dict[a_triple[_OBJECT]][a_triple[_PERDICATE]] >= self._class_security_threshold:
                    set_result.add(a_triple[_PERDICATE])
        return self._classpointers_formatter.format_classpointers_set(set_result)

