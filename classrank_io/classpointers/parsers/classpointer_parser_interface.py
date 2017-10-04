"""
Object able to transform a certain source (a file, some online content, raw text...) into a set of classpointers.

The main funcionallity of the instantiated objects should be encapsulated in the method "parse_classpointers()".
The params of the __init__ method may defer depending on the nature of the targeted source.
"""


class ClasspointerParserInterface(object):
    def __init__(self):
        pass

    def parse_classpointers(self):
        """
        It returns a set of classpointers

        :return:
        """
        raise NotImplementedError("Method should be redefined")
