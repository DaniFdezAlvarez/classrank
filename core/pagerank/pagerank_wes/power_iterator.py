
class PowerIterator(object):
    def __init__(self, target_matrix, epsilon, max_iters):
        self._target_matrix = target_matrix
        self._eps = epsilon
        self._max_iters = max_iters
        self._n_nodes = self._target_matrix.n_nodes
        self._curr_iters = 0
        self._current_vector = self._initialize_vector()


    @property
    def iterations_performed(self):
        return self._curr_iters

    def _initialize_vector(self):
        new_vec = []
        initial_value = 1.0 / self._target_matrix.n_nodes
        for i in range(0, self._n_nodes):
        # for a_key in self._target_matrix.yield_node_ids():
            new_vec.append(initial_value)
        return new_vec

    def calculate_pagerank_vector(self):
        self._curr_iters = 0
        print "starting"
        while self._curr_iters < self._max_iters:
            self._curr_iters += 1
            new_vec = []
            for i in range(0, self._n_nodes):
            # for a_key in self._current_vector:
                new_vec.append(self._compute_cell_value(i))
            if self._converges(new_vec):
                self._current_vector = new_vec
                break
            self._current_vector = new_vec
            if self._curr_iters % 10 == 0:
                print self._curr_iters
        if self._curr_iters >= self._max_iters:
            return self._current_vector
            # raise ValueError("The graph does not converge after " + str(self._max_iters) + " iterations.")
        return self._current_vector

    def _converges(self, new_vec):
        for i in range(0, self._n_nodes):
        # for elem in new_vec:
            if abs(new_vec[i] - self._current_vector[i]) > self._eps:
                return False
        return True

    def _compute_cell_value(self, target_row):
        result = 0
        # for elem in self._current_vector:
        for i in range(0, self._n_nodes):
            result += self._current_vector[i] * self._target_matrix.get(row=target_row,
                                                                        col=i)
        return result




