class LogEntry(object):

    def __init__(self, query, ip=None, timestamp=None, user_agent=None):
        self._query = query
        self._ip = ip
        self._timestamp = timestamp
        self._user_agent = user_agent

    def __str__(self):
        return self._ip + " - " + str(self._timestamp) + " - " + str(self._user_agent) + " - " + self._query