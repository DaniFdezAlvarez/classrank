from experimentation.dbpedia.query_mining import ClassUsageMiner
from classrank_io.json_io import write_obj_to_json

_RESULTS_KEY = "results"


class ClassUsageMinerMultiLog(ClassUsageMiner):

    def __init__(self, set_target_classes, instance_tracker, list_of_entry_yielders, domran_tracker=None,
                 namespaces=None, dict_ips_machine_traffic=None, filter_machine_traffic=False,
                 serialize_final_results=True,
                 serialize_finished_partials=True, base_path_for_finished_partials=None):
        self._list_of_entry_yielders = list_of_entry_yielders
        self._yielder_count = 0
        self._serialize_finished_partials = serialize_finished_partials
        self._serialize_final_results = serialize_final_results
        self._base_path_for_finished_partials = base_path_for_finished_partials

        self._set_target_classes = set_target_classes

        self._dict_of_partial_results = {}

        super().__init__(set_target_classes=set_target_classes,
                         instance_tracker=instance_tracker,
                         domran_tracker=domran_tracker,
                         namespaces=namespaces,
                         list_of_log_entries=None,
                         entries_yielder_func=None,
                         dict_ips_machine_traffic=dict_ips_machine_traffic,
                         filter_machine_traffic=filter_machine_traffic)
        # _classes_total_mentions will act as a partial results.
        #  Accumulated values will be acumulated in accumulated_classes_total_mentions
        self._accumulated_classes_total_mentions = self._init_class_mentions_dict(set_target_classes=set_target_classes,
                                                                                  filter_machine_traffic=filter_machine_traffic)

        self._accumulated_queries_with_mentions = 0
        self._accumulated_queries_without_mentions = 0
        self._accumulated_bad_prefixed_uris = 0
        self._accumulated_number_of_valid_queries = 0
        self._accumulated_number_of_queries = 0
        self._accumulated_wrong_uris_in_queries = 0
        self._accumulated_wrong_entries = 0

    def _increment_queries(self):
        self._number_of_queries += 1
        self._accumulated_number_of_queries += 1

    def _increment_valid_queries(self):
        self._number_of_valid_queries += 1
        self._accumulated_number_of_valid_queries += 1

    def _increment_wrong_entries(self):
        self._wrong_entries += 1
        self._accumulated_wrong_entries += 1

    def _increment_queries_with_mentions(self):
        self._queries_with_mentions += 1
        self._accumulated_queries_with_mentions += 1

    def _increment_queries_without_mentions(self):
        self._queries_without_mentions += 1
        self._accumulated_queries_without_mentions += 1

    def _increment_wrong_uris_in_queries(self):
        self._wrong_uris_in_queries += 1
        self._accumulated_wrong_uris_in_queries += 1

    def _increment_bad_prefixed_uris(self):
        self._bad_prefixed_uris += 1
        self._accumulated_bad_prefixed_uris += 1

    @property
    def wrong_uris_in_queries(self):
        return self._accumulated_wrong_uris_in_queries

    @property
    def bad_prefixed_uris(self):
        return self._accumulated_bad_prefixed_uris

    @property
    def wrong_entries(self):
        return self._accumulated_wrong_entries

    @property
    def class_total_mentions(self):
        return self._accumulated_classes_total_mentions

    @property
    def number_of_valid_queries(self):
        return self._accumulated_number_of_valid_queries

    @property
    def number_of_queries(self):
        return self._accumulated_number_of_queries

    def _set_internal_yielder_func(self):
        return None  # It wont be used in this miner

    def _process_entries(self):
        for a_yielder in self._list_of_entry_yielders:
            self._change_yielder()
            counter = 0
            for an_entry in a_yielder.yield_entries():
                self._process_an_entry(an_entry)
                counter += 1
                if counter % 1000 == 0:
                    print(counter)
        if self._serialize_final_results:
            self._serialize_accumulated_data()

    def _change_yielder(self):
        if self._yielder_count > 0:
            self._manage_current_partial_results()
        self._yielder_count += 1
        self._reset_yielder_stats()

    def _manage_current_partial_results(self):
        self._dict_of_partial_results[self._yielder_count] = {
            "queries_with_mentions": self._queries_with_mentions,
            "queries_without_mentions": self._queries_without_mentions,
            "bad_prefixed_uris": self._bad_prefixed_uris,
            "number_of_valid_queries": self._number_of_valid_queries,
            "number_of_queries": self._number_of_queries,
            "wrong_uris_in_queries": self._wrong_uris_in_queries,
            "wrong_entries": self._wrong_entries,
            _RESULTS_KEY: self._classes_total_mentions
        }

        if self._serialize_finished_partials:
            self._serialize_current_yielder_results()

    def _serialize_accumulated_data(self):
        class_mention_path = self._get_accumulated_class_mention_path_to_serialize()
        write_obj_to_json(target_obj=self._accumulated_classes_total_mentions,
                          out_path=class_mention_path,
                          indent=2)
        stats_path = self._get_accumulated_stats_path_to_serialize()
        stats_dict = {"queries_with_mentions": self._accumulated_queries_with_mentions,
                      "queries_without_mentions": self._accumulated_queries_without_mentions,
                      "bad_prefixed_uris": self._accumulated_bad_prefixed_uris,
                      "number_of_valid_queries": self._accumulated_number_of_valid_queries,
                      "number_of_queries": self._accumulated_number_of_queries,
                      "wrong_uris_in_queries": self._accumulated_wrong_uris_in_queries,
                      "wrong_entries": self._accumulated_wrong_entries}
        write_obj_to_json(target_obj=stats_dict,
                          out_path=stats_path,
                          indent=2)

    def _get_accumulated_class_mention_path_to_serialize(self):
        return self._base_path_for_finished_partials + "_classes_total.json"

    def _get_accumulated_stats_path_to_serialize(self):
        return self._base_path_for_finished_partials + "_stats_total.json"

    def _serialize_current_yielder_results(self):
        class_mention_path = self._get_current_class_mention_path_to_serialize()
        write_obj_to_json(target_obj=self._dict_of_partial_results[self._yielder_count][_RESULTS_KEY],
                          out_path=class_mention_path,
                          indent=2)

        stast_path = self._get_current_stats_path_to_serialize()
        stats_summary_as_json = self._get_current_stats_as_json_dict()
        write_obj_to_json(target_obj=stats_summary_as_json,
                          out_path=stast_path,
                          indent=2)

    def _get_current_class_mention_path_to_serialize(self):
        return self._base_path_for_finished_partials + "_classes_" + str(self._yielder_count) + ".json"

    def _get_current_stats_path_to_serialize(self):
        return self._base_path_for_finished_partials + "_stats_" + str(self._yielder_count) + ".json"

    def _get_current_stats_as_json_dict(self):
        result = {}
        for a_key in self._dict_of_partial_results[self._yielder_count]:
            if a_key != _RESULTS_KEY:
                result[a_key] = self._dict_of_partial_results[self._yielder_count][a_key]
        return result

    def _reset_yielder_stats(self):
        self._queries_with_mentions = 0
        self._queries_without_mentions = 0
        self._bad_prefixed_uris = 0
        self._number_of_valid_queries = 0
        self._number_of_queries = 0
        self._wrong_uris_in_queries = 0
        self._wrong_entries = 0

        self._classes_total_mentions = self._init_class_mentions_dict(set_target_classes=self._set_target_classes,
                                                                      filter_machine_traffic=self._filter_machine_traffic)
