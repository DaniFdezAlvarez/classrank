_SUBJECT = 0
_PERDICATE = 1
_OBJECT = 2

_KEY_CPS = "cps"
_KEY_DECREMENT = "decrement"
_KEY_NUM_CPS = "nCps"

class RangedCpCandidatesFinder(object):

    def __init__(self, triple_yielder, classpointers_formater, min_threshold, max_threshold, max_triples=-1):
        self._triple_yielder = triple_yielder
        self._classpointers_formatter = classpointers_formater
        self._min_threshold = min_threshold
        self._max_threshold = max_threshold
        self._max_triples = max_triples

    def generate_classpointer_candidates_by_range(self):
        classes_dict, set_above_max = self._build_classes_dict()
        results_by_range = self._build_list_of_tuple_results_by_threshold(classes_dict, set_above_max)
        return self._classpointers_formatter.format_dict_of_classpointers_result(results_by_range)


    def _build_classes_dict(self):
        set_above_max = set()
        classes_dict = {}
        for a_triple in self._triple_yielder.yield_triples(max_triples=self._max_triples):
            if a_triple[_PERDICATE] not in set_above_max:
                if a_triple[_OBJECT] not in classes_dict:
                    classes_dict[a_triple[_OBJECT]] = {}
                if a_triple[_PERDICATE] not in classes_dict[a_triple[_OBJECT]]:
                    classes_dict[a_triple[_OBJECT]][a_triple[_PERDICATE]] = 0
                classes_dict[a_triple[_OBJECT]][a_triple[_PERDICATE]] += 1
                if classes_dict[a_triple[_OBJECT]][a_triple[_PERDICATE]] >= self._max_threshold:
                    set_above_max.add(a_triple[_PERDICATE])
        return classes_dict, set_above_max


    def _build_list_of_tuple_results_by_threshold(self, classes_dict, set_above_max):
        result = {}
        # Initialization
        for i in range(self._min_threshold, self._max_threshold + 1):
            result[i] = {_KEY_CPS : set(),
                         _KEY_DECREMENT : None,
                         _KEY_NUM_CPS: 0}
        # Computation of not about max props
        for a_class_key in classes_dict:
            for a_prop_key in classes_dict[a_class_key]:
                if a_prop_key not in set_above_max:
                    for a_threshold_key in result:  # could be improved
                        if a_threshold_key <= classes_dict[a_class_key][a_prop_key]:  # could be improved
                            result[a_threshold_key][_KEY_CPS].add(a_prop_key)

        # Computation of above max props
        for a_prop_key in set_above_max:
            for a_threshold_key in result:
                result[a_threshold_key][_KEY_CPS].add(a_prop_key)

        # Adding num_cps
        for a_threshold_key in result:
            result[a_threshold_key][_KEY_NUM_CPS] = len(result[a_threshold_key][_KEY_CPS])

        # Adding decrements
        result[self._min_threshold][_KEY_DECREMENT] = set()
        for i in range(self._min_threshold +1, self._max_threshold + 1):

            result[i][_KEY_DECREMENT] = result[i-1][_KEY_CPS].difference(result[i][_KEY_CPS])

        # Turning sets into lists
        for a_threshold_key in result:
            result[a_threshold_key][_KEY_CPS] = list(result[a_threshold_key][_KEY_CPS])
            result[a_threshold_key][_KEY_DECREMENT] = list(result[a_threshold_key][_KEY_DECREMENT])

        #return
        return result







