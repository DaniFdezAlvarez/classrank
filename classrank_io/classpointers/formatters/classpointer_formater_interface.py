__author__ = "Dani"

class ClasspointerFormatterInterface(object):

    def __init__(self):
        pass

    def format_classpointers_set(self, set_classpointers):
        raise NotImplementedError("This method should be redefined")