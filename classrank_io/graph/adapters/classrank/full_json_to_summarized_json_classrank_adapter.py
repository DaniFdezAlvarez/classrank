import json
from classranker import KEY_CLASSRANK, KEY_CLASS_POINTERS, KEY_INSTANCES
from classrank_io.graph.formatters.classrank.classrank_formatter_interface import KEY_ELEM, KEY_RANK_POSITION

from classrank_io.graph.adapters.classrank.class_rank_adapter_interface import ClassRankAdapterInterface


class FullJsonToSummarizedJsonClassrankAdapter(ClassRankAdapterInterface):
    def __init__(self, source_path, output_path):
        super(FullJsonToSummarizedJsonClassrankAdapter, self).__init__(source_path)
        self._out_file = output_path

    def adapt_file(self, top_k=-1):
        """
        If top_k is a positive number, just the $top_k more relevant entities
        will be written to the output_path

        :param top_k:
        :return:
        """
        result = []
        rank_counter = 1
        with open(self._source_path, "r") as in_stream:
            original_rank = json.load(in_stream)
            for a_original_dict in original_rank:
                a_sum_dict = {KEY_ELEM: a_original_dict[KEY_ELEM],
                              KEY_CLASSRANK: a_original_dict[KEY_CLASSRANK],
                              KEY_INSTANCES: a_original_dict[KEY_INSTANCES],
                              KEY_CLASS_POINTERS: {},
                              KEY_RANK_POSITION: rank_counter
                              }

                rank_counter += 1
                if rank_counter % 5000 == 0:
                    print rank_counter
                for a_cp in a_original_dict[KEY_CLASS_POINTERS]:
                    a_sum_dict[KEY_CLASS_POINTERS][a_cp] = len( a_original_dict[KEY_CLASS_POINTERS][a_cp])
                result.append(a_sum_dict)

        with open(self._out_file, "w") as out_stream:
            json.dump(result, out_stream, indent=2)

        return "CR summarized and written to: " + self._out_file
