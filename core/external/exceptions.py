class IterationException(Exception):
    def __init__(self, num_iterations, *args):
        msg = "Max number of iterations exceeded {}".format(num_iterations)
        super(IterationException, self).__init__(msg, *args)


class UnlikelyConvergenceException(Exception):
    def __init__(self, non_convergent_nodes, *args):
        msg = "The algorithm seems stuck in a fixed number of non-convergent nodes: {}".format(non_convergent_nodes)
        super(UnlikelyConvergenceException, self).__init__(msg, *args)
