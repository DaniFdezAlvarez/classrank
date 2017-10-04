from classrank_io.graph.formatters.pagerank.pagerank_formater_interface import PageRankFormatterInterface


class RawPageRankFormatter(PageRankFormatterInterface):
    def __init__(self):
        PageRankFormatterInterface.__init__(self)


    def format_pagerank_dict(self, a_dict):
        result = ""
        for a_key in a_dict:
            result += str(a_key) + "\t " + str(a_dict[a_key]) + "\n"
        return result
