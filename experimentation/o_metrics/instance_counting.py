from core.classrank.classranker import KEY_INSTANCES
from classrank_io.graph.formatters.classrank.classrank_formatter_interface import KEY_ELEM
from experimentation.o_metrics.asbtract_cr_adapter import AbstractScoresAdapter



class InstanceCountingCrAdpater(AbstractScoresAdapter):

    def __init__(self, classrank_scores_file=None, classrank_scores_raw=None):
        super().__init__(scores_file=classrank_scores_file,
                         scores_raw=classrank_scores_raw)

    def adapt_scores(self, out_file=None, string_output=None):
        result = []
        for a_dict in self._scores:
            result.append([a_dict[KEY_ELEM],
                           a_dict[KEY_INSTANCES]])
        result.sort(reverse=True, key=lambda x: x[1])
        counter = 1
        for a_list in result:
            a_list.append(str(counter))
            counter += 1
        return self._decide_return(result=result,
                                   out_file=out_file,
                                   string_output=string_output)



