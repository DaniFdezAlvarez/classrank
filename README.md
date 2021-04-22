# ClassRank

This repository contains a Python implementation of the algorithm ClassRank. ClassRank is a novel technique handy for measuring the relevance of each class in a RDF graph.

We provide [an online demo of Classrank][demo_online] which also includes an overview of the algorithm. 

Prerequisites
-------------

- Python 3 (64-bit version if you want to compute huge datastes)
- All the libraries listed in the file requirements.txt

Execution
---------
At the moment we are not providing installing methods, just the original python scripts. If you are planning to integrate this code with some other project you may have to deal with issues related to paths. We will be providing nicer ways to interact with this library soon.

Example code
------------

The easiest way to execute ClassRank is using the function 'generate_pagerank()' located in helpers.classrank:

    
    from helpers.classrank import generate_classrank
    
    print(generate_classrank(graph_file="path/to/some/file.ttl",
                             raw_classpointers="http://www.w3.org/1999/02/22-rdf-syntax-ns#type",
                             string_return=True,
                             instantiation_threshold=1,
                             class_threshold=1))

    
By executing the previous code providing the path to some graph with the param ``graph_file`` you will print a JSON representation of the ClassRank scores of the classes detected in the graph, as well as the list of instances pointing them with ``rdf:type``.  The function generate_classrank admits a large list of optional params to configure its behaviour:

    def generate_classrank(damping_factor=0.85, max_iters=250, instantiation_threshold=15, class_threshold=15,
                       max_triples=-1, graph_format=TTL_FULL_FORMAT, output_format=JSON_FULL_OUTPUT, graph_file=None,
                       classpointers_file=None, raw_graph=None, raw_classpointers=None,
                       output_file=None, string_return=False):
                       
    :param damping_factor: Damping factor for PageRank execution. 
    :param max_iters: Max iterations por PageRank execution. 
    :param instantiation_threshold: Instance threshold for ClassRank. 
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
     

Alternatively, you can execute the algorithm using the class ClassRanker:

    from classrank_io.graph.parsers.ttl_full_digraph_parser import TtlFullDigraphParser
    from classrank_io.classpointers.parsers.one_per_line_classpointer_parser import OnePerLineClasspointerParser
    from classrank_io.graph.yielders.ttl_full_triples_yielder import TtlFullTriplesYielder
    from classrank_io.graph.formatters.classrank.sorted_json_classrank_formatter import SortedJsonClassrankFormatter
    from classranker import ClassRanker
    
    graph_path = "path/to/some/graph.ttl"
    cp_path = "path/to/some/classpointers.txt"
    
    parser = TtlFullDigraphParser(graph_path)
    classpointers_parser = OnePerLineClasspointerParser(cp_path)
    triple_yielder = TtlFullTriplesYielder(graph_path)
    classrank_formater = SortedJsonClassrankFormatter(target_file="path/to/serialize/results.json")

    classranker = ClassRanker(digraph_parser=parser,
                              triple_yielder=triple_yielder,
                              classpointers_parser=classpointers_parser,
                              classrank_formatter=classrank_formater,
                              damping_factor=0.9,
                              class_security_threshold=20,
                              instantiation_security_threshold=20,
                              max_edges=500000,
                              max_iter_pagerank=250)
     
     classranker.generate_classrank()
     
The ClassRankers objects need 4 extra objects to read the graph/classpointers and to return/serialize the results.
- digraph_parser: It reads the target graph and returns an object of type networkx.Graph(). Interface:  classrank_io.graph.parsers.digraph_parser_interface.DiGraphParserInterface
- triple_yielder: It reads the target graph and yields 3-tuples (using Python generators) of the form s,p,o representing parsed triples. . Interface: classrank_io.graph.yielders.triples_yielder_interface.TriplesYielderInterface
- classpointers_parser: It reads the Classpointer list an return a Python list containing all of them. Interface: classrank_io.classpointers.parsers.classpointer_parser_interface.ClasspointerParserInterface
- classrank_formater: It turns in-memory results of ClassRank into some representation, possibly serializing it. Interface: classrank_io.graph.formatters.classrank.classrank_formatter_interface.ClassRankFormatterInterface
     


Contributing
------------
Theoretically, ClassRank can be applied to any kind of directed graph. This prototype is ready to compute a limited set of formats. However, it has been developed following a modular architecture that allows to easily add new formats by implementing some ad-hoc parsers or formatters. If you want to analize some graph in any other format than turtle, you could implement the correspondent parsers, yielders or formaters following the interfaces listed in the previous section.

Contact
-------

Feel free to create issues or to reach me at danifdezalvarez@gmail.com 


[demo_online]: http://boa.weso.es/
