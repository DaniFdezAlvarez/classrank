class PowerIterator(object):
    def __init__(self, target_matrix, epsilon, max_iters):
        self._target_matrix = target_matrix
        self._eps = epsilon
        self._max_iters = max_iters
        self._current_vector = self._initialize_vector()


    def _initialize_vector(self):
        new_vec = {}
        initial_value = 1.0 / self._target_matrix.n_nodes
        for a_key in self._target_matrix.yield_node_ids():
            new_vec[a_key] = initial_value
        return new_vec

    def calculate_pagerank_vector(self):
        iters = 0
        while iters < self._max_iters:
            iters += 1
            new_vec = {}
            for a_key in self._current_vector:
                new_vec[a_key] = self._compute_cell_value(a_key)
            if self._converges(new_vec):
                self._current_vector = new_vec
                break
            self._current_vector = new_vec
        if iters >= self._max_iters:
            raise ValueError("The graph does not converge after " + str(self._max_iters) + " iterations.")
        return self._current_vector

    def _converges(self, new_vec):
        for a_key in new_vec:
            if abs(new_vec[a_key] - self._current_vector[a_key]) > self._eps:
                return False
            return True

    def _compute_cell_value(self, target_row):
        result = 0
        for a_key in self._current_vector:
            result += self._current_vector[a_key] * self._target_matrix.get(row=target_row,
                                                                            col=a_key)
        return result




