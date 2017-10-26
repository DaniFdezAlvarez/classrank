from classrank_io.graph.formatters.classrank.classrank_formatter_interface import ClassRankFormatterInterface
from classranker import KEY_CLASSRANK, KEY_CLASS_POINTERS, KEY_INSTANCES
import json

KEY_ELEM = "class"

class SortedJsonClassrankFormatter(ClassRankFormatterInterface):
    def __init__(self, target_file=None, string_output=False):
        super(SortedJsonClassrankFormatter, self).__init__()
        self._target_file = target_file
        self._string_output = string_output


    def format_classrank_dict(self, a_dict):
        sorted_list = self._sort_dict(a_dict)
        for a_class_dict in sorted_list:
            for a_cp in a_class_dict[KEY_CLASS_POINTERS]:
                a_class_dict[KEY_CLASS_POINTERS][a_cp] = list(a_class_dict[KEY_CLASS_POINTERS][a_cp])
        if not self._string_output:
            self._serialize_list(sorted_list)
            return "ClassRank serialized to " + self._target_file
        else:
            return self._stringify_result(sorted_list)


    def _sort_dict(self, classes_dict):
        for a_key in classes_dict:
            classes_dict[a_key][KEY_ELEM] = a_key
        result = list(classes_dict.values())
        result.sort(reverse=True, key=lambda x:x[KEY_CLASSRANK])
        return result
        # return sorted(classes_dict.values(),
        #               key=lambda dict_class: classes_dict[dict_class][_KEY_CLASSRANK],
        #               reverse=True)

    def _stringify_result(self, a_list):
        return json.dumps(a_list, indent=1)

    def _serialize_list(self, a_list):
        with open(self._target_file, "w") as out_stream:
            json.dump(a_list, fp=out_stream, indent=1)