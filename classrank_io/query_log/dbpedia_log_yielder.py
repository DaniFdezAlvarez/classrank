from classrank_io.query_log.query_log_yielder_interface import QueryLogYielderInterface
# import time
import datetime

"""
Example of log entry:


fdbb563883f26e13b6ff5de74e91924d - - [08/Jul/2017 03:00:00 +0200] "GET /sparql?query=PREFIX+foaf%3A+%3Chttp%3A//xmlns.com/foaf/0.1/%3E%0APREFIX+owl%3A+%3Chttp%3A//www.w3.org/2002/07/owl%23%3E%0APREFIX+dc%3A+%3Chttp%3A//purl.org/dc/elements/1.1/%3E%0APREFIX+skos%3A+%3Chttp%3A//www.w3.org/2004/02/skos/core%23%3E%0APREFIX+dbpedia2%3A+%3Chttp%3A//dbpedia.org/property/%3E%0APREFIX+rdfs%3A+%3Chttp%3A//www.w3.org/2000/01/rdf-schema%23%3E%0APREFIX+dbpedia-owl%3A+%3Chttp%3A//dbpedia.org/ontology/%3E%0APREFIX+rdf%3A+%3Chttp%3A//www.w3.org/1999/02/22-rdf-syntax-ns%23%3E%0APREFIX+dbpedia%3A+%3Chttp%3A//dbpedia.org/%3E%0APREFIX+xsd%3A+%3Chttp%3A//www.w3.org/2001/XMLSchema%23%3E%0APREFIX+dcterms%3A+%3Chttp%3A//purl.org/dc/terms/%3E%0A%0A++++++++++++SELECT+%3Fpark+WHERE+%7B%0A++++++%3Chttp%3A//dbpedia.org/resource/Maineville%2C_Ohio%3E+dcterms%3Asubject+%3Fpark%0A%7D%0A++++++++&output=json&results=json&format=json HTTP/1.1" 200 229 "-" "-" "-"


"""


_DATE_FORMAT = "%Y/%b/%d %H:%M:S %z"

class DBpediaLogYielder(QueryLogYielderInterface):

    def __init__(self, source_file):
        super(DBpediaLogYielder, self).__init__()
        self._source_file = source_file



    def yield_entries(self):
        with open(self._source_file, "r") as in_stream:
            for a_line in in_stream:
                a_line = a_line.strip()
                if self._is_valid_line(a_line):
                    yield self._build_model_entry_log(a_line)


    def _is_valid_line(self, a_line):
        if a_line != "":
            return True
        return False


    def _build_model_entry_log(self, a_line):
        hashed_ip = self._look_for_hashed_ip(a_line)
        timestamp = self._look_for_timestamp_and_index_of_last_timestamp_char(a_line)


    def _look_for_timestamp_and_index_of_last_timestamp_char(self, a_line):
        """
        It return the already built timestamp object and the last index of the raw string timestamp (char ']')
        :param a_line:
        :return:
        """

        last_char_timestamp_index = a_line.find("]")
        string_timestamp = a_line[a_line.find("[") + 1:last_char_timestamp_index]

        return datetime.datetime.strptime(string_timestamp, _DATE_FORMAT), \
               last_char_timestamp_index


    def _look_for_hashed_ip(self, a_line):
        """
        The hash finishes when the first white space is met
        :param a_line:
        :return:
        """
        return a_line[:a_line.find(" ")]
