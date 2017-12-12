from classrank_io.classpointers.formatters.one_per_line_classpointers_formatter import OnePerLineClasspointerFormatter
from classrank_io.classpointers.formatters.raw_classpointer_formatter import RawClasspointerFormater
from classrank_io.graph.yielders.tsv_spo_triples_yielder import TsvSpoTriplesYielder
from classrank_io.graph.yielders.ttl_explicit_spo_triples_yielder import TtlExplicitSpoTriplesYielder
from classrank_io.graph.yielders.ttl_full_memory_kind_triples_yielder import TtlFullMemoryKindTriplesYielder
from classrank_io.graph.yielders.ttl_full_triples_yielder import TtlFullTriplesYielder
from classrank_io.graph.yielders.ttl_simple_triples_yielder import TtlSimpleTriplesYielder
from core.classpointers.classpointer_candidates_finder import CpCandidatesFinder
from helpers.const import *

_ACCEPTED_GRAPH_FORMATS = [TTL_FULL_FORMAT, TSV_SPO_FORMAT, TTL_SIMPLE_FORMAT, TTL_EXPLICIT_SPO_FORMAT]


def _build_yielder(graph_format, graph_file, raw_graph, save_memory_mode):
    if raw_graph is not None and graph_format in [TTL_FULL_FORMAT, TTL_SIMPLE_FORMAT, TTL_EXPLICIT_SPO_FORMAT]:
        return TtlFullTriplesYielder(string_graph=raw_graph)
    else:
        if graph_format == TTL_FULL_FORMAT:
            if save_memory_mode:
                return TtlFullMemoryKindTriplesYielder(source_file=graph_file)
            else:
                return TtlFullTriplesYielder(source_file=graph_file)
        elif graph_format == TTL_EXPLICIT_SPO_FORMAT:
            return TtlExplicitSpoTriplesYielder(source_file=graph_file)
        elif graph_format == TTL_SIMPLE_FORMAT:
            return TtlSimpleTriplesYielder(source_file=graph_file)
        elif graph_format == TSV_SPO_FORMAT:
            return TsvSpoTriplesYielder(source_file=graph_file)
        else:
            raise ValueError("Unsupported graph format building yielder")


def _build_formatter(target_file, string_return):
    if string_return:
        return RawClasspointerFormater()
    else:
        return OnePerLineClasspointerFormatter(target_file)


def _assert_valid_param_combination(class_security_threshold, graph_format, raw_graph,
                                    graph_file, output_file, string_return):
    if graph_file is None and raw_graph is None:
        raise ValueError("You must provide a path in 'graph_file' XOR a string graph in 'raw_graph'")
    if graph_file is not None and raw_graph is not None:
        raise ValueError("You must provide a path in 'graph_file' XOR a string graph in 'raw_graph'")

    if output_file is None and not string_return:
        raise ValueError("You must provide a path in 'output_file' XOR set 'string_return' to True")
    if output_file is not None and string_return:
        raise ValueError("You must provide a path in 'output_file' XOR set 'string_return' to True")

    if graph_format not in _ACCEPTED_GRAPH_FORMATS:
        raise ValueError("Unsupported graph format")

    if class_security_threshold < 1:
        raise ValueError("'class_security_threshold' must be an integer >= 1")


def generate_classpointer_candidates(class_security_threshold=15, graph_format=TTL_FULL_FORMAT,
                                     raw_graph=None, graph_file=None, output_file=None, string_return=False,
                                     save_memory_mode=False):
    _assert_valid_param_combination(class_security_threshold=class_security_threshold,
                                    graph_format=graph_format,
                                    raw_graph=raw_graph,
                                    graph_file=graph_file,
                                    output_file=output_file,
                                    string_return=string_return)

    formater = _build_formatter(graph_file, string_return)
    yielder = _build_yielder(graph_format, graph_file, raw_graph, save_memory_mode)

    cp_finder = CpCandidatesFinder(triple_yielder=yielder,
                                   classpointers_formater=formater,
                                   class_security_threshold=class_security_threshold)

    return cp_finder.generate_classpointer_candidates()
