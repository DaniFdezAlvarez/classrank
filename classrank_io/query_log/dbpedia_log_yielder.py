from classrank_io.query_log.query_log_yielder_interface import QueryLogYielderInterface
from model.log.log_entry import LogEntry
# import time
import datetime
import urllib.parse
import rdflib
from rdflib.plugins.sparql import prepareQuery



"""
Example of log entry:


fdbb563883f26e13b6ff5de74e91924d - - [08/Jul/2017 03:00:00 +0200] "GET /sparql?query=PREFIX+foaf%3A+%3Chttp%3A//xmlns.com/foaf/0.1/%3E%0APREFIX+owl%3A+%3Chttp%3A//www.w3.org/2002/07/owl%23%3E%0APREFIX+dc%3A+%3Chttp%3A//purl.org/dc/elements/1.1/%3E%0APREFIX+skos%3A+%3Chttp%3A//www.w3.org/2004/02/skos/core%23%3E%0APREFIX+dbpedia2%3A+%3Chttp%3A//dbpedia.org/property/%3E%0APREFIX+rdfs%3A+%3Chttp%3A//www.w3.org/2000/01/rdf-schema%23%3E%0APREFIX+dbpedia-owl%3A+%3Chttp%3A//dbpedia.org/ontology/%3E%0APREFIX+rdf%3A+%3Chttp%3A//www.w3.org/1999/02/22-rdf-syntax-ns%23%3E%0APREFIX+dbpedia%3A+%3Chttp%3A//dbpedia.org/%3E%0APREFIX+xsd%3A+%3Chttp%3A//www.w3.org/2001/XMLSchema%23%3E%0APREFIX+dcterms%3A+%3Chttp%3A//purl.org/dc/terms/%3E%0A%0A++++++++++++SELECT+%3Fpark+WHERE+%7B%0A++++++%3Chttp%3A//dbpedia.org/resource/Maineville%2C_Ohio%3E+dcterms%3Asubject+%3Fpark%0A%7D%0A++++++++&output=json&results=json&format=json HTTP/1.1" 200 229 "-" "-" "-"


"""


_DATE_FORMAT = "%d/%b/%Y %H:%M:%S %z"

class DBpediaLogYielder(QueryLogYielderInterface):

    def __init__(self, source_file, namespaces_file, ignore_query=False):
        super(DBpediaLogYielder, self).__init__()
        self._source_file = source_file
        self._namespaces = self._build_dict_precharged_namespaces(namespaces_file)  # Empty graph to be used for checking queries
        self._ignore_query = ignore_query

    def yield_entries(self):
        with open(self._source_file, "r") as in_stream:
            for a_line in in_stream:
                a_line = a_line.strip()
                if self._is_valid_line(a_line):
                    yield self._build_model_entry_log(a_line)

    def _build_dict_precharged_namespaces(self, namespaces_file):
        if namespaces_file is None:
            return {}
        result = {}
        with open(namespaces_file, "r") as in_stream:
            for a_line in in_stream:
                a_line = a_line.strip()
                if a_line != "":
                    pieces = a_line.split("\t")
                    result[pieces[0]] = rdflib.Namespace([pieces[1]])
        return result

    def _is_valid_line(self, a_line):
        if a_line != "":
            return True
        return False


    def _build_model_entry_log(self, a_line):
        hashed_ip = self._look_for_hashed_ip(a_line)
        timestamp, index_last_timestamp = self._look_for_timestamp_and_index_of_last_timestamp_char(a_line)
        user_agent = self._look_for_user_agent(a_line, index_last_timestamp)

        str_query = ""
        is_valid_query = True
        if not self._ignore_query:
            str_query, is_valid_query = self._look_for_query(a_line[index_last_timestamp+1:])

        return LogEntry(query=str_query,
                        valid_query=is_valid_query,
                        timestamp=timestamp,
                        user_agent=user_agent,
                        ip=hashed_ip)

    def _look_for_query(self, a_partial_line):
        ini_query = a_partial_line.find("query=") + 6  # 6 == len("query")
        if ini_query == 5:  # 5 == -1 + 6 (-1 cause query was not found)
            return "", False
        fin1_query = a_partial_line[ini_query:].find(" ")
        fin2_query = a_partial_line[ini_query:].find("&")
        fin_query = fin1_query if fin2_query == -1 else fin2_query

        str_query = urllib.parse.unquote_plus(a_partial_line[ini_query:ini_query+fin_query])
        is_valid_query = self._check_valid_query(str_query)
        return str_query, is_valid_query

    def _check_valid_query(self, str_query):
        try:
            prepareQuery(str_query, initNs=self._namespaces)
            return True
        except:
            # print(str_query)
            return False


    def _look_for_user_agent(self, a_line, index_last_timestamp):
        return None  # TODO WHEN WE HAVE PROPER LOGS


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
