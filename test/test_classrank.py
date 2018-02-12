from classrank_io.classpointers.parsers.one_per_line_classpointer_parser import OnePerLineClasspointerParser
from classrank_io.graph.formatters.classrank.sorted_json_classrank_formatter_several_thresholds import \
    SortedJsonClassrankFormatterSeveralThresholds
from classrank_io.graph.parsers.json_wikidata_dump_digraph_parser import JsonWikidataDumpDiGraphParser
from classrank_io.graph.yielders.json_wikidata_dump_triples_yielder import JsonWikidataDumpTriplesYielder
from helpers.classrank import generate_classrank
from core.pagerank.pageranker import PageRanker
from classrank_io.graph.parsers.ttl_full_digraph_parser import TtlFullDigraphParser
from classrank_io.graph.yielders.ttl_full_triples_yielder import TtlFullTriplesYielder
from classrank_io.graph.formatters.pagerank.raw_pagerank_formatter import RawPageRankFormatter
from core.classrank.classranker_several_thresholds import ClassrankerSeveralThresholds
from classrank_io.classpointers.parsers.raw_classpointers_parser import RawClasspointerParser

from core.pagerank.pagerank_nx import calculate_pagerank

graph_str = """
@prefix txn: <http://example.org/data/transaction/> .
@prefix srv: <http://example.org/data/server/> .
@prefix log: <http://example.org/ont/transaction-log/> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

txn:123 <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> log:Transaction ;
	log:processedBy srv:A ;
	log:processedAt "2015-10-16T10:22:23"^^xsd:dateTime ;
	log:statusCode 200 .

txn:124 <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> log:Transaction ;
	log:processedBy srv:B ;
	log:processedAt "2015-10-16T10:22:24"^^xsd:dateTime ;
	log:statusCode 200 .

txn:125 <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> log:Transaction ;
	log:processedBy srv:C ;
	log:processedAt "2015-10-16T10:22:24"^^xsd:dateTime ;
	log:statusCode 200 .

txn:126 <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> log:Transaction ;
	log:processedBy srv:A ;
	log:processedAt "2015-10-16T10:22:25"^^xsd:dateTime ;
	log:statusCode 200 .

txn:127 <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> log:Transaction ;
	log:processedBy srv:B ;
	log:processedAt "2015-10-16T10:22:25"^^xsd:dateTime ;
	log:statusCode 200 .

txn:128 <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> log:Transaction ;
	log:processedBy srv:C ;
	log:processedAt "2015-10-16T10:22:26"^^xsd:dateTime ;
	log:statusCode 200 .

txn:129 <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> log:Transaction ;

	log:processedBy srv:A ;
	log:processedAt "2015-10-16T10:22:28"^^xsd:dateTime ;
	log:statusCode 500 .

txn:130 <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> log:Transaction ;
	log:processedBy srv:B ;
	log:processedAt "2015-10-16T10:22:31"^^xsd:dateTime ;
	log:statusCode 200 .

txn:131 <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> log:Transaction ;
	log:processedBy srv:C ;
	log:processedAt "2015-10-16T10:22:31"^^xsd:dateTime ;
	log:statusCode 200 .

txn:132 <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> log:Transaction ;
	log:processedBy srv:A ;
	log:processedAt "2015-10-16T10:22:32"^^xsd:dateTime ;
	log:statusCode 500 .

txn:133 <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> log:Transaction ;
	log:processedBy srv:B ;
	log:processedAt "2015-10-16T10:22:33"^^xsd:dateTime ;
	log:statusCode 200 .

txn:134 <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> log:Transaction ;
	log:processedBy srv:C ;
	log:processedAt "2015-10-16T10:22:33"^^xsd:dateTime ;
	log:statusCode 200 .

txn:135 <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> log:Transaction ;
    <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> srv:A ;
	log:processedBy srv:A ;
	log:processedAt "2015-10-16T10:22:35"^^xsd:dateTime ;
	log:statusCode 401 .

txn:aaa <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> srv:A .
"""
instances_transaction = [
    "http://example.org/data/transaction/131",
    "http://example.org/data/transaction/123",
    "http://example.org/data/transaction/125",
    "http://example.org/data/transaction/129",
    "http://example.org/data/transaction/128",
    "http://example.org/data/transaction/133",
    "http://example.org/data/transaction/132",
    "http://example.org/data/transaction/124",
    "http://example.org/data/transaction/127",
    "http://example.org/data/transaction/126",
    "http://example.org/data/transaction/130",
    "http://example.org/data/transaction/134",
    "http://example.org/data/transaction/135"
]

instances_A = [
    "http://example.org/data/transaction/132",
    "http://example.org/data/transaction/126",
    "http://example.org/data/transaction/129",
    "http://example.org/data/transaction/123",
    "http://example.org/data/transaction/135"
]

classrank_results = generate_classrank(raw_graph=graph_str,  # graph_file="files\\sample_ttl_full_tiny.ttl",
                                       raw_classpointers="http://www.w3.org/1999/02/22-rdf-syntax-ns#type\nhttp://example.org/ont/transaction-log/processedBy",
                                       # raw_classpointers="http://www.w3.org/1999/02/22-rdf-syntax-ns#type",
                                       string_return=True,
                                       instantiation_threshold=1,
                                       class_threshold=1)

parser_several = TtlFullDigraphParser(string_graph=graph_str)
yielder_several = TtlFullTriplesYielder(string_graph=graph_str)
cp_parser_several = RawClasspointerParser(list_of_classpointers=["http://www.w3.org/1999/02/22-rdf-syntax-ns#type",
                                                                 "http://example.org/ont/transaction-log/processedBy"])
formatter_several = SortedJsonClassrankFormatterSeveralThresholds(string_output=True,
                                                                  link_instances=True,
                                                                  serialize_pagerank=False)

classranker_several = ClassrankerSeveralThresholds(digraph_parser=parser_several,
                                                   triple_yielder=yielder_several,
                                                   classpointers_parser=cp_parser_several,
                                                   classrank_formatter=formatter_several,
                                                   damping_factor=0.85,
                                                   max_iter_pagerank=300,
                                                   thresholds_list=[1, 4],
                                                   max_edges=-1)

results_several = classranker_several.generate_classrank()

# pageranker = PageRanker(graph_parser=TtlFullDigraphParser(string_graph=graph_str),
#                         damping_factor=0.85,
#                         pagerank_formatter=RawPageRankFormatter(),
#                         max_edges=-1,
#                         max_iter=150)

raw_pagerank = calculate_pagerank(graph=TtlFullDigraphParser(string_graph=graph_str).parse_graph(),
                                  damping_factor=0.85,
                                  max_iter=300)

pg_res_transaction = 0
for ins in instances_transaction:
    pg_res_transaction += raw_pagerank[ins]
print pg_res_transaction, "transaction"

pg_res_A = 0
for ins in instances_A:
    pg_res_A += raw_pagerank[ins]

print pg_res_A, "A4"
print pg_res_A + raw_pagerank["http://example.org/data/transaction/aaa"], "A1"

# print raw_pagerank
# print classrank_results
print results_several


# pageranker_result = pageranker.generate_pagerank()

# print type(pageranker_result)
# print classrank_results
