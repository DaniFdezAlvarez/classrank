_SUBJECT = 0
_PREDICATE = 1
_OBJECT = 2

_KEY_CLASS = "class"
_KEY_NOT_CLASS = "not_class"

_KEY_CLASSPOINTERS = "cps"
_KEY_NOT_CLASSPOINTERS = "no_cps"
_KEY_N_CLASSES = "n_classes"
_KEY_DECREMENT = "decrement"


class EmphiricalClasspointersFinder(object):
    def __init__(self, triple_yielder, list_of_classes, formatter, prefix_tuples=None, thresholds=None, max_triples=-1):
        if thresholds is None:
            thresholds = [0.98]
        self._triple_yielder = triple_yielder
        self._prefixes = self._build_dict_of_prefixes_from_tuples(prefix_tuples, inverse=False)
        self._inverse_prefixes = self._build_dict_of_prefixes_from_tuples(prefix_tuples, inverse=True)
        self._set_of_classes = set(list_of_classes)
        self._thresholds = thresholds
        self._max_triples = max_triples
        self._props_usage_dict = {}
        self._formatter = formatter

    def generate_classpointers_candidates(self):
        for a_triple in self._triple_yielder.yield_triples(self._max_triples):
            # Including in usage dict if needed
            if a_triple[_PREDICATE] not in self._props_usage_dict:
                self._props_usage_dict[_PREDICATE] = self._get_empty_dict_of_usage()

            # Incrementing the corresponding usage
            if self._is_class(a_triple[_OBJECT]):
                self._props_usage_dict[a_triple[_PREDICATE]][_KEY_CLASS] += 1
            else:
                self._props_usage_dict[a_triple[_PREDICATE]][_KEY_NOT_CLASS] += 1
        result = self._build_result_dict()
        return self._formatter.format_dict_of_classpointers_result(result)

    def _build_result_dict(self):
        result = {}
        self._include_class_classification_by_threshold(result)
        self._add_decrements_to_result_dict(result)
        self._make_result_dict_serializable(result)
        return result

    def _include_class_classification_by_threshold(self, result):
        for a_threshold in self._thresholds:
            result[a_threshold] = self._get_empty_dict_of_threshold()
            for a_prop_key in self._props_usage_dict:
                if self._is_a_prop_pointing_to_classes(a_prop_key, a_threshold):
                    result[a_threshold][_KEY_CLASSPOINTERS].add(a_prop_key)
                else:
                    result[a_threshold][_KEY_NOT_CLASSPOINTERS].add(a_prop_key)

    def _add_decrements_to_result_dict(self, result):
        for i in range(1, len(self._thresholds)):
            result[self._thresholds[i]][_KEY_DECREMENT] = result[self._thresholds[i - 1]][_KEY_CLASS].difference(
                result[self._thresholds[i]][_KEY_CLASS])

    @staticmethod
    def _make_result_dict_serializable(result):
        for a_threshold_key in result:
            result[a_threshold_key][_KEY_NOT_CLASSPOINTERS] = list(result[a_threshold_key][_KEY_NOT_CLASSPOINTERS])
            result[a_threshold_key][_KEY_CLASSPOINTERS] = list(result[a_threshold_key][_KEY_CLASSPOINTERS])
            result[a_threshold_key][_KEY_DECREMENT] = list(result[a_threshold_key][_KEY_DECREMENT])

    def _is_a_prop_pointing_to_classes(self, a_property, threshold):
        frequency = len(self._props_usage_dict[a_property][_KEY_CLASS]) / (
            len(self._props_usage_dict[a_property][_KEY_CLASS]) + len(
                self._props_usage_dict[a_property][_KEY_NOT_CLASS]))
        return True if frequency >= threshold else False

    def _is_class(self, an_elem):
        if an_elem in self._set_of_classes:
            return True

        if an_elem.startswith("http://"):
            index_key_char = an_elem.index("#") if "#" in an_elem else an_elem.rindex("/")
            if an_elem[:index_key_char + 1] in self._inverse_prefixes:
                return self._inverse_prefixes[an_elem[:index_key_char + 1]] + ":" + \
                       an_elem[index_key_char:] in self._set_of_classes
            else:
                return False
        else:
            index_key_char = an_elem.index(":")
            if an_elem[:index_key_char + 1] in self._prefixes:
                return self._prefixes[an_elem[:index_key_char + 1]] + ":" + \
                       an_elem[index_key_char:] in self._set_of_classes
            else:
                return False


    @staticmethod
    def _get_empty_dict_of_threshold():
        return {_KEY_CLASSPOINTERS: set(),
                _KEY_NOT_CLASSPOINTERS: set(),
                _KEY_N_CLASSES: 0,
                _KEY_DECREMENT: set()}

    @staticmethod
    def _get_empty_dict_of_usage():
        return {_KEY_CLASS: 0,
                _KEY_NOT_CLASS: 0}

    @staticmethod
    def _build_dict_of_prefixes_from_tuples(prefix_tuples, inverse=True):
        result = {}
        if prefix_tuples is None:
            return result
        for a_tuple in prefix_tuples:
            if not inverse:
                result[a_tuple[0]] = a_tuple[1]
            else:
                result[a_tuple[1]] = a_tuple[0]
        return result
