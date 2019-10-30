from classrank_io.json_io import write_obj_to_json

_KEY_HUMAN = "H"
_KEY_MACHINE = "M"
_KEY_UNKNOWN = "U"

_POS_IP = 0
_POS_AVG_PETITIONS = 1


class IpClassifierByAvgPetitions(object):

    def __init__(self, source_file, human_threshold, machine_threshold, headings_in_source_file=True):
        self._source_file = source_file
        self._human_threshold = human_threshold
        self._machine_threshold = machine_threshold
        self._headings_in_source_file = headings_in_source_file

        self._result_dict = self._init_result_dict()



    def run(self, output_file):
        for a_line in self._ip_numbers_lines(self._headings_in_source_file):
            self._anotate_ip(a_line)
        self._serialize(output_file)


    def _init_result_dict(self):
        return {
            _KEY_UNKNOWN : [],
            _KEY_MACHINE : [],
            _KEY_HUMAN : []
        }


    def _serialize(self, output_file):
        write_obj_to_json(target_obj=self._result_dict,
                          out_path=output_file,
                          indent=2)

    def _anotate_ip(self, a_line):
        pieces = a_line.split("\t")
        self._result_dict[self._solve_key_for_petitions_avg(pieces[_POS_AVG_PETITIONS])].append(pieces[_POS_IP])


    def _ip_numbers_lines(self, headings_in_source_file):
        with open(self._source_file, "r") as in_stream:

            if headings_in_source_file:
                in_stream.readline()  # and boom!! headers blown
            for a_line in in_stream:
                stripped = a_line.strip()
                if stripped != "":
                    yield a_line


    def _solve_key_for_petitions_avg(self, str_petitions_avg):
        rate = float(str_petitions_avg)
        if rate < self._human_threshold:
            return _KEY_HUMAN
        if rate > self._machine_threshold:
            return _KEY_MACHINE
        return _KEY_UNKNOWN






