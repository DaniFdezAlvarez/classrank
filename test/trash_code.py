
from classrank_io.graph.parsers.tsv_spo_digraph_parser import TsvSpoGraphParser
from classrank_io.graph.formatters.pagerank.raw_pagerank_formatter import RawPageRankFormatter
from classrank_io.classpointers.parsers.one_per_line_classpointer_parser import OnePerLineClasspointerParser
from classrank_io.classpointers.formatters.raw_classpointer_formatter import RawClasspointerFormater
from classrank_io.graph.yielders.tsv_spo_triples_yielder import TsvSpoTriplesYielder
from classrank_io.graph.formatters.classrank.sorted_json_classrank_formatter import SortedJsonFormatedInterface
from pageranker import PageRanker
from classranker import ClassRanker
from classrank_io.graph.parsers.ttl_simple_digraph_parser import TtlSimpleDigraphParser
from classrank_io.graph.yielders.ttl_simple_triples_yielder import TtlSimpleTriplesYielder
from classrank_io.classpointers.formatters.one_per_line_classpointers_formatter import OnePerLineClasspointerFormatter
from classpointer_candidates_finder import CpCandidatesFinder
from classrank_io.graph.parsers.ttl_full_digraph_parser import TtlFullDigraphParser
from classrank_io.graph.yielders.ttl_full_triples_yielder import TtlFullTriplesYielder
from classrank_io.graph.yielders.ttl_explicit_spo_triples_yielder import TtlExplicitSpoTriplesYielder
from classrank_io.graph.parsers.ttl_explicit_spo_digraph_parser import TtlExplicitSpoDigraphParser

#
# parser = TsvSpoGraphParser("files\\tsv_spo_tiny.tsv")
#
# formater = RawPageRankFormatter()
#
# pageranker = PageRanker(graph_parser=parser,
#                         pagerank_formatter=formater,
#                         damping_factor=0.85)
# result = pageranker.generate_pagerank()
#
#
# classpointers_parser = OnePerLineClasspointerParser("files\\classpointers_tiny.tsv")
# classpointer_set = classpointers_parser.parse_classpointers()
# classpointer_str = RawClasspointerFormater().format_classpointers_set(classpointer_set)
#
#
# triple_yielder = TsvSpoTriplesYielder(source_file="files\\tsv_spo_tiny.tsv")
# classrank_formater = SortedJsonFormatedInterface(target_file="files\\out\\CR_tiny.tsv")
#
# classranker = ClassRanker(digraph_parser=parser,
#                           triple_yielder=triple_yielder,
#                           classpointers_parser=classpointers_parser,
#                           classrank_formatter=classrank_formater,
#                           damping_factor=0.9,
#                           class_security_threshold=1,
#                           instantiation_security_threshold=1)
#
# result_2 = classranker.generate_classrank()
# print result_2
#

########################################### DBPEDIA
#
# db_es_path = "C:\\Users\\Dani\\Documents\\EII\\doctorado\\PAPERS_PROPIOS\\classrank_dbpedia\\datasets\\mappingbased_objects_en_uris_es.ttl\\mappingbased_objects_en_uris_es.ttl"
# db_en_path = "C:\\Users\\Dani\\Documents\\EII\\doctorado\\PAPERS_PROPIOS\\classrank_dbpedia\\datasets\\mappingbased_objects_en.ttl\\db_en.ttl"
#
# parser = TtlSimpleDigraphParser(db_en_path)
#
# formater = RawPageRankFormatter()
#
# # pageranker = PageRanker(graph_parser=parser,
# #                         pagerank_formatter=formater,
# #                         damping_factor=0.85)
# # result = pageranker.generate_pagerank()
#
#
# classpointers_parser = OnePerLineClasspointerParser("files\\dbpedia_cps_tiny.tsv")
# classpointer_set = classpointers_parser.parse_classpointers()
# classpointer_str = RawClasspointerFormater().format_classpointers_set(classpointer_set)
#
#
# triple_yielder = TtlSimpleTriplesYielder(source_file=db_en_path)
# classrank_formater = SortedJsonFormatedInterface(target_file="files\\out\\CR_dbp_en_tiny.json")
#
# classranker = ClassRanker(digraph_parser=parser,
#                           triple_yielder=triple_yielder,
#                           classpointers_parser=classpointers_parser,
#                           classrank_formatter=classrank_formater,
#                           damping_factor=0.9,
#                           class_security_threshold=20,
#                           instantiation_security_threshold=20,
#                           max_edges=500000,
#                           max_iter_pagerank=250)
#
# result_2 = classranker.generate_classrank()
#
# print result_2
# print classranker.triples_analized
# print classranker.triples_with_error
# print "--------"
# print classranker.number_of_classes
# print classranker.number_of_entities



