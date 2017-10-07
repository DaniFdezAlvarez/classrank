
from classrank_io.classpointers.formatters.classpointer_formater_interface import ClasspointerFormatterInterface


class OnePerLineClasspointerFormatter(ClasspointerFormatterInterface):

    def __init__(self, target_file):
        super(OnePerLineClasspointerFormatter, self).__init__()
        self._target_file = target_file


    def format_classpointers_set(self, set_classpointers):
        with open(self._target_file, "w") as out_stream:
            for elem in set_classpointers:
                out_stream.write(str(elem) + "\n")
        return "Classpointers succesfully written to: " + self._target_file
