from classrank_io.classpointers.parsers.classpointer_parser_interface import ClasspointerParserInterface


class OnePerLineClasspointerParser(ClasspointerParserInterface):

    def __init__(self, source_file):
        super(OnePerLineClasspointerParser, self).__init__()
        self._source_file = source_file
        self._err_count = 0
        self._line_count = 0


    def parse_classpointers(self):
        result = set()
        with open(self._source_file, "r") as input_io:
            for a_line in input_io:
                a_classpointer = self._get_classpointer_from_line(a_line)
                if a_classpointer is not None:
                    self._line_count += 1
                    result.add(a_classpointer)
                else:
                    self._err_count += 1
        return result

    def _get_classpointer_from_line(self, a_line):
        result = a_line.strip()
        if result not in ["", None]:
            return result
        return None


