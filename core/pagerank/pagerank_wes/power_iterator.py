
class PowerIterator(object):

    def __init__(self, target_matrix, epsilon, max_iters):
        self._target_matrix = target_matrix
        self._eps = epsilon
        self._max_iters = max_iters
        self._current_vector = self._initialize_vector()
        self._curr_iters = 0

    @property
    def iterations_performed(self):
        return self._curr_iters

    def _initialize_vector(self):
        new_vec = {}
        initial_value = 1.0 / self._target_matrix.n_nodes
        for a_key in self._target_matrix.yield_node_ids():
            new_vec[a_key] = initial_value
        return new_vec

    def calculate_pagerank_vector(self):
        self._curr_iters = 0
        while self._curr_iters < self._max_iters:
            self._curr_iters += 1
            new_vec = dict.fromkeys(self._current_vector.keys(), 0)
            sum_dangling_nodes = sum(self._current_vector[a_dang_node] for a_dang_node in self._target_matrix.dangling_nodes)

            for n in self._target_matrix.non_dangling_nodes:
                for a_node_reached_by_n in self._target_matrix._cols[n]:
                    new_vec[a_node_reached_by_n] += self._target_matrix.alpha * \
                                                    self._current_vector[n] * \
                                                    self._target_matrix._dict_degrees[n]

            for n in self._current_vector:
                new_vec[n] += self._target_matrix.sink_score * (sum_dangling_nodes + self._target_matrix.d)
            if self._converges(new_vec):
                self._current_vector = new_vec
                break
            self._current_vector = new_vec

        #     self._curr_iters += 1
        #     unreached_nodes_cell = self._compute_unreached_nodes_cell()
        #     dangling_section_score = self._compute_dangling_section()
        #     # new_vec = {}
        #     new_vec = dict.fromkeys(self._current_vector.keys(), 0)
        #     for target_row in self._current_vector:
        #         # tmp_res = 0
        #         # for a_target_col in self._current_vector:
        #         #     tmp_res += self._current_vector[a_target_col] * self._target_matrix.get(row=target_row,
        #         #                                                                             col=a_target_col)
        #         # new_vec[target_row] = tmp_res
        #
        #         # new_vec[target_row] = sum([self._current_vector[target_col] *
        #         #                            self._target_matrix.get(row=target_row,
        #         #                                                    col=target_col)
        #         #                            for target_col in self._current_vector])
        #         if target_row in self._target_matrix.unreached_nodes:
        #             new_vec[target_row] = unreached_nodes_cell
        #             # print "weee", self._curr_iters
        #         else:
        #             # new_vec[target_row] = self._compute_cell_value(target_row)
        #             new_vec[target_row] = dangling_section_score + self._compute_non_dangling_section(target_row)
        #     if self._converges(new_vec):
        #         self._current_vector = new_vec
        #         break
        #     self._current_vector = new_vec
        # # print self._curr_iters, "I"
        # # if self._curr_iters >= self._max_iters:
        # #     raise ValueError("The graph does not converge after " + str(self._max_iters) + " iterations.")
        return self._current_vector

    def _converges(self, new_vec):
        return False
        # for a_key in new_vec:
        #     if abs(new_vec[a_key] - self._current_vector[a_key]) > self._eps:
        #         return False
        # return True

    def _compute_cell_value(self, target_row):
        result = 0
        for a_key in self._current_vector:
            result += self._current_vector[a_key] * self._target_matrix.get(row=target_row,
                                                                            col=a_key)
        return result

    def _compute_non_dangling_section(self, target_row):
        result = 0
        for a_key in self._target_matrix.non_dangling_nodes:
            result += self._current_vector[a_key] * self._target_matrix.get(row=target_row,
                                                                            col=a_key)
        return result

    def _compute_dangling_section(self):
        result = 0
        for a_dangling in self._target_matrix.dangling_nodes:
            result += self._current_vector[a_dangling] * self._target_matrix.sink_score
        return result

    def _compute_unreached_nodes_cell(self):
        result = 0
        for a_key_danglig in self._target_matrix.dangling_nodes:
            result += self._current_vector[a_key_danglig] * self._target_matrix.sink_score
        for a_non_dangling in self._target_matrix.non_dangling_nodes:
            result += self._current_vector[a_non_dangling] * self._target_matrix.base_score
        return result


    # def __init__(self, target_matrix, epsilon, max_iters):
    #     self._target_matrix = target_matrix
    #     self._eps = epsilon
    #     self._max_iters = max_iters
    #     self._n_nodes = self._target_matrix.n_nodes
    #     self._curr_iters = 0
    #     self._current_vector = self._initialize_vector()
    #
    #
    # @property
    # def iterations_performed(self):
    #     return self._curr_iters
    #
    # def _initialize_vector(self):
    #     new_vec = []
    #     initial_value = 1.0 / self._target_matrix.n_nodes
    #     for i in range(0, self._n_nodes):
    #     # for a_key in self._target_matrix.yield_node_ids():
    #         new_vec.append(initial_value)
    #     return new_vec
    #
    # def calculate_pagerank_vector(self):
    #     self._curr_iters = 0
    #     print "starting"
    #     while self._curr_iters < self._max_iters:
    #         self._curr_iters += 1
    #         new_vec = []
    #         for i in range(self._n_nodes):
    #         # for a_key in self._current_vector:
    #             new_vec.append(self._compute_cell_value(i))
    #         if self._converges(new_vec):
    #             self._current_vector = new_vec
    #             break
    #         self._current_vector = new_vec
    #         # if self._curr_iters % 10 == 0:
    #         print self._curr_iters,"I"
    #     if self._curr_iters >= self._max_iters:
    #         return self._current_vector
    #         # raise ValueError("The graph does not converge after " + str(self._max_iters) + " iterations.")
    #     return self._to_dict(self._current_vector)
    #
    # def _to_dict(self, vector):
    #     result = {}
    #     for i in range(len(vector)):
    #         result[self._target_matrix._node_index[i]] = vector[i]
    #     return result
    #
    # # # power iteration: make up to max_iter iterations
    # # for _ in range(max_iter):
    # #     xlast = x
    # #     x = dict.fromkeys(xlast.keys(), 0)
    # #     danglesum = alpha * sum(xlast[n] for n in dangling_nodes)
    # #     for n in x:
    # #         # this matrix multiply looks odd because it is
    # #         # doing a left multiply x^T=xlast^T*W
    # #         for nbr in W[n]:
    # #             x[nbr] += alpha * xlast[n] * W[n][nbr][weight]
    # #         x[n] += danglesum * dangling_weights.get(n, 0) + (1.0 - alpha) * p.get(n, 0)
    # #     # check convergence, l1 norm
    # #     err = sum([abs(x[n] - xlast[n]) for n in x])
    # #     if err < N * tol:
    # #         return x
    # # raise nx.PowerIterationFailedConvergence(max_iter)
    #
    # # # Create a copy in (right) stochastic form
    # # W = nx.stochastic_graph(D, weight=weight)
    # # N = W.number_of_nodes()
    # #
    # # # Choose fixed starting vector if not given
    # # if nstart is None:
    # #     x = dict.fromkeys(W, 1.0 / N)
    # # else:
    # #     # Normalized nstart vector
    # #     s = float(sum(nstart.values()))
    # #     x = dict((k, v / s) for k, v in nstart.items())
    # #
    # # if personalization is None:
    # #     # Assign uniform personalization vector if not given
    # #     p = dict.fromkeys(W, 1.0 / N)
    # # else:
    # #     s = float(sum(personalization.values()))
    # #     p = dict((k, v / s) for k, v in personalization.items())
    # #
    # # if dangling is None:
    # #     # Use personalization vector if dangling vector not specified
    # #     dangling_weights = p
    # # else:
    # #     s = float(sum(dangling.values()))
    # #     dangling_weights = dict((k, v / s) for k, v in dangling.items())
    # # dangling_nodes = [n for n in W if W.out_degree(n, weight=weight) == 0.0]
    # #
    #
    #
    # def _converges(self, new_vec):
    #     for i in range(0, self._n_nodes):
    #     # for elem in new_vec:
    #         if abs(new_vec[i] - self._current_vector[i]) > self._eps:
    #             return False
    #     return True
    #
    # def _compute_cell_value(self, target_row):
    #     # return sum([self._current_vector[i] * self._target_matrix.get(row=target_row, col=i) for i in range(0, self._n_nodes)])
    #     #
    #     result = 0
    #     # for elem in self._current_vector:
    #     for i in range(self._n_nodes):
    #         result += self._current_vector[i] * self._target_matrix.get(row=target_row,
    #                                                                     col=i)
    #     return result




