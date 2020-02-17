from experimentation.o_metrics.asbtract_cr_adapter import AbstractScoresAdapter


class PagerankAdapter(AbstractScoresAdapter):


    def __init__(self, target_uris, pagerank_scores_file=None, pagerank_scores_raw=None):
        super().__init__(scores_file=pagerank_scores_file,
                         scores_raw=pagerank_scores_raw)
        self._target_uris = target_uris


    def adapt_scores(self, out_file=None, string_output=None):
        result = []
        for an_uri in self._target_uris:
            result.append([an_uri, self._scores[an_uri] if an_uri in self._scores else 0])
        result.sort(reverse=True, key=lambda x:x[1])
        counter = 1
        for a_list in result:
            a_list.append(str(counter))
            counter += 1
        return self._decide_return(result=result,
                                   out_file=out_file,
                                   string_output=string_output)

