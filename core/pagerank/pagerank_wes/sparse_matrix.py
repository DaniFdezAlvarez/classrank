from classrank_io.graph.yielders.tsv_edges_yielder import TsvEdgesYielder
from classrank_io.graph.yielders.ttl_explicit_spo_triples_yielder import TtlExplicitSpoTriplesYielder


class SMatrix(object):
    def __init__(self, d=0.85, source_file=None, raw_graph=None, max_edges=-1, base_yielder=None):
        self._source_file = source_file
        self._base_yielder = base_yielder
        self._raw_graph = raw_graph
        self._rows = {}
        self._cols = {}
        self._n_nodes = 0  # Will change later
        self._base_score = 0  # Will change_later
        self._sink_score = 0  # Will change_later
        self._dict_degrees = {}
        self._staying_probability = d
        self._jumping_probability = 1 - d
        self._max_edges = max_edges
        self._dangling_nodes = set()  # Will be filled later
        self._non_dangling_nodes = set()  # Will be filled later
        self._unreached_nodes = set()  # Will be filled later
        self._load_matrix()


    @property
    def sink_score(self):
        return self._sink_score

    @property
    def base_score(self):
        return self._base_score

    @property
    def unreached_nodes(self):
        return self._unreached_nodes
    @property
    def dangling_nodes(self):
        return self._dangling_nodes

    @property
    def non_dangling_nodes(self):
        return self._non_dangling_nodes

    @property
    def alpha(self):
        return self._jumping_probability

    @property
    def d(self):
        return self._staying_probability

    @property
    def n_nodes(self):
        return self._n_nodes

    def yield_node_ids(self):
        for a_key in self._dict_degrees:
            yield a_key

    def _load_matrix(self):
        yielder = TsvEdgesYielder(TtlExplicitSpoTriplesYielder(source_file=self._source_file)) \
            if self._source_file is not None else TsvEdgesYielder(self._base_yielder)
        nodes_reached = set()
        for an_edge in yielder.yield_edges(self._max_edges):
            self._include_nodes_if_needed(an_edge)
            self._dict_degrees[an_edge[0]] += 1
            # self._rows[an_edge[1]].add(an_edge[0])
            self._cols[an_edge[0]].add(an_edge[1])
            nodes_reached.add(an_edge[0])
        self._set_base_values()
        self._fill_relevant_node_sets(nodes_reached)

    def _set_base_values(self):
        self._n_nodes = len(self._dict_degrees)
        self._base_score = self._jumping_probability / self._n_nodes
        self._sink_score = 1.0 / self._n_nodes

    def _fill_relevant_node_sets(self, nodes_reached):
        for a_key in self._dict_degrees:
            if self._dict_degrees[a_key] == 0:
                self._dangling_nodes.add(a_key)
            else:
                self._non_dangling_nodes.add(a_key)
            if a_key not in nodes_reached:
                self._unreached_nodes.add(a_key)

    def _include_nodes_if_needed(self, an_edge):
        for elem in an_edge:
            if elem not in self._dict_degrees:
                self._dict_degrees[elem] = 0
        # if an_edge[1] not in self._rows:  # an_edge[1] = subject
        #     self._rows[an_edge[1]] = set()

        if an_edge[0] not in self._cols:
            self._cols[an_edge[0]] = set()

    def get_col(self, col_key):
        return self._cols[col_key]

    def get_degree_of_node(self, node):
        return self._dict_degrees[node]

    # def get(self, row, col):
    #     return 0
    #     # if self._dict_degrees[col] == 0:
    #     #     return self._sink_score
    #     # elif row not in self._rows or col not in self._rows[row]:
    #     #     return self._base_score
    #     # ##### else
    #     # return self._base_score + (self._staying_probability / self._dict_degrees[col])

    # def __init__(self, d=0.85, source_file=None, raw_graph=None, max_edges=-1):
    #     self._source_file = source_file
    #     self._raw_graph = raw_graph
    #     self._rows = []  # Will be a list of sets later
    #     self._n_nodes = 0  # Will change later
    #     self._base_score = 0  # Will change_later
    #     self._sink_score = 0  # Will change_later
    #     self._dict_degrees = {}
    #     self._staying_probability = d
    #     self._jumping_probability = 1 - d
    #     self._max_edges = max_edges
    #     self._node_index = {}
    #     self._load_matrix()
    #
    #
    # @property
    # def n_nodes(self):
    #     return self._n_nodes
    #
    # def yield_node_ids(self):
    #     for a_key in self._dict_degrees:
    #         yield a_key
    #
    # def _load_matrix(self):
    #     self._rows = {}  # Will change into list later
    #     yielder = TsvEdgesYielder(TtlExplicitSpoTriplesYielder(source_file=self._source_file))
    #     for an_edge in yielder.yield_edges(self._max_edges):
    #         self._include_nodes_if_needed(an_edge)
    #         self._dict_degrees[an_edge[0]] += 1
    #         self._rows[an_edge[1]].add(an_edge[0])
    #     self._set_base_values()
    #     self._turn_row_dict_into_list()
    #
    # def _set_base_values(self):
    #     self._n_nodes = len(self._dict_degrees)
    #     self._base_score = self._jumping_probability / self._n_nodes
    #     self._sink_score = 1.0 / self._n_nodes
    #
    # def _turn_row_dict_into_list(self):
    #     new_rows = []
    #     i = 0
    #     for a_key in self._dict_degrees:
    #         if a_key in self._rows:
    #             new_rows.append(self._rows[a_key])
    #         else:
    #             new_rows.append(set())
    #         self._node_index[i] = a_key
    #         i += 1
    #     self._rows = new_rows
    #
    # def _include_nodes_if_needed(self, an_edge):
    #     for elem in an_edge:
    #         if elem not in self._dict_degrees:
    #             self._dict_degrees[elem] = 0
    #     if an_edge[1] not in self._rows:  # an_edge[1] = subject
    #         self._rows[an_edge[1]] = set()
    #
    # def get(self, row, col):
    #     if self._dict_degrees[self._node_index[col]] == 0:
    #         return self._sink_score
    #     elif len(self._rows[row]) == 0 or col not in self._rows[row]:
    #         return self._base_score
    #     #else
    #     return self._base_score + (self._staying_probability / self._dict_degrees[col])


