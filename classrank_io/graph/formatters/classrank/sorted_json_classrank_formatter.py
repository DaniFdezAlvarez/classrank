import json

from classrank_io.graph.formatters.classrank.classrank_formatter_interface import ClassRankFormatterInterface, KEY_ELEM
from core.classrank.classranker import KEY_CLASSRANK, KEY_CLASS_POINTERS, KEY_UNDER_T_CLASS_POINTERS



class SortedJsonClassrankFormatter(ClassRankFormatterInterface):
    def __init__(self, target_file=None, string_output=False, link_instances=True, serialize_pagerank=False):
        super(SortedJsonClassrankFormatter, self).__init__(link_instances=link_instances,
                                                           serialize_pagerank=serialize_pagerank)
        self._target_file = target_file
        self._string_output = string_output


    def format_classrank_dict(self, a_dict, pagerank_dict=None):
        # TODO: implement pagerank serialization
        sorted_list = self._sort_dict(a_dict)
        self._manage_instances_serialization(sorted_list, pagerank_dict)
        if not self._string_output:
            self._serialize_list(sorted_list)
            return "ClassRank serialized to " + self._target_file
        else:
            return self._stringify_result(sorted_list)

    def _manage_instances_serialization(self, sorted_list, pagerank_dict):
        for a_class_dict in sorted_list:
            self._convert_dict_of_instances(a_class_dict[KEY_CLASS_POINTERS], pagerank_dict)
            self._convert_dict_of_instances(a_class_dict[KEY_UNDER_T_CLASS_POINTERS], pagerank_dict)
            # for a_cp in a_class_dict[KEY_CLASS_POINTERS]:
            #     if self._link_instances:  # Link instances with each CP
            #         a_class_dict[KEY_CLASS_POINTERS][a_cp] = list(a_class_dict[KEY_CLASS_POINTERS][a_cp])
            #     else:  # Just keep a number of instances
            #         a_class_dict[KEY_CLASS_POINTERS][a_cp] = len(a_class_dict[KEY_CLASS_POINTERS][a_cp])

    def _convert_dict_of_instances(self, target_dict, pagerank_dict):
        for a_cp in target_dict:
            if self._link_instances:  # Link instances with each CP
                if not self._serialize_pagerank:
                    target_dict[a_cp] = list(target_dict[a_cp])
                else:
                    tmp_dict = {}
                    for an_instance_key in target_dict[a_cp]:
                        tmp_dict[an_instance_key] = pagerank_dict[an_instance_key]
                    target_dict[a_cp] = tmp_dict
            else:  # Just keep a number of instances
                target_dict[a_cp] = len(target_dict[a_cp])

    def _sort_dict(self, classes_dict):
        for a_key in classes_dict:
            classes_dict[a_key][KEY_ELEM] = a_key
        result = list(classes_dict.values())
        result.sort(reverse=True, key=lambda x:x[KEY_CLASSRANK])
        return result

    def _stringify_result(self, a_list):
        return json.dumps(a_list, indent=1)

    def _serialize_list(self, a_list):
        with open(self._target_file, "w") as out_stream:
            json.dump(a_list, fp=out_stream, indent=1)