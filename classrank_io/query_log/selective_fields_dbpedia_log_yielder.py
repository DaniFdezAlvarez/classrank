"""
WARNING: The parsing of some fields depends on the parsing of timestamp. SO not including timestmap as target field
may cause errors. Use this class wisely

"""

from classrank_io.query_log.dbpedia_log_yielder import DBpediaLogYielder
from model.log.log_entry import LogEntry

QUERY_FIELD = "QUERY"
IP_FIELD = "IP"
TIMESTAMP_FIELD = "TIMESTAMP"
USER_AGENT_FIELD = "USER_AGENT"


class SelectiveFieldsDbpediaLogYielder(DBpediaLogYielder):

    def __init__(self, source_file, target_fields_list):
        super().__init__(source_file=source_file,
                         namespaces_file=None)
        self._target_fields_list = target_fields_list
        self._set_exploratory_functions(target_fields_list)


    def _look_for_ip_func(self, a_line):
        raise NotImplementedError("This function must be overwritten during the __init__")

    def _empty_ip_func(self, a_line):
        return None

    def _look_for_timestamp_func(self, a_line):
        raise NotImplementedError("This function must be overwritten during the __init__")

    def _empty_timestamp_func(self, a_line):
        return None, -1

    def _loof_for_query_func(self, a_line):
        raise NotImplementedError("This function must be overwritten during the __init__")

    def _empty_query_func(self, a_line):
        return None, False

    def _look_for_user_agent_func(self, a_line, index_last_timestamp):
        raise NotImplementedError("This function must be overwritten during the __init__")

    def _empty_user_agent_func(self, a_line, index_of_last_timestamp):
        return None

    def _set_exploratory_functions(self, target_fields_list):
        self._look_for_query_func = self._look_for_query if QUERY_FIELD in target_fields_list\
            else self._empty_query_func
        self._look_for_ip_func = self._look_for_hashed_ip if IP_FIELD in target_fields_list \
            else self._empty_ip_func
        self._look_for_timestamp_func = self._look_for_timestamp_and_index_of_last_timestamp_char if TIMESTAMP_FIELD in target_fields_list \
            else self._empty_timestamp_func
        self._look_for_user_agent_func = self._look_for_user_agent if USER_AGENT_FIELD in target_fields_list \
            else self._empty_user_agent_func

    def _build_model_entry_log(self, a_line):
        hashed_ip = self._look_for_ip_func(a_line) # self._look_for_hashed_ip(a_line)
        timestamp, index_last_timestamp =  self._look_for_timestamp_func(a_line) # self._look_for_timestamp_and_index_of_last_timestamp_char(a_line)
        user_agent = self._look_for_user_agent_func(a_line, index_last_timestamp)  # self._look_for_user_agent(a_line, index_last_timestamp)

        str_query, is_valid_query = self._look_for_query_func(a_line[index_last_timestamp+1:])  # self._look_for_query(a_line[index_last_timestamp+1:])

        return LogEntry(query=str_query,
                        valid_query=is_valid_query,
                        timestamp=timestamp,
                        user_agent=user_agent,
                        ip=hashed_ip)