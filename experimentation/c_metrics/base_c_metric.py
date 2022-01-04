from classrank_io.json_io import json_obj_to_string, write_obj_to_json
from classrank_utils.g_paths import shortest_path, EfficientShortPathCalculator, MAX_AVAILABLE, \
    fill_absent_paths_with_an_all_nodes_walk, delete_auto_path

NX_COMPUTATION = "nx"
PARALLEL_COMPUTATION = "custom"


class BaseCMetric(object):

    def __init__(self, shortest_paths_dict=None, shortest_paths_computation=NX_COMPUTATION, nxgraph=None,
                 tunned_shortest_paths_dict=None):
        self._shortest_paths = shortest_paths_dict
        self._tunned_shortest_path_dict = tunned_shortest_paths_dict
        self._computation_choice = shortest_paths_computation
        self._nxgraph = nxgraph

    def _get_shortest_paths(self, graph=None):
        g = graph if graph is not None else self._nxgraph
        if self._shortest_paths is not None and (graph is None or graph == self._nxgraph):
            return self._shortest_paths
        else:
            return self._compute_shortest_paths(g)

    def _get_tunned_shortest_paths(self, graph=None):
        if self._tunned_shortest_path_dict is not None and (graph is None or graph == self._nxgraph):
            return self._tunned_shortest_path_dict
        g = graph if graph is not None else self._nxgraph
        result = self._get_shortest_paths(graph=g)
        fill_absent_paths_with_an_all_nodes_walk(paths_dict=result,
                                                 target_nodes=g.nodes)
        delete_auto_path(paths_dict=result)
        return result

    def _compute_shortest_paths(self, graph=None):
        g = graph if graph is not None else self._nxgraph
        if self._computation_choice == NX_COMPUTATION:
            return shortest_path(graph=g)
        elif self._computation_choice == PARALLEL_COMPUTATION:
            EfficientShortPathCalculator(nx_graph=g,
                                         n_threads=MAX_AVAILABLE).get_shortests_paths()

    def _return_result(self, obj_result, string_return, out_path):
        if out_path is not None:
            write_obj_to_json(target_obj=obj_result, out_path=out_path, indent=2)
        if string_return:
            return json_obj_to_string(target_obj=obj_result, indent=2)
        return obj_result
