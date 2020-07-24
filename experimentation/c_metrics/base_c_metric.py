from classrank_io.json_io import json_obj_to_string, write_obj_to_json

class BaseCMetric(object):

    def _return_result(self, obj_result, string_return, out_path):
        if out_path is not None:
            write_obj_to_json(target_obj=obj_result, out_path=out_path, indent=2)
        if string_return:
            return json_obj_to_string(target_obj=obj_result, indent=2)
        return obj_result


    def _fill_absent_paths_with_an_all_nodes_walk(self, paths_dict, target_nodes, origin):
        """
        It expect a dict with this format:

        {'d': ['e', 'd'], 'b': ['e', 'b'], 'f': ['e', 'd', 'f'], 'e': ['e'], 'c': ['e', 'b', 'c']}

        key: destination_node from a given_source
        value: path from origin to reach the destination

        :param paths_dict:
        :param target_nodes: list of every node in the graph
        :param origin: node from which the path start
        :return:
        """
        infinity_path = [an_elem for an_elem in target_nodes]  # just a copy
        for a_node in target_nodes:
            if a_node != origin:
                if a_node not in paths_dict:
                    paths_dict[a_node] = infinity_path


    def _delete_auto_path(self, paths_dict, origin):
        """

        It expect a dict with this format:

        {'d': ['e', 'd'], 'b': ['e', 'b'], 'f': ['e', 'd', 'f'], 'e': ['e'], 'c': ['e', 'b', 'c']}

        key: destination_node from a given_source
        value: path from origin to reach the destination

        :param paths_dict:
        :param origin: node from which the path start
        :return:
        """
        if origin in paths_dict:
            del paths_dict[origin]

