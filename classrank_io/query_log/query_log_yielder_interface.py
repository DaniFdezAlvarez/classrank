

class QueryLogYielderInterface(object):

    def __init__(self):
        pass

    def yield_entries(self):
        """
        It yields  LogEntry objects

        :return:
        """
        raise NotImplementedError()