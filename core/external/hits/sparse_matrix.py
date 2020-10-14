import array

_S = 0
_O = 1

IN_EDGES = 0
OUT_EDGES = 1

_ARRAY_TYPE = 'i'


class HITSSparseMatrix(object):
    def __init__(self, edges_yielder, max_edges):
        self._edges_yielder = edges_yielder
        self._max_edges = max_edges
        self._nodes_dict = {} # Will be initialized later
        self._build_matrix()

    def incoming_edges(self, node):
        return self._nodes_dict[node][IN_EDGES]

    def outgoing_edges(self, node):
        return self._nodes_dict[node][OUT_EDGES]

    @property
    def n_nodes(self):
        return len(self._nodes_dict)

    def yield_nodes(self):
        for a_node_key in self._nodes_dict:
            yield a_node_key

    def _build_matrix(self):
        for an_edge in self._edges_yielder.yield_edges(max_edges=self._max_edges):
            self._add_needed_entries_to_dict(an_edge)
            self._annotate_edge(an_edge)
        self._remove_repeated_nodes()

    def _annotate_edge(self, edge):
        self._nodes_dict[edge[_O]][IN_EDGES].append(edge[_S])
        self._nodes_dict[edge[_S]][OUT_EDGES].append(edge[_O])

    def _add_needed_entries_to_dict(self, edge):
        if edge[_O] not in self._nodes_dict:
            self._nodes_dict[edge[_O]] = ([], [])

        if edge[_S] not in self._nodes_dict:
            self._nodes_dict[edge[_S]] = ([], [])

    def _remove_repeated_nodes(self):
        for a_node_key in self._nodes_dict:
            self._nodes_dict[a_node_key] = (
                list(set(self._nodes_dict[a_node_key][0])),
                list(set(self._nodes_dict[a_node_key][1]))
            )


class HITSSparseMatrixWikidata(object):
    def __init__(self, edges_yielder, max_edges):
        self._edges_yielder = edges_yielder
        self._max_edges = max_edges
        self._nodes_dict = {}  # Will be initialized later
        self._build_matrix()

    def incoming_edges(self, node):
        return self._nodes_dict[node][IN_EDGES]

    def outgoing_edges(self, node):
        return self._nodes_dict[node][OUT_EDGES]

    @property
    def n_nodes(self):
        return len(self._nodes_dict)

    def yield_nodes(self):
        for a_node_key in self._nodes_dict:
            yield a_node_key

    def _build_matrix(self):
        for an_edge in self._edges_yielder.yield_edges(max_edges=self._max_edges):
            integer_edge = (self.qid_to_int(an_edge[0]), self.qid_to_int(an_edge[1]))
            self._add_needed_entries_to_dict(integer_edge)
            self._annotate_edge(integer_edge)
        self._remove_repeated_nodes()

    def _annotate_edge(self, edge):
        self._nodes_dict[edge[_O]][IN_EDGES].append(edge[_S])
        self._nodes_dict[edge[_S]][OUT_EDGES].append(edge[_O])

    def _add_needed_entries_to_dict(self, edge):
        if edge[_O] not in self._nodes_dict:
            self._nodes_dict[edge[_O]] = (array.array(_ARRAY_TYPE), array.array(_ARRAY_TYPE))

        if edge[_S] not in self._nodes_dict:
            self._nodes_dict[edge[_S]] = (array.array(_ARRAY_TYPE), array.array(_ARRAY_TYPE))

    def _remove_repeated_nodes(self):
        for a_node_key in self._nodes_dict:
            self._nodes_dict[a_node_key] = (
                array.array(_ARRAY_TYPE, list(set(self._nodes_dict[a_node_key][0]))),
                array.array(_ARRAY_TYPE, list(set(self._nodes_dict[a_node_key][1])))
            )


    @staticmethod
    def qid_to_int(qid):
        return int(qid[1:])

    @staticmethod
    def int_to_qid(an_int):
        return "Q" + str(an_int)
