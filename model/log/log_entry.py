class LogEntry(object):

    def __init__(self, query, valid_query=False, ip=None, timestamp=None, user_agent=None):
        self._query = query
        self._ip = ip
        self._timestamp = timestamp
        self._user_agent = user_agent
        self._valid_query = valid_query

    def __str__(self):
        return self._ip + " - " + str(self._timestamp) + " - " + str(self._user_agent) + " - " + self._query

    @property
    def timestamp(self):
        return self._timestamp

    @property
    def hour(self):
        return self._timestamp.hour

    @property
    def ip(self):
        return self._ip

    @property
    def user_agent(self):
        return self._user_agent

    @property
    def is_valid_query(self):
        return self._valid_query

    @property
    def str_query(self):
        return self._query
