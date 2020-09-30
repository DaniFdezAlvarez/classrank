class DirectedGraphDumpFilter(object):
    def __init__(self, triples_yielder, target_file, separator="\t", multifilter_compatibility=False):
        self._triples_yielder = triples_yielder
        self._target_file = target_file
        self._separator = separator

        self._out_stream = None if not multifilter_compatibility else open(self._target_file, "w")

    def generate_filter(self):
        with open(self._target_file, "w") as out_stream:
            for a_triple in self._triples_yielder:
                self._write_line(line=self._triple_to_adequate_line(a_triple),
                                 stream=out_stream)

    def process_triple(self, a_triple):
        """
        This is thought to be used just with multifilter_compatibility mode.
        Invoke to process a single triple.

        :param a_triple:
        :return:
        """
        self._write_line(line=self._triple_to_adequate_line(a_triple),
                         stream=self._out_stream)

    def close_filter(self):
        """
        This is thought to be used just with multifilter_compatibility mode.
        Invoke when all the triples has been processed

        :return:
        """

        #TODO continue here


    def _triple_to_adequate_line(self, a_triple):
        return self._separator.join([a_triple[0], a_triple[2]])

    def _write_line(self, line, stream):
        stream.write(line + "\n")


class DirectedGraphSlicerDumpFilter(object):
    def __init__(self, triples_yielder, base_file_path, max_triples_per_file=1000000, multifilter_compatibility=False):
        pass


class ClassCountDumpFilter(object):
    def __init__(self, triples_yielder, classpointers, multifilter_compatibility=False):
        pass


class MultiDumpFilter(object):
    def __init__(self, triples_yielder):
        pass