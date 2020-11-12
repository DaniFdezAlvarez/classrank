from experimentation.c_metrics.base_c_metric import BaseCMetric
from classrank_utils.g_paths import shortest_path, build_graph_for_paths
from classrank_utils.scores import normalize_score
import multiprocessing as mp

_POS_RAD_DICT = 0
_POS_HARM_DICT = 1
_POS_TMP_DIAMETER = 2


class ParallelRadialityAndHarmonicCentrality(BaseCMetric):

    def __init__(self, triples_yielder, n_threads, out_path_harmonic, out_path_radiality, normalize=True):
        super().__init__()
        self._nxgraph = build_graph_for_paths(triples_yielder=triples_yielder)
        self._infinite_walk = self._create_infinite_walk()
        self._harmonic_dict = {}
        self._radiality_dict = {}
        self._diameter = 0  # Will be filled later
        self._n_threads = n_threads
        self._normalize = normalize
        self._out_path_harmonic = out_path_harmonic
        self._out_path_radiality = out_path_radiality

    def run(self):
        manager, queue = self._init_nodes_queue()
        self._run_processes(manager=manager,
                            queue=queue)

        self._recompute_radiality_with_diameter()

        if self._normalize:
            self._normalize_dict(self._harmonic_dict)
            self._normalize_dict(self._radiality_dict)

        self._return_result(obj_result=self._harmonic_dict.copy(),
                            string_return=False,
                            out_path=self._out_path_harmonic)

        self._return_result(obj_result=self._radiality_dict.copy(),
                            string_return=False,
                            out_path=self._out_path_radiality)

    def _recompute_radiality_with_diameter(self):
        for a_node_key in self._radiality_dict.keys():
            self._radiality_dict[a_node_key] = sum([self._diameter - (float(1) / a_len)
                                                    for a_len in self._radiality_dict[a_node_key]])

    def _normalize_dict(self, a_dict):
        max_score = self._find_max_score(a_dict)
        for a_node_key in a_dict.keys():
            a_dict[a_node_key] = normalize_score(score=a_dict[a_node_key],
                                                 max_score=max_score)

    def _find_max_score(self, a_dict):
        return max(a_dict.values())

    def _run_processes(self, manager, queue):
        lock_queue = mp.Lock()
        lock_list = mp.Lock()
        list_result = manager.list()
        list_result.append(manager.dict())  # 0
        list_result.append(manager.dict())  # 1
        list_result.append(0)  # 2
        processes = [mp.Process(target=self._parallel_node_scoring,
                                args=(queue, list_result, self._nxgraph.copy(as_view=True), lock_queue, lock_list)) for _ in
                     range(self._n_threads)]
        for p in processes:
            p.start()
        for p in processes:
            p.join()

        self._harmonic_dict = list_result[_POS_HARM_DICT]
        self._radiality_dict = list_result[_POS_RAD_DICT]
        self._diameter = list_result[_POS_TMP_DIAMETER]

    def _init_nodes_queue(self):
        manager = mp.Manager()
        queue = manager.Queue()
        for a_node in self._nxgraph.nodes:
            queue.put(a_node)
        return manager, queue

    def _parallel_node_scoring(self, queue, list_result, g_view, lock_queue, lock_list):
        while True:
            lock_queue.acquire()
            if queue.empty():
                lock_queue.release()
                break
            node = queue.get()
            lock_queue.release()
            self._harm_and_rad_scores_of_a_node(a_node=node,
                                                g_view=g_view,
                                                list_result=list_result,
                                                lock=lock_list)

    def _harm_and_rad_scores_of_a_node(self, a_node, list_result, g_view, lock):
        paths = shortest_path(graph=g_view,
                              origin=a_node)
        max_length = max([len(a_path) for a_path in paths.values()])
        if max_length > list_result[_POS_TMP_DIAMETER]:
            lock.acquire()
            list_result[_POS_TMP_DIAMETER] = max_length
            lock.release()
        self._fill_absent_paths_with_an_all_nodes_walk(paths_dict=paths,
                                                       origin=a_node)
        self._delete_auto_paths(paths_dict=paths,
                                origin=a_node)

        denominator_harm = sum([len(paths[a_path_key]) for a_path_key in paths])
        list_lenghts = [len(paths[a_path_key]) for a_path_key in paths]
        lock.acquire()
        list_result[_POS_HARM_DICT][a_node] = float(1) / denominator_harm
        list_result[_POS_RAD_DICT][a_node] = list_lenghts
        lock.release()


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
