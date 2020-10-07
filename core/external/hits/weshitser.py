from core.external.hits.sparse_matrix import HITSSparseMatrix

class WesHITSer(object):

    def __init__(self, edges_yielder, max_iters=400, epsilon=1.0e-8):
        self._edges_yielder = edges_yielder
        self._maxiters = max_iters
        self._epsilon = epsilon

        self._matrix = None
        self._node_positions = []
        self._auth_scores = []
        self._hub_scores = []

        self._iteration_performed = 0


    @property
    def iterations_performed(self):
        return self._iteration_performed

    def compute_hits(self):
        self._init_structures()
        self._compute_hubs_and_auth()


    def _init_structures(self):
        self._matrix = HITSSparseMatrix(edges_yielder=self._edges_yielder)
        i = 0
        for a_node in self._matrix.yield_nodes():
            self._node_positions[a_node] = i
            self._auth_scores.append(1.0)  # Initial auth score
            self._hub_scores.append(1.0)  # Initial hub score

    def _compute_hubs_and_auth(self):
        ref_to_out_edges = self._matrix._out_dict
        ref_to_in_edges = self._matrix._in_dict

        while(not self._convergence_reached()):
            new_hubs = []
            new_auths = []
            for a_node in self._node_positions:
                new_hubs.append(self._compute_new_auth(ref_to_in_edges, a_node))
                new_auths.append(self._compute_new_hub(ref_to_out_edges, a_node))
            self._normalize_list(new_hubs)
            self._normalize_list(new_auths)


    def _normalize_list(self, a_list):
        total = sum(a_list)
        for i in range(0, len(a_list)):
            a_list[i] = a_list[i]/total


    def _convergence_reached(self):
        pass  # TODO check epsilon

    def _compute_new_auth(self, ref_to_in_edges, a_node):
        result = 0
        for an_incoming_node in ref_to_in_edges[a_node]:
            result += self._hub_scores[self._node_positions[an_incoming_node]]
        return result

    def _compute_new_hub(self, ref_to_out_edges, a_node):
        result = 0
        for an_outgoing_edge in ref_to_out_edges[a_node]:
            result += self._auth_scores[self._node_positions[an_outgoing_edge]]
        return result