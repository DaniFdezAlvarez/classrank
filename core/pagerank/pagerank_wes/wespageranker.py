from core.pagerank.pagerank_wes.sparse_matrix import SMatrix
from core.pagerank.pagerank_wes.power_iterator import PowerIterator


class Wespageranker(object):

    def __init__(self, source_file=None, raw_graph=None, damping_factor=0.85, epsilon=1.0e-8, max_iters=300):
        self._source_file = source_file
        self._raw_graph = raw_graph,
        self._damping_factor = damping_factor
        self._eps = epsilon
        self._max_iters = max_iters
        self._iterations_performd = 0

    def compute_pagerank_vector(self):
        matrix = SMatrix(d=self._damping_factor,
                         source_file=self._source_file,
                         raw_graph=self._raw_graph)

        p_iterator = PowerIterator(target_matrix=matrix,
                                   epsilon=self._eps,
                                   max_iters=self._max_iters)
        result = p_iterator.calculate_pagerank_vector()
        self._iterations_performd = p_iterator.iterations_performed
        return result


    @property
    def iterations_performed(self):
        return self._iterations_performd

