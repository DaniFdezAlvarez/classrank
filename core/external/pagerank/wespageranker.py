from core.external.pagerank.sparse_matrix import PageRankSMatrix
from core.external.pagerank.power_iterator import PowerIterator


class Wespageranker(object):

    def __init__(self, source_file=None, raw_graph=None, damping_factor=0.85,
                 epsilon=1.0e-8, max_iters=300, max_edges=-1, base_triples_yielder=None, base_edges_yielder=None):
        self._source_file = source_file
        self._raw_graph = raw_graph,
        self._damping_factor = damping_factor
        self._eps = epsilon
        self._max_iters = max_iters
        self._iterations_performed = 0
        self._max_edges = max_edges
        self._base_yielder = base_triples_yielder
        self._base_edges_yielder = base_edges_yielder

    def compute_pagerank_vector(self):
        matrix = PageRankSMatrix(d=1 - self._damping_factor,
                                 source_file=self._source_file,
                                 raw_graph=self._raw_graph,
                                 max_edges=self._max_edges,
                                 base_triple_yielder=self._base_yielder,
                                 base_edges_yielder=self._base_edges_yielder)

        p_iterator = PowerIterator(target_matrix=matrix,
                                   epsilon=self._eps,
                                   max_iters=self._max_iters)
        result = p_iterator.calculate_pagerank_vector()
        self._iterations_performed = p_iterator.iterations_performed
        return result


    @property
    def iterations_performed(self):
        return self._iterations_performed

