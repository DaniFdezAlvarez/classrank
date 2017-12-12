
import json

from classrank_io.classpointers.formatters.ranged_classpointers_formatter_interface import RangedClasspointersFormatterInterface

class JsonRangedClasspointersFormater(RangedClasspointersFormatterInterface):

    def __init__(self, output_file=None, string_result=True):
        super(JsonRangedClasspointersFormater, self).__init__()
        self._output_file = output_file
        self._string_result = string_result

    def format_dict_of_classpointers_result(self, dict_of_classpointers_results):
        if self._string_result:
            return json.dumps(dict_of_classpointers_results, indent=2)
        else:
            with open(self._output_file, "w") as out_stream:
                json.dump(dict_of_classpointers_results, out_stream)
