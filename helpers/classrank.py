from classrank_io.graph.parsers.tsv_spo_digraph_parser import TsvSpoGraphParser
from classrank_io.graph.parsers.ttl_explicit_spo_digraph_parser import TtlExplicitSpoDigraphParser
from classrank_io.graph.parsers.ttl_simple_digraph_parser import TtlSimpleDigraphParser
from classrank_io.graph.parsers.ttl_full_digraph_parser import TtlFullDigraphParser

from classrank_io.graph.yielders.tsv_spo_triples_yielder import TsvSpoTriplesYielder
from classrank_io.graph.yielders.ttl_explicit_spo_triples_yielder import TtlExplicitSpoTriplesYielder
from classrank_io.graph.yielders.ttl_full_triples_yielder import TtlFullTriplesYielder
from classrank_io.graph.yielders.ttl_simple_triples_yielder import TtlSimpleTriplesYielder

from classrank_io.classpointers.parsers.one_per_line_classpointer_parser import OnePerLineClasspointerParser

from classrank_io.graph.formatters.classrank.sorted_json_classrank_formatter import SortedJsonClassrankFormatter

from classranker import ClassRanker




TTL_FULL_FORMAT = "ttl"
TSV_SPO_FORMAT = "tsv_spo"
TTL_SIMPLE_FORMAT = "ttl_simple"  # All triples are complete and are relevant
TTL_EXPLICIT_SPO_FORMAT = "ttl_explicit"  # All the triples are complete, but there may be literals or bnodes.
JSON_FULL_OUTPUT = "json"

_ACCEPTED_GRAPH_FORMATS = [TTL_FULL_FORMAT, TSV_SPO_FORMAT, TTL_SIMPLE_FORMAT, TTL_EXPLICIT_SPO_FORMAT]
_ACCEPTED_OUTPUT_FORMATS = [JSON_FULL_OUTPUT]



def _build_graph_yielder(graph_format, graph_file, raw_graph):
    if raw_graph is not None and graph_format in [TTL_FULL_FORMAT, TTL_SIMPLE_FORMAT, TTL_EXPLICIT_SPO_FORMAT]:
        return TtlFullTriplesYielder(string_graph=raw_graph)
    else:
        if graph_format == TTL_FULL_FORMAT:
            return TtlFullTriplesYielder(source_file=graph_file)
        elif graph_format == TTL_EXPLICIT_SPO_FORMAT:
            return TtlExplicitSpoTriplesYielder(source_file=graph_file)
        elif graph_format == TTL_SIMPLE_FORMAT:
            return TtlSimpleTriplesYielder(source_file=graph_file)
        elif graph_format == TSV_SPO_FORMAT:
            return TsvSpoTriplesYielder(source_file=graph_file)
        else:
            raise ValueError("Unsupported graph format building yielder")


def _build_digraph_parser(graph_format, graph_file, raw_graph):
    if raw_graph is not None and graph_format in [TTL_FULL_FORMAT, TTL_SIMPLE_FORMAT, TTL_EXPLICIT_SPO_FORMAT]:
        return TtlFullDigraphParser(string_graph=raw_graph)
    else:
        if graph_format == TTL_FULL_FORMAT:
            return TtlFullDigraphParser(source_file=graph_file)
        elif graph_format == TTL_EXPLICIT_SPO_FORMAT:
            return TtlExplicitSpoDigraphParser(source_file=graph_file)
        elif graph_format == TTL_SIMPLE_FORMAT:
            return TtlSimpleDigraphParser(source_file=graph_file)
        elif graph_format == TSV_SPO_FORMAT:
            return TsvSpoGraphParser(source_file=graph_file)
        else:
            raise ValueError("Unsupported graph format building parser")


def _build_cps_parser(classpointers_file, raw_classpointers):
    if raw_classpointers is not None:
        return OnePerLineClasspointerParser(raw_string=raw_classpointers)
    else:
        return OnePerLineClasspointerParser(source_file=classpointers_file)


def _build_cr_formatter(output_format, output_file, string_return):
    if output_format not in _ACCEPTED_OUTPUT_FORMATS:
        raise ValueError("Unsupported output format when building classrank formatter")
    elif string_return:
        return SortedJsonClassrankFormatter(string_output=True)
    else:
        return SortedJsonClassrankFormatter(target_file=output_file)





