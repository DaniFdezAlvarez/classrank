
from queue import LifoQueue
from model.log.search_session import SearchSession


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
        self._entries.append(an_entry)
        self._last_timestamp = an_entry.timestamp

    @property
    def last_entry(self):
        result = self._entries.pop()
        self._entries.append(result)  # Ugly, isnt it? but not sure if accesing by index the last one is O(n)
        return result

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
    @property
    def ratio_entries_minute(self):
        return float(len(self._entries)) / self.duration() * 60

    @property
    def duration(self):
        return SesionyzerConsecutiveQueries.time_gap(timestamp_old=self._first_timestamp,
                                                     timestamp_new=self._last_timestamp)



class SesionyzerConsecutiveQueries(object):

    def __init__(self, entries_yielder, max_gap_between_queries=300, max_window_session=1800, minimun_human_gap_between_queries=10):
        self._entries_yielder = entries_yielder
        self._max_gap_between_queries = max_gap_between_queries
        self._max_window_session= max_window_session

        self._last_timestamp_checked_to_close_session = None
        self._minimun_human_gap_between_queries = minimun_human_gap_between_queries

        self._reference_queue = LifoQueue()
        self._oldest_item_reference = None
        self._current_sessions_dict = {}

        self._refresh_reference_entry = self._create_reference_entry  # These are functions.
                                                                      # This value is gonna change in exec time

        self._sessions_ready_to_yield = []


    def yield_sessions(self):
        for an_entry in self._entries_yielder.yield_entries():
            self._reference_queue.put(an_entry)
            self._integrate_entry_in_current_sessions(an_entry)
            self._refresh_reference_entry(an_entry)
            self._attempt_to_close_extinguished_session(an_entry)
            while len(self._sessions_ready_to_yield) != 0:
                yield self._create_a_ready_session(self._sessions_ready_to_yield.pop())


    def _create_a_ready_session(self, summary_session):
        return SearchSession(init_timestamp=summary_session.first_timestamp,
                             miliseconds=summary_session.duration*1000,
                             n_queries=summary_session.n_entries,
                             representative_query=summary_session.last_entry)


    def _attempt_to_close_extinguished_session(self, an_entry):
        if self._last_timestamp_checked_to_close_session is None:
            self._last_timestamp_checked_to_close_session = an_entry.timestamp
            return
        if self.time_gap(entry_new=an_entry, timestamp_old=self._last_timestamp_checked_to_close_session) > self._max_gap_between_queries * 2:
            self._last_timestamp_checked_to_close_session = an_entry.timestamp
            self._close_extinguished_sessions(an_entry)

    def _close_extinguished_sessions(self, an_entry):
        keys_to_remove = []
        for an_ip_key in self._current_sessions_dict:
            if self.time_gap(timestamp_old=self._current_sessions_dict[an_ip_key].last_timestamp,
                             entry_new=an_entry) > self._max_gap_between_queries:
                keys_to_remove.append(an_ip_key)
                self._sessions_ready_to_yield.append(self._current_sessions_dict[an_ip_key])
        for a_key in keys_to_remove:
            del self._current_sessions_dict[a_key]


    def _refresh_reference_entry(self, an_entry):
        pass  # During execution, it will be _recheck_reference_entry or _initiate_reference_entry, the first time.

    def _create_reference_entry(self, an_entry):
        self._oldest_item_reference = self._reference_queue.get()
        self._refresh_reference_entry = self._recheck_reference_entry  # Change the strategy to renew reference_entry


    def _recheck_reference_entry(self, an_entry):
        while self.time_gap(entry_new=an_entry, entry_old=self._oldest_item_reference) > self._max_window_session:
            self._oldest_item_reference = self._reference_queue.get()

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
        if self.time_gap(entry_new=an_entry, timestamp_old=target_session.last_timestamp) <= self._max_gap_between_queries:
            return True
        return False

    @staticmethod
    def time_gap(entry_new=None, timestamp_new=None, entry_old=None, timestamp_old=None):
        """
        Provide one new item (entry or timestamp) and one old itme (entry or timestamp).
        I trust you'll do it ok? dont mess around
        :param entry_new:
        :param timestamp_new:
        :param entry_old:
        :param timestamp_old:
        :return:
        """
        target_new = timestamp_new if timestamp_new is not None else entry_new.timestamp
        target_old = timestamp_old if timestamp_old is not None else entry_old.timestamp
        return (target_new - target_old).seconds

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
        pass # TODO: READ COMMENT












