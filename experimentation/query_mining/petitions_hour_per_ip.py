from classrank_io.query_log.selective_fields_dbpedia_log_yielder import SelectiveFieldsDbpediaLogYielder, \
    TIMESTAMP_FIELD, IP_FIELD

_N_PETITIONS_KEY = "n_p"
_AMOUNT_OF_HOURS_KEY = "Hs"
_HEADERS = ["IP", "AVG_PETITIONS_HOUR", "TOTAL_PETITIONS", "TOTAL_HOURS", "MAX_PETITIONS_IN_AN_HOUR"]
_SEPARATOR = "\t"

class PetitionsAverager(object):


    def __init__(self, list_of_files):
        self._list_of_files = list_of_files
        self._ips_dict = {}
        self._results_list = []

    def _reset_internal_structures(self):
        self._ips_dict = {}
        self._results_list = []

    def run(self, out_path):
        self._reset_internal_structures()
        for a_file in self._list_of_files:
            self._track_ip_activity_of_file(a_file)
        self._compute_averages()
        self._write_results(out_path)


    def _track_ip_activity_of_file(self, a_file_path):
        print("Analyzing " + a_file_path + "...")
        for an_entry in SelectiveFieldsDbpediaLogYielder(source_file=a_file_path,
                                                         target_fields_list=[IP_FIELD, TIMESTAMP_FIELD]).yield_entries():

            if an_entry.ip not in self._ips_dict:
                self._ips_dict[an_entry.ip] = {}
            self._anotate_ip_dict(an_entry)

    def _compute_averages(self):
        for an_ip, an_ip_dict in self._ips_dict.items():
            total_ip_hours = 0
            total_ip_petitions = 0
            max_pet_within_hour = 0

            for petitions in an_ip_dict.values():
                total_ip_hours += 1
                total_ip_petitions += petitions
                if petitions > max_pet_within_hour:
                    max_pet_within_hour = petitions

            self._results_list.append((an_ip,
                                       float(total_ip_petitions)/total_ip_hours,
                                       total_ip_petitions,
                                       total_ip_hours,
                                       max_pet_within_hour))
        self._results_list.sort(reverse=True,
                                key=lambda x:x[1])


    def _anotate_ip_dict(self, an_entry):
        hour = an_entry.timestamp.hour
        ip = an_entry.ip
        if hour not in self._ips_dict[ip]:
            self._ips_dict[ip][hour] = 0
        self._ips_dict[ip][hour] += 1


    def _write_results(self, out_path):
        with open(out_path, "w") as out_stream:
            out_stream.write(_SEPARATOR.join(_HEADERS) + "\n")
            for a_tuple in self._results_list:
                out_stream.write(_SEPARATOR.join(str(elem) for elem in a_tuple) + "\n")