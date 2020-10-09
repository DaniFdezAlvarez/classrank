from core.external.hits.sparse_matrix import HITSSparseMatrix
from core.external.exceptions import IterationException

class WesHITSer(object):

    def __init__(self, edges_yielder, max_iters=400, epsilon=1.0e-8, max_edges=-1):
        self._edges_yielder = edges_yielder
        self._maxiters = max_iters
        self._epsilon = epsilon
        self._max_edges=max_edges

        self._matrix = None
        self._node_positions = {}
        self._auth_scores = []
        self._hub_scores = []

        self._iterations_performed = 0


    @property
    def iterations_performed(self):
        return self._iterations_performed

    def compute_hits(self):
        try:
            self._init_structures()
            self._compute_hubs_and_auth()
            return self._produce_final_output()
        except ZeroDivisionError as e:
            raise ValueError("Cant compute HITS, one of the arrays completely turned into zero")

    def _produce_final_output(self):
        """
        Tuples with: (node, auth_score, hub_score)
        :return:
        """
        return [(a_node, self._auth_scores[a_position], self._hub_scores[a_position])
                for a_node, a_position in self._node_positions.items()]


    def _init_structures(self):
        self._matrix = HITSSparseMatrix(edges_yielder=self._edges_yielder,
                                        max_edges=self._max_edges)
        i = 0
        for a_node in self._matrix.yield_nodes():
            self._node_positions[a_node] = i
            self._auth_scores.append(1.0)  # Initial auth score
            self._hub_scores.append(1.0)  # Initial hub score
            i += 1

    def _compute_hubs_and_auth(self):
        ref_to_out_edges = self._matrix._out_dict
        ref_to_in_edges = self._matrix._in_dict

        # new_hubs = None
        # new_auths = None

        while self._iterations_performed <= self._maxiters:
            new_hubs, new_auths = self._perform_iteration(ref_to_in_edges=ref_to_in_edges,
                                                          ref_to_out_edges=ref_to_out_edges)
            if self._convergence_reached(new_auths=new_auths,
                                         new_hubs=new_hubs):
                self._hub_scores = new_hubs
                self._auth_scores = new_auths
                break
            self._hub_scores = new_hubs
            self._auth_scores = new_auths
        if self._iterations_performed >= self._maxiters:
            raise IterationException(num_iterations=self._maxiters)


    def _perform_iteration(self, ref_to_in_edges, ref_to_out_edges):
        new_hubs = []
        new_auths = []
        for a_node in self._node_positions:
            new_auth_score = 0.0
            for an_incoming_node in ref_to_in_edges[a_node]:  # _compute_new_auth()
                new_auth_score += self._hub_scores[self._node_positions[an_incoming_node]]
            new_auths.append(new_auth_score)
            new_hubs_score = 0.0
            for an_outgoing_edge in ref_to_out_edges[a_node]:  # _compute_new_hub()
                new_hubs_score += self._auth_scores[self._node_positions[an_outgoing_edge]]
            new_hubs.append(new_hubs_score)
        # normalize_lists  # _normalize_list()
        total_hubs = sum(new_hubs)
        total_auths = sum(new_auths)
        for i in range(0, len(new_hubs)):
            new_hubs[i] = new_hubs[i] / total_hubs
            new_auths[i] = new_auths[i] / total_auths

        self._iterations_performed += 1

        return new_hubs, new_auths


    def _normalize_list(self, a_list):
        total = sum(a_list)
        for i in range(0, len(a_list)):
            a_list[i] = a_list[i]/total


    def _convergence_reached(self, new_hubs, new_auths):
        if sum([abs(new_hubs[i] - self._hub_scores[i]) for  i in range(0, len(new_hubs))]) > self._epsilon or \
                sum([abs(new_auths[i] - self._auth_scores[i]) for  i in range(0, len(new_hubs))]) > self._epsilon:
            return False
        return True
        # for i in range(0, len(new_hubs)):
        #     if abs(new_hubs[i] - self._hub_scores[i]) > self._epsilon or \
        #             abs(new_auths[i] - self._auth_scores[i]) > self._epsilon:
        #         return False
        # return True

    def _compute_new_auth(self, ref_to_in_edges, a_node):
        result = 0.0
        for an_incoming_node in ref_to_in_edges[a_node]:
            result += self._hub_scores[self._node_positions[an_incoming_node]]
        return result

    def _compute_new_hub(self, ref_to_out_edges, a_node):
        result = 0.0
        for an_outgoing_edge in ref_to_out_edges[a_node]:
            result += self._auth_scores[self._node_positions[an_outgoing_edge]]
        return result