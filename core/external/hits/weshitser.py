from core.external.hits.sparse_matrix import HITSSparseMatrix
from core.external.exceptions import IterationException, UnlikelyConvergenceException
import array

_ARRAY_TYPE = 'f'

class WesHITSer(object):

    def __init__(self, edges_yielder, max_iters=400, epsilon=1.0e-8, max_edges=-1, longest_posible_streak=40):
        self._edges_yielder = edges_yielder
        self._maxiters = max_iters
        self._epsilon = epsilon
        self._max_edges=max_edges
        self._longst_possible_streak = longest_posible_streak

        self._matrix = None
        self._node_positions = {}
        self._auth_scores = None  # Will be array
        self._hub_scores = None  # Will be array
        self._old_non_convergent_nodes = 0  # Will be managed_later
        self._same_non_convergence_strike = 0  # Will be managed_later
        self._iterations_performed = 0  # Will be managed_later
        self._n_nodes = 0  # Will be managed_later


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
        finally:
            #Free memory
            self._hub_scores = None
            self._auth_scores = None

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
            # self._auth_scores.append(1.0)  # Initial auth score
            # self._hub_scores.append(1.0)  # Initial hub score
            i += 1
        self._hub_scores = array.array(_ARRAY_TYPE, (1.0 for _ in range(0, i)))
        self._auth_scores = array.array(_ARRAY_TYPE, (1.0 for _ in range(0, i)))
        self._old_non_convergent_nodes = i
        self._n_nodes = i

    def _compute_hubs_and_auth(self):
        ref_to_out_edges = self._matrix._out_dict
        ref_to_in_edges = self._matrix._in_dict

        # new_hubs = None
        # new_auths = None

        while self._iterations_performed <= self._maxiters:
            new_hubs, new_auths = self._perform_iteration(ref_to_in_edges=ref_to_in_edges,
                                                          ref_to_out_edges=ref_to_out_edges)
            try:
                if self._convergence_reached(new_auths=new_auths):
                    self._hub_scores = new_hubs
                    self._auth_scores = new_auths
                    break
                self._hub_scores = new_hubs
                self._auth_scores = new_auths
            except UnlikelyConvergenceException as e:
                print("WARNING: returning results but consider the following: " + str(e))
                self._hub_scores = new_hubs
                self._auth_scores = new_auths
                break
        if self._iterations_performed >= self._maxiters:
            raise IterationException(num_iterations=self._maxiters)

    def _perform_iteration(self, ref_to_in_edges, ref_to_out_edges):
        new_hubs = array.array(_ARRAY_TYPE)
        new_auths = array.array(_ARRAY_TYPE)
        for a_node in self._matrix.yield_nodes():
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

    def _convergence_reached(self, new_auths):
        res = 0.0
        non_convergent_nodes = 0
        for i in range(self._n_nodes):
            min_res = abs(new_auths[i] - self._auth_scores[i])
            if min_res > self._epsilon:
                non_convergent_nodes += 1
            res += min_res
        if self._old_non_convergent_nodes == non_convergent_nodes:
            self._same_non_convergence_strike += 1
        else:
            self._same_non_convergence_strike = 0
            self._old_non_convergent_nodes = non_convergent_nodes
        if self._same_non_convergence_strike >= self._longst_possible_streak:
            raise UnlikelyConvergenceException(non_convergent_nodes)   # TODO continue here
        return res < self._epsilon

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