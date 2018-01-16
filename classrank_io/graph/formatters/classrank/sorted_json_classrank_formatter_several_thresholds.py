import json

from classrank_io.graph.formatters.classrank.classrank_formatter_interface import ClassRankFormatterInterface, KEY_ELEM
from core.classrank.classranker import KEY_CLASSRANK, KEY_CLASS_POINTERS, KEY_UNDER_T_CLASS_POINTERS
from core.classrank.classranker_several_thresholds import KEY_THRESHOLDS


class SortedJsonClassrankFormatterSeveralThresholds(ClassRankFormatterInterface):
    def __init__(self, target_file=None, string_output=False, link_instances=True, serialize_pagerank=False):
        super(SortedJsonClassrankFormatterSeveralThresholds, self).__init__(link_instances=link_instances,
                                                                            serialize_pagerank=serialize_pagerank)
        self._target_file = target_file
        self._string_output = string_output


    def format_classrank_dict(self, a_dict, pagerank_dict=None):
        # TODO: implement pagerank serialization
        sorted_list = self._sort_dict(a_dict)
        self._manage_instances_serialization(sorted_list)
        if not self._string_output:
            self._serialize_list(sorted_list)
            return "ClassRank serialized to " + self._target_file
        else:
            return self._stringify_result(sorted_list)

    def _manage_instances_serialization(self, sorted_list):
        for a_class_dict in sorted_list:
            if self._link_instances:
                for a_cp in a_class_dict[KEY_CLASS_POINTERS]:
                    a_class_dict[KEY_CLASS_POINTERS][a_cp] = list(a_class_dict[KEY_CLASS_POINTERS][a_cp])
                for a_cp in a_class_dict[KEY_UNDER_T_CLASS_POINTERS]:
                    a_class_dict[KEY_UNDER_T_CLASS_POINTERS][a_cp] = list(a_class_dict[KEY_UNDER_T_CLASS_POINTERS][a_cp])
            else:  # Just keep a number of instances
                for a_cp in a_class_dict[KEY_UNDER_T_CLASS_POINTERS]:
                    a_class_dict[KEY_CLASS_POINTERS][a_cp] = len(a_class_dict[KEY_CLASS_POINTERS][a_cp])
                for a_cp in a_class_dict[KEY_UNDER_T_CLASS_POINTERS]:
                    a_class_dict[KEY_UNDER_T_CLASS_POINTERS][a_cp] = len(a_class_dict[KEY_UNDER_T_CLASS_POINTERS][a_cp])

    def _sort_dict(self, classes_dict):
        for a_key in classes_dict:
            classes_dict[a_key][KEY_ELEM] = a_key
        result = list(classes_dict.values())
        min_threshold = self._detect_min_threshold(classes_dict)
        result.sort(reverse=True, key=lambda x:x[KEY_THRESHOLDS][min_threshold][KEY_CLASSRANK])
        return result
        # return sorted(classes_dict.values(),
        #               key=lambda dict_class: classes_dict[dict_class][_KEY_CLASSRANK],
        #               reverse=True)


    def _detect_min_threshold(self, classes_dict):
        for a_key in classes_dict:
            # We just need a key, no matter what, and we dont know any a priori.
            # So a for with a return at the first iteration
            return max([a_threshold for a_threshold in classes_dict[a_key][KEY_THRESHOLDS]])


    def _stringify_result(self, a_list):
        return json.dumps(a_list, indent=1)

    def _serialize_list(self, a_list):
        with open(self._target_file, "w") as out_stream:
            json.dump(a_list, fp=out_stream, indent=1)