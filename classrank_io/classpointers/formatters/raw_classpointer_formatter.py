
from classrank_io.classpointers.formatters.classpointer_formater_interface import ClasspointerFormatterInterface


class RawClasspointerFormater(ClasspointerFormatterInterface):

    def __init__(self):
        super(RawClasspointerFormater, self).__init__()


    def format_classpointers_set(self, set_classpointers):
        result = ""
        for an_elem in set_classpointers:
            result += str(an_elem) + "\n"
        return result