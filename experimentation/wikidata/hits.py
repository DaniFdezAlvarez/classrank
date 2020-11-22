from experimentation.wikidata.pagerank import PageRankScorer

_OPEN_BRACKET = "["

class HitsScorer(PageRankScorer):

    def __init__(self, results_source_file, target_classes, labels_file):
        super().__init__(results_source_file, target_classes, labels_file)

    def _yield_tuples_class_score(self):
        with open(self._results_source_file, "r") as in_str:
            curr_class = ""
            # curr_score = 0
            pending_elements = 0
            for a_line in in_str:
                a_line = a_line.strip()
                if a_line == _OPEN_BRACKET:
                    pending_elements = 4
                elif pending_elements == 3:
                    curr_class = self._beautify_wd_id(a_line[:-1])  # Discard comma
                elif pending_elements == 2:
                    yield (curr_class, float(a_line[:-1]))
                pending_elements -= 1



