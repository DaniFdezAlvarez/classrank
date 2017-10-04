from classrank_io.graph.formatters.classrank.classrank_formatter_interface import ClassRankFormatterInterface
from classranker import _KEY_CLASSRANK, _KEY_CLASS_POINTERS, _KEY_INSTANCES
import json

_KEY_ELEM = "class"

class SortedJsonFormatedInterface(ClassRankFormatterInterface):
    def __init__(self, target_file):
        super(SortedJsonFormatedInterface, self).__init__()
        self._target_file = target_file


    def format_classrank_dict(self, a_dict):
        sorted_list = self._sort_dict(a_dict)
        self._serialize_list(sorted_list)
        return "ClassRank serialized to " + self._target_file


    def _sort_dict(self, classes_dict):
        for a_key in classes_dict:
            classes_dict[a_key][_KEY_ELEM] = a_key
        result = list(classes_dict.values())
        result.sort(reverse=True, key=lambda x:x[_KEY_CLASSRANK])
        return result
        # return sorted(classes_dict.values(),
        #               key=lambda dict_class: classes_dict[dict_class][_KEY_CLASSRANK],
        #               reverse=True)

    def _serialize_list(self, a_list):
        for a_class_dict in a_list:
            for a_cp in a_class_dict[_KEY_CLASS_POINTERS]:
                a_class_dict[_KEY_CLASS_POINTERS][a_cp] = list(a_class_dict[_KEY_CLASS_POINTERS][a_cp])
        with open(self._target_file, "w") as out_stream:
            json.dump(a_list, fp=out_stream, indent=1)