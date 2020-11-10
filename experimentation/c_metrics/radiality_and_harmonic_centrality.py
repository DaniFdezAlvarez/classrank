from experimentation.c_metrics.base_c_metric import BaseCMetric
from classrank_utils.g_paths import nx_diameter, shortest_path, build_graph_for_paths
from classrank_utils.scores import normalize_score
import multiprocessing as mp

_POS_RAD_DICT = 0
_POS_HARM_DICT = 1


class ParallelRadialityAndHarmonicCentrality(BaseCMetric):

    def __init__(self, triples_yielder, n_threads, normalize=True):
        super().__init__()
        self._nxgraph = build_graph_for_paths(triples_yielder=triples_yielder)
        self._infinite_walk = self._create_infinite_walk()
        self._harmonic_dict = {}
        self._radiality_dict = {}
        self._diameter = 0  # Will be filled later
        self._n_threads = n_threads
        self._normalize = normalize

    def run(self):
        self._diameter = nx_diameter(self._nxgraph)
        manager, queue = self._init_nodes_queue()
        self._run_processes(manager=manager,
                            queue=queue,
                            harm_dict=self._harmonic_dict,
                            rad_dict=self._radiality_dict,
                            nxgraph=self._nxgraph)
        if self._normalize:
            self._normalize_dict(self._harmonic_dict)
            self._normalize_dict(self._radiality_dict)

        self._return_result(obj_result=self._harmonic_dict,
                            string_return=False,
                            out_path=self._out_path_harmonic)



    def _normalize_dict(self, a_dict):
        max_score = self._find_max_score(a_dict)
        for a_node_key in a_dict:
            a_dict[a_node_key] = normalize_score(score=a_dict[a_node_key],
                                                 max_score=max_score)

    def _find_max_score(self, a_dict):
        return max([a_dict[an_uri] for an_uri in a_dict])

    def _run_processes(self, manager, queue, rad_dict, harm_dict, nxgraph):
        lock = mp.Lock()
        list_result = manager.List()
        list_result[_POS_RAD_DICT] = rad_dict
        list_result[_POS_HARM_DICT] = harm_dict
        processes = [mp.Process(target=self._parallel_node_scoring,
                                args=(queue, list_result, nxgraph.copy(as_view=True), lock)) for _ in
                     range(self._n_threads)]
        for p in processes:
            p.start()
        for p in processes:
            p.join()

    def _init_nodes_queue(self):
        manager = mp.Manager()
        queue = manager.Queue()
        for a_node in self._nxgraph.nodes:
            queue.put(a_node)
        return manager, queue

    def _parallel_node_scoring(self, queue, list_result, g_view, lock):
        while True:
            lock.acquire()
            if queue.empty():
                lock.release()
                break
            node = queue.get()
            lock.release()
            harm_score, rad_score = self._harm_and_rad_scores_of_a_node(a_node=node,
                                                                        diameter=self._diameter,
                                                                        g_view=g_view)
            lock.acquire()
            list_result[_POS_HARM_DICT][node] = harm_score
            list_result[_POS_RAD_DICT][node] = rad_score
            lock.release()

    def _harm_and_rad_scores_of_a_node(self, a_node, diameter, g_view):
        paths = shortest_path(graph=g_view,
                              origin=a_node)
        self._fill_absent_paths_with_an_all_nodes_walk(paths_dict=paths,
                                                       origin=a_node)
        self._delete_auto_paths(paths_dict=paths,
                                origin=a_node)

        denominator_rad = sum([diameter - (float(1) / len(paths[a_path_key])) for a_path_key in paths])
        denominator_harm = sum([len(paths[a_path_key]) for a_path_key in paths])

        return (float(1) / denominator_harm), float(1) / denominator_rad

    def _create_infinite_walk(self):
        return [node for node in self._nxgraph.nodes]

    def _fill_absent_paths_with_an_all_nodes_walk(self, paths_dict, origin):
        for a_node in self._nxgraph.nodes:
            if a_node != origin:
                if a_node not in paths_dict:
                    paths_dict[a_node] = self._infinite_walk

    def _delete_auto_paths(self, paths_dict, origin):
        if origin in paths_dict:
            del paths_dict[origin]
