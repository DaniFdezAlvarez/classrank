
class ClassRankAdapterInterface(object):

    def __init__(self, source_path):
        self._source_path = source_path


    def adapt_file(self):
        raise NotImplementedError("Should be implemented")