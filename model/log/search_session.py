
class SearchSession(object):

    def __init__(self, init_timestamp, miliseconds, n_queries, representative_query=None, ip=None):
        self._init_timestamp = init_timestamp
        self._miliseconds = miliseconds
        self._n_queries = n_queries
        self._representative_query = representative_query
        self._ip = ip

