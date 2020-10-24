from core.classrank.classranker import ClassRanker


class ClassRankerSeveralCpSets(ClassRanker):

    def __init__(self, digraph_parser, triple_yielder, classpointers_sets, classrank_formatter,
                 damping_factor=0.85, max_iter_pagerank=100, max_edges=-1, pagerank_scores=None):
        super().__init__(digraph_parser=digraph_parser,
                         triple_yielder=triple_yielder,
                         classpointers_parser=None,  # there are different sets of classpointers known a priori
                         classrank_formatter=classrank_formatter,
                         damping_factor=damping_factor,
                         max_iter_pagerank=max_iter_pagerank,
                         threshold=1,  # Classes are known a priori as well
                         max_edges=max_edges,
                         pagerank_scores=pagerank_scores)

        self._classpointers_sets = classpointers_sets

    # TODO:
    # - Redefine the part in which cps are checked. Turn them all in for loops comparing results against the
    #   different sets of classpointers

    # - Redefine as well the part in which the algorithm looks for classes. Classes are known a priori
    # - Enjoy the life man!
    