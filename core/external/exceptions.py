class IterationException(Exception):
    def __init__(self, num_iterations, *args):
        msg = "Max number of iterations exceeded {}".format(num_iterations)
        super(IterationException, self).__init__(msg, "", *args)
