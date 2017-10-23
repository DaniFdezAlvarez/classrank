from flask import Flask, request
from classranker import ClassRanker
from classrank_io.graph.parsers.ttl_full_digraph_parser import TtlFullDigraphParser
from classrank_io.graph.yielders.ttl_full_triples_yielder import TtlFullTriplesYielder
from classrank_io.classpointers.parsers.one_per_line_classpointer_parser import OnePerLineClasspointerParser
from classrank_io.graph.formatters.classrank.sorted_json_classrank_formatter import SortedJsonClassrankFormatter
from flask_cors import CORS


GRAPH_KEY = "G"
CLASSPOINTERS_KEY = "CP"
THRESHOLD_INSTANCES_KEY = "TI"
THRESHOLD_CLASSES_KEY = "TC"
DAMPING_FACTOR_KEY = "D"

PORT = 5002
MAX_LEN = 100000

app = Flask(__name__)


###################### SUPPORT FUNCTIONS


def _parse_damping(expected_str_float):
    result = float(expected_str_float)
    if result < 0 or result > 1:
        raise RuntimeError("Wrong damping factor")
    return result


def _parse_threshold(expected_str_int):
    result = int(expected_str_int)
    if result < 0:
        raise RuntimeError("Wrong threshold")
    return result


def _parse_cp_list(expected_str_list):
    result = ""
    expected_str_list = expected_str_list.strip()
    for a_line in expected_str_list.split("\n"):
        a_line = a_line.strip()
        if not a_line.startswith("# "):
            result += a_line + "\n"
    result = result.strip()
    if len(result) == 0:
        raise RuntimeError("Empty classpointers list")
    return result


def _parse_ttl_graph(expected_ttl_graph):
    if len(expected_ttl_graph) == 0:
        raise RuntimeError("Empty graph")
    elif len(expected_ttl_graph) == MAX_LEN:
        raise RuntimeError("Graph too big. Currently, this demo only process up to " + str(MAX_LEN) + " chars." )
    return expected_ttl_graph



####################### FLASK API


@app.route('/classrank', methods=['POST'])
def classrank():
    ttl_graph = ""
    cp_list = ""
    instances_threshold = 0
    classes_threshold = 0
    damping_factor = 0
    try:
        data = request.json
        damping_factor = _parse_damping(data[DAMPING_FACTOR_KEY])
        instances_threshold = _parse_threshold(data[THRESHOLD_INSTANCES_KEY])
        classes_threshold = _parse_threshold(data[THRESHOLD_CLASSES_KEY])
        cp_list = _parse_cp_list(data[CLASSPOINTERS_KEY])
        ttl_graph = _parse_ttl_graph(data[GRAPH_KEY])

    except BaseException as e:
        message =  "Unexpected data format: " + e.message
        return '{"Error" : "' + message + '"}'


    parser = TtlFullDigraphParser(string_graph=ttl_graph)
    yielder = TtlFullTriplesYielder(string_graph=ttl_graph)
    cp_parser = OnePerLineClasspointerParser(raw_string=cp_list)
    formatter = SortedJsonClassrankFormatter(string_output=True)

    classranker = ClassRanker(digraph_parser=parser,
                              triple_yielder=yielder,
                              classpointers_parser=cp_parser,
                              classrank_formatter=formatter,
                              damping_factor=damping_factor,
                              max_iter_pagerank=250,
                              class_security_threshold=classes_threshold,
                              instantiation_security_threshold=instances_threshold)
    result = classranker.generate_classrank()
    return result

CORS(app)
app.run(port=PORT)

