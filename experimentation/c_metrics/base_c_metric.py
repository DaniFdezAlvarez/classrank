from classrank_io.json_io import json_obj_to_string, write_obj_to_json

class BaseCMetric(object):

    def _return_result(self, obj_result, string_return, out_path):
        if out_path is not None:
            write_obj_to_json(target_obj=obj_result, out_path=out_path, indent=2)
        if string_return:
            return json_obj_to_string(target_obj=obj_result, indent=2)
        return obj_result