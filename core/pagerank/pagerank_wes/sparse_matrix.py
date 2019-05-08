from classrank_io.graph.yielders.tsv_edges_yielder import TsvEdgesYielder


class SMatrix(object):

    def __init__(self, d=0.85, source_file=None, raw_graph=None):
        self._source_file = None
        self._raw_graph = None
        self._rows = {}
        self._n_nodes = 0  # Will change later
        self._base_score = 0  # Will change_later
        self._dict_degrees = {}
        self._staying_probability = d
        self._jumping_probability = 1 - d
        self._load_matrix()

    @property
    def n_nodes(self):
        return self._n_nodes

    def yield_node_ids(self):
        for a_key in self._dict_degrees:
            yield a_key

    def _load_matrix(self):
        yielder = TsvEdgesYielder(source_file=self._source_file,
                                  raw_graph=self._raw_graph)
        for an_edge in yielder.yield_edges():
            self._include_nodes_if_needed(an_edge)
            self._dict_degrees[an_edge[0]] += 1
            self._rows[an_edge[1]].add(an_edge[0])
        self._set_base_values()

    def _set_base_values(self):
        self._n_nodes = len(self._dict_degrees)
        self._base_score = self._jumping_probability / self._n_nodes

    def _include_nodes_if_needed(self, an_edge):
        for elem in an_edge:
            if elem not in self._dict_degrees:
                self._dict_degrees[elem] = 0
        if an_edge[1] not in self._rows:  # an_edge[1] = subject
            self._rows[an_edge[1]] = set()

    def get(self, row, col):
        if row not in self._rows or col not in self._rows[col] :
            return self._base_score
        #else
        return self._base_score + (self._staying_probability / self._dict_degrees[col])


