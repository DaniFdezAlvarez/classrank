"""
Object able to transform a certain source (a file, some online content, raw text...) into a
directed graph of the library networkx  ---> networkx.DiGraph().

The main funcionallity of the instantiated objects should be encapsulated in the method "parse_graph()".
The params of the __init__ method may defer depending on the nature of the targeted source.
"""


class DiGraphParserInterface(object):
    def __init__(self):
        pass

    def parse_graph(self, max_edges=-1):
        """
        It returns an object networkx.DiGraph() containing edges between the s and o of every
        triple (s, p, o)

        If max_edges has a posotive value, the returned graph should contain just the first
        $max_edges in the source at most
        :param max_edges:
        :return:
        """
        raise NotImplementedError("Method should be redefined")
