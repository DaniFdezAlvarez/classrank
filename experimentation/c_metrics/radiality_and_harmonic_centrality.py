from experimentation.c_metrics.base_c_metric import BaseCMetric
from classrank_utils.g_paths import nx_diameter, shortest_path, fill_absent_paths_with_an_all_nodes_walk, delete_auto_path


class RadialityAndHarmonicCentrality(BaseCMetric):

    def __init__(self, nxgraph):
        super().__init__()
        self._nxgraph = nxgraph
        self._infinite_walk = self._create_infinite_walk()
        self._harmonic_dict = {}
        self._radiality_dict = {}


    def run(self):
        diameter = nx_diameter(self._nxgraph)
        for a_node in self._nxgraph.nodes:
            # Radiality
            paths = shortest_path(graph=self._nxgraph,
                                  origin=a_node)
            self._fill_absent_paths_with_an_all_nodes_walk(paths_dict=paths,
                                                           origin=a_node)
            self._delete_auto_paths(paths_dict=paths,
                                    origin=a_node)

            denominator_rad = sum([diameter - (float(1) / len(paths[a_path_key])) for a_path_key in paths])
            denominator_harm = sum([len(paths[a_path_key]) for a_path_key in paths])

            self._harmonic_dict[a_node] = float(1) / denominator_harm
            self._radiality_dict[a_node] = float(1) / denominator_rad

            # TODO normalize


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
