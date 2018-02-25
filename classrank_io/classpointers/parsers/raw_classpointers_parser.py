from classrank_io.classpointers.parsers.classpointer_parser_interface import ClasspointerParserInterface

class RawClasspointerParser(ClasspointerParserInterface):
    def __init__(self, list_of_classpointers):
        super(RawClasspointerParser, self).__init__()
        self._set_of_classpointers = set(list_of_classpointers)

    def parse_classpointers(self):
        """
        It returns a set of classpointers

        :return:
        """
        return self._set_of_classpointers