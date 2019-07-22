
from queue import LifoQueue



class SummarySession(object):

    def __init__(self, first_entry):
        self._first_timestamp = first_entry.timestamp
        self._last_timestamp = first_entry.timestamp
        self._ip = first_entry.ip
        self._entries = [first_entry]

    def add_entry(self, an_entry):
        """
        It is assuming that the added query is older than the current ones cause the logs
        are being sequentially processed.
        :param an_entry:
        :return:
        """
        self._entries = []
        self._last_timestamp = an_entry.timestamp

    @property
    def first_timestamp(self):
        return self._first_timestamp

    @property
    def last_timestamp(self):
        return self._last_timestamp

    @property
    def ip(self):
        return self._ip

    @property
    def n_entries(self):
        return len(self._entries)

    @property
    def entries(self):
        return self._entries

    def ratio_entries_minute(self):
        pass  # TODO

    def duration(self):
        pass  # TODO




class SesionyzerConsecutiveQueries(object):

    def __init__(self, entries_yielder, max_gap_between_queries=300, max_window_session=1800, minimun_human_gap_between_queries=10):
        self._entries_yielder = entries_yielder
        self._max_gap_between_queries = max_gap_between_queries
        self._max_window_session= max_window_session

        self._reference_queue = LifoQueue()
        self._oldest_item_reference = None
        self._current_sessions_dict = {}

        self._sessions_ready_to_yield = []


    def yield_sessions(self):
        for an_entry in self._entries_yielder.yield_entries():
            self._reference_queue.put(an_entry)
            self._integrate_entry_in_current_sessions(an_entry)

            #TODO timestamps management: renew reference entry and manage aged sessions to clean the dict and yield elements.



    def _integrate_entry_in_current_sessions(self, an_entry):
        if an_entry.ip not in self._current_sessions_dict:
            self._create_new_summary_session(an_entry)
        else:
            if self._entry_belongs_to_session(an_entry):
                self._integrate_entry_in_session(an_entry)
            else:
                self._examine_current_ip_session_to_yield(an_ip=an_entry.ip,
                                                          remove=False)
                self._create_new_summary_session(an_entry)  # No need to del the key in the dict, since there is gonna
                # be a new session with the same key now erasin the old one, already ready to yield

    def _entry_belongs_to_session(self, an_entry):
        target_session = self._current_sessions_dict[an_entry.ip]
        if (an_entry.timestamp - target_session.last_timestamp).seconds <= self._max_gap_between_queries:
            return True
        return False


    def _integrate_entry_in_session(self, an_entry):
        self._current_sessions_dict[an_entry.ip].add_entry(an_entry)


    def _examine_current_ip_session_to_yield(self, an_ip, remove=False):
        target_session = self._current_sessions_dict[an_ip]
        if target_session.duration <= self._max_window_session:
            self._sessions_ready_to_yield.append(target_session)
        else:
            self._split_target_session_in_propper_ones_to_yield(an_ip)

        if remove:
            del self._current_sessions_dict[an_ip]

    def _create_new_summary_session(self, an_entry):
        self._current_sessions_dict[an_entry.ip] = SummarySession(first_entry=an_entry)



    def _split_target_session_in_propper_ones_to_yield(self, an_ip):
        """
        Here I could check gaps between queries and find the best way to divide it with this startegy:
        FInding the longest gap and check if splitting the session there makes the pieces fit into mas duration session.
        As long as this max gap is above a certain threshold (minimun_human_gap_between_queries)
        But, even if its does sounds crazy, that threshold sounds too arbitraty to be scientific. Lets just yield the whole
        session now and recheck this later in case there are too many cases of too long sessions,
        which I dont know a priori.
        :param an_ip:
        :return:
        """
        self._sessions_ready_to_yield.append(self._current_sessions_dict[an_ip])
        pass # TODO: REEAD COMMENT