def _assert_valid_param_combination_classrank(damping_factor, max_iters, instantiation_threshold, class_threshold,
                                              graph_format, output_format, graph_file, classpointers_file, raw_graph,
                                              raw_classpointers, output_file, string_return):
    if graph_file is None and raw_graph is None:
        raise ValueError("You must provide a path in 'graph_file' XOR a string graph in 'raw_graph'")
    if graph_file is not None and raw_graph is not None:
        raise ValueError("You must provide a path in 'graph_file' XOR a string graph in 'raw_graph'")

    if classpointers_file is None and raw_classpointers is None:
        raise ValueError("You must provide a path in 'classpointers_file' XOR a string in 'raw_classpointers'")
    if classpointers_file is not None and raw_classpointers is not None:
        raise ValueError("You must provide a path in 'classpointers_file' XOR a string in 'raw_classpointers'")

    if output_file is None and not string_return:
        raise ValueError("You must provide a path in 'output_file' XOR set 'string_return' to True")
    if output_file is not None and string_return:
        raise ValueError("You must provide a path in 'output_file' XOR set 'string_return' to True")

    if damping_factor < 0 or damping_factor > 1:
        raise ValueError("'damping_factor' must be a value between 0 and 1")

    if max_iters < 1:
        raise ValueError("'max_iters' must be an integer positive value")

    if instantiation_threshold < 1:
        raise ValueError("'instantiation_threshold' must be an integer positive value")

    if class_threshold < 1:
        raise ValueError("'class_threshold' must be an integer >= 1")

    if graph_format not in _ACCEPTED_GRAPH_FORMATS:
        raise ValueError("Unsupported graph format")

    if output_format not in _ACCEPTED_OUTPUT_FORMATS:
        raise ValueError("Unsupported output format")


def generate_classrank(damping_factor=0.85, max_iters=250, instantiation_threshold=15, class_threshold=15,
                       max_triples=-1, graph_format=TTL_FULL_FORMAT, output_format=JSON_FULL_OUTPUT, graph_file=None,
                       classpointers_file=None, raw_graph=None, raw_classpointers=None,
                       output_file=None, string_return=False):
    """

    :param damping_factor: Damping factor for PageRank execution
    :param max_iters: Max iterations por PageRank execution
    :param instantiation_threshold: Instance threshold for ClassRank
    :param class_threshold:  Class threshold por ClassRank
    :param max_triples: If it is set to a positive integer, it makes the parsers and yielders stop when they process
     the specified amount of triples (correct ones).
    :param graph_format: format of the provided graph
    :param output_fotmat: format of the provided file.
    :param graph_file: path to the file in which the target graph is contained. If you want to
        provide the graph using a raw string, set to None and provide the graph though the param raw_graph
    :param classpointers_file: path to the file in which the classpointers are contained. If you want to
        provide the classpointers using a raw string, set to None and provide them though the param raw_classpointers
    :param raw_graph: string containing the target graph. If you want to provide the graph via file, set to
        None and provide the path through the param graph_file
    :param raw_classpointers: string containing the classpointers. If you want to provide them via file, set to
        None and provide them through the param classpointers_file
    :param output_file: format of the computed classrank.
    :param string_return: It it is True, the resulting classrank will be returned in this method. If its False,
     the result will be provided in the file specified in output_file
    :return:
    """
    ### Checking params
    _assert_valid_param_combination_classrank(damping_factor, max_iters, instantiation_threshold, class_threshold,
                                              graph_format, output_format, graph_file, classpointers_file, raw_graph,
                                              raw_classpointers, output_file, string_return)

    ### Parsers, yielders and formaters
    graph_parser = _build_digraph_parser(graph_format, graph_file, raw_graph)
    graph_yielder = _build_graph_yielder(graph_format, graph_file, raw_graph)
    cps_parser = _build_cps_parser(classpointers_file, raw_classpointers)
    cr_formatter = _build_cr_formatter(output_format, output_file, string_return)

    ### Execution

    ranker = ClassRanker(digraph_parser=graph_parser,
                         triple_yielder=graph_yielder,
                         classpointers_parser=cps_parser,
                         classrank_formatter=cr_formatter,
                         damping_factor=damping_factor,
                         max_iter_pagerank=250,
                         class_security_threshold=class_threshold,
                         instantiation_security_threshold=instantiation_threshold,
                         max_edges=max_triples)

    results = ranker.generate_classrank()

    ### Return
    return results  # It may be an string containig the Classrank or just a confirmation message
                    # in case the scores were stored in a file

