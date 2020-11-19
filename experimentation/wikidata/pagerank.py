from classrank_io.json_io import write_obj_to_json, read_json_obj_from_path

KEY_CLASS = "class"
KEY_SCORE = "score"
KEY_RANK = "rank"
KEY_LABEL = "lb"

class PageRankScorer(object):

    def __init__(self, pr_source_file, target_classes, labels_file):
        self._pr_source_file = pr_source_file
        self._labels_dict = self._load_labels(labels_file)
        self._target_classes = target_classes
        self._result_list = []


    def run(self, dest_file):
        self._filter_scores()
        self._sort_classes()
        self._add_rankings()
        self._serialize(dest_file)

    @staticmethod
    def _load_labels(labels_file):
        return read_json_obj_from_path(labels_file)

    def _sort_classes(self):
        self._result_list.sort(reverse=True, key= lambda x: x[KEY_SCORE])

    def _add_rankings(self):
        i = 0
        for a_sub_dict in self._result_list:
            i += 1
            a_sub_dict[KEY_RANK] = i

    def _serialize(self, dest_file):
        write_obj_to_json(target_obj=self._result_list,
                          out_path=dest_file,
                          indent=2)

    def _filter_scores(self):
        for a_class, a_score in self._yield_tuples_class_score():
            if a_class in self._target_classes:
                self._result_list.append(self._build_base_dict(a_class=a_class,
                                                               score=a_score))

    def _build_base_dict(self, a_class, score):
        return {
            KEY_CLASS: a_class,
            KEY_SCORE: score,
            KEY_RANK: 0,
            KEY_LABEL: "" if a_class not in self._labels_dict else self._labels_dict[a_class]
        }

    def _yield_tuples_class_score(self):
        with open(self._pr_source_file, "r") as in_stream:
            for a_line in in_stream:
                pieces = a_line.strip().split(":")
                if len(pieces) == 2:
                    yield self._beautify_wd_id(pieces[0]), self._beautify_score(pieces[1])

    @staticmethod
    def _beautify_wd_id(raw_id):
        return raw_id.replace("\"", "")

    @staticmethod
    def _beautify_score(raw_score):
        raw_score = raw_score.strip()
        if raw_score.endswith(","):
            raw_score = raw_score[:-1]
        return float(raw_score)
