
class SesionyzerSimpleMachineIpHours(object):

    def __init__(self, entries_yielder, max_queries_in_an_hour=80):
        self._entries_yielder = entries_yielder
        self._max_queries_in_an_hour = max_queries_in_an_hour
        self._active_sessions = {}



    def build_dict_machine_sessions(self):
        counter = 0
        for an_entry in self._entries_yielder.yield_entries():
            self._anonotate_in_active_sessions(an_entry)
            counter += 1
            if counter % 2000 == 0:
                print(counter)
        return self._build_dict_of_machine_time_gaps()


    def _anonotate_in_active_sessions(self, an_entry):
        if an_entry.ip not in self._active_sessions:
            self._active_sessions[an_entry.ip] = {}
        if an_entry.hour not in self._active_sessions[an_entry.ip]:
            self._active_sessions[an_entry.ip][an_entry.hour] = 0
        self._active_sessions[an_entry.ip][an_entry.hour] += 1


    def _build_dict_of_machine_time_gaps(self):
        result = {}
        for an_ip_key in self._active_sessions:
            i = 0
            for i in range(24):
                if i in self._active_sessions[an_ip_key]:
                    if self._active_sessions[an_ip_key][i] > self._max_queries_in_an_hour:
                        if an_ip_key not in result:
                            result[an_ip_key] = {}

                        result[an_ip_key][i] = self._active_sessions[an_ip_key][i]
        return result




