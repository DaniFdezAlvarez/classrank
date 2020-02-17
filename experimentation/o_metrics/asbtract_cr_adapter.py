from classrank_io.json_io import read_json_obj_from_path, json_obj_to_string, write_obj_to_json


class AbstractScoresAdapter(object):

    def __init__(self, scores_file, scores_raw):
        self._scores = self._decide_scores(scores_file=scores_file,
                                           scores_raw=scores_raw)


    def _decide_scores(self, scores_file, scores_raw):
        return scores_raw if scores_raw is not None \
            else read_json_obj_from_path(scores_file)

    def adapt_scores(self, out_file=None, string_output=None):
        raise NotImplementedError()

    def _decide_return(self, result, out_file, string_output):
        if string_output:
            return json_obj_to_string(target_obj=result)
        else:
            write_obj_to_json(target_obj=result,
                              out_path=out_file,
                              indent=2)
            return "Results serialized to " + out_file