###### Classpointer candidates


# db_es_path = "C:\\Users\\Dani\\Documents\\EII\\doctorado\\PAPERS_PROPIOS\\classrank_dbpedia\\datasets\\mappingbased_objects_en_uris_es.ttl\\mappingbased_objects_en_uris_es.ttl"
# db_en_path = "C:\\Users\\Dani\\Documents\\EII\\doctorado\\PAPERS_PROPIOS\\classrank_dbpedia\\datasets\\mappingbased_objects_en.ttl\\db_en.ttl"
#
#
# triple_yielder = TtlSimpleTriplesYielder(source_file=db_en_path)
#
# candidates_finder = CpCandidatesFinder(triple_yielder=triple_yielder,
#                                        classpointers_formater=OnePerLineClasspointerFormatter(target_file="files\\out\\db_en_cps.tsv"),
#                                        class_security_threshold=15)
# print candidates_finder.generate_classpointer_candidates()


############### Full TTl parsers

# parser1 = TtlFullDigraphParser(source_file="files\\sample_ttl_full_tiny.ttl")
# graph1 = parser1.parse_graph(max_edges=4)
# for an_edge in graph1.edges_iter():
#     print an_edge
#
# print "Parsed", parser1.parsed_triples
# print "Ignored", parser1.ignored_triples
# print "Error", parser1.error_triples
#
# print "----------------"
#
# yielder2 = TtlFullTriplesYielder(source_file="files\\sample_ttl_full_tiny.ttl")
# for a_triple in yielder2.yield_triples(max_triples=4):
#     print a_triple
#
# print "Yielded", yielder2.yielded_triples
# print "Ignored", yielder2.ignored_triples
# print "Error", yielder2.error_triples


############### SImple Ttl parsers with triples involving literals and possibly b-nodes

person_data_en_path = "C:\\Users\\Dani\\Documents\\EII\\doctorado\\PAPERS_PROPIOS\\classrank_dbpedia\\datasets\\persondata_en.ttl\\persondata_en.ttl"
instances_en_path = "C:\\Users\\Dani\\Documents\\EII\\doctorado\\PAPERS_PROPIOS\\classrank_dbpedia\\datasets\\instance_types_en.ttl\\instance_types_en.ttl"
skos_cats_en_path = "C:\\Users\\Dani\\Documents\\EII\\doctorado\\PAPERS_PROPIOS\\classrank_dbpedia\\datasets\\skos_categories_en.ttl\\skos_categories_en.ttl"

yielder = TtlExplicitSpoTriplesYielder(source_file=person_data_en_path)
for a_triple in yielder.yield_triples(max_triples=1000):
    print a_triple, yielder.yielded_triples

print "Yielded", yielder.yielded_triples
print "Ignored", yielder.ignored_triples
print "Error", yielder.error_triples

print "--------------------"

parser = TtlExplicitSpoDigraphParser(person_data_en_path)
graph = parser.parse_graph(max_edges=1000)
for an_edge in graph.edges_iter():
    print an_edge

print "Parser", parser.parsed_triples
print "Ignored", parser.ignored_triples
print "Error", parser.error_triples


