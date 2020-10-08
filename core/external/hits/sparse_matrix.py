_S = 0
_O = 1


class HITSSparseMatrix(object):
    def __init__(self, edges_yielder, max_edges):
        self._edges_yielder = edges_yielder
        self._max_edges = max_edges
        self._in_dict = {}  # Will be filled later
        self._out_dict = {}  # Will be filled later
        self._build_matrix()

    def incoming_edges(self, node):
        return self._in_dict[node]

    def outgoing_edges(self, node):
        return self._out_dict[node]

    @property
    def n_nodes(self):
        return len(self._in_dict)

    def yield_nodes(self):
        for a_node_key in self._in_dict:
            yield a_node_key

    def _build_matrix(self):
        for an_edge in self._edges_yielder.yield_edges(max_edges=self._max_edges):
            self._add_needed_entries_to_dict(an_edge)
            self._annotate_edge(an_edge)

    def _annotate_edge(self, edge):
        self._in_dict[edge[_O]].append(edge[_S])
        self._out_dict[edge[_S]].append(edge[_O])

    def _add_needed_entries_to_dict(self, edge):
        if edge[_O] not in self._in_dict:
            self._in_dict[edge[_O]] = []
            self._out_dict[edge[_O]] = []
        if edge[_S] not in self._in_dict:
            self._in_dict[edge[_S]] = []
            self._out_dict[edge[_S]] = []

