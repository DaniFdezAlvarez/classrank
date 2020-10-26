from classrank_io.graph.formatters.classrank.classrank_formatter_interface import ClassRankFormatterInterface
from core.classrank.classranker import KEY_CLASSRANK, KEY_CLASS_POINTERS
from classrank_io.json_io import write_obj_to_json
import statistics

SORT_BY_FIRST_CP_SET = "fcp"
SORT_BY_LAST_CP_SET = "lcp"
SORT_BY_AVERAGE_SCORE = "avg"

KEY_CLASS = "Class"


class SortedJsonClassRankFormatterSeveralCpSets(ClassRankFormatterInterface):

    def __init__(self, cp_sets, sort_by=SORT_BY_FIRST_CP_SET, target_file=None, raw_output=False):
        super().__init__()
        # Erase instances
        # Erase classpointers
        # Ignore pagerank scores
        self._cp_sets = cp_sets
        self._target_file = target_file
        self._raw_output = raw_output
        self._sort_by = sort_by

    def format_classrank_dict(self, classrank_dict, pagerank_dict=None):
        self._del_instances_key(classrank_dict)  # Highly invasive, but saving some memory that we may need.
        result = self._list_target_structure(classrank_dict)
        self._sort_list_result(result)
        return self._produce_results(result)

    def _del_instances_key(self, classrank_dict):
        for a_class_key in classrank_dict:
            del classrank_dict[a_class_key][KEY_CLASS_POINTERS]

    def _list_target_structure(self, classrank_dict):
        return [self._adapt_class_info(key, value) for key, value in classrank_dict.items()]

    def _adapt_class_info(self, class_key, class_value):
        class_value[KEY_CLASS] = class_key
        return class_value

    def _sort_list_result(self, target_list):
        target_list.sort(reverse=True,
                         key=self._get_lambda_to_sort())

    def _get_lambda_to_sort(self):
        if self._sort_by == SORT_BY_FIRST_CP_SET:
            return lambda x: x[KEY_CLASSRANK][0]
        elif self._sort_by == SORT_BY_LAST_CP_SET:
            return lambda x: x[KEY_CLASSRANK][-1]
        elif self._sort_by == SORT_BY_AVERAGE_SCORE:
            return lambda x: statistics.mean(x[KEY_CLASSRANK])

    def _produce_results(self, target_list):
        if self._raw_output:
            return target_list
        else:
            write_obj_to_json(target_obj=target_list,
                              out_path=self._target_file)
