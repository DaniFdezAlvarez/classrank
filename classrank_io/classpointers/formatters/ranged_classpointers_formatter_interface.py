__author__ = "Dani"

class RangedClasspointersFormatterInterface(object):

    def __init__(self):
        pass

    def format_dict_of_classpointers_result(self, dict_of_classpointers_results):
        raise NotImplementedError("This method should be redefined")