from classrank_utils.uri import remove_corners
from experimentation.consts import REGEX_PREFIXED_URI, REGEX_TYPE_QUERY, REGEX_WHOLE_URI, re
from experimentation.utils.query_mining_utils import parse_new_prefixes, replace_literal_spaces_with_blank,\
    detect_literal_spaces, detect_complete_uri_mentions, detect_prefixed_uri_mentions

_DIRECT_MENTIONS = "d"
_INSTANCE_MENTIONS = "i"
_DOMRAN_MENTIONS = "DR"

_CLASS_DIRECT_MENTIONS = "T"
_CLASS_QUERY_MENTIONS = "Q"
_CLASS_INSTANCE_MENTIONS = "I"
_CLASS_DOMRAN_MENTIONS = "DR"

_HUMAN_KEY = "H"
_MACHINE_KEY = "M"
_UNKNOWN_KEY = "U"
"""
Some expected models:

dict_ips_machine_traffic --> {
"H": ["ip1", "ip2",...],
"U": ["ip1", "ip2",...],
"M": ["ip1", "ip2",...]
}


"""

class ClassUsageMiner(object):

    def __init__(self, set_target_classes, instance_tracker, domran_tracker=None, namespaces=None,
                 list_of_log_entries=None,entries_yielder_func=None, dict_ips_machine_traffic=None,
                 filter_machine_traffic=False):
        self._instance_tracker = instance_tracker
        self._domran_tracker = domran_tracker
        self._list_of_log_entries = list_of_log_entries
        self._external_yielder_func = entries_yielder_func
        self._filter_machine_traffic = filter_machine_traffic
        self._dict_ips_machine_traffic = self._adpat_dict_machine_traffic(dict_ips_machine_traffic)

        self._entities_yielder_func = self._set_internal_yielder_func()
        self._add_mentions_to_class_dicts = self._set_internal_annotation_func()

        self._classes_total_mentions = self._init_class_mentions_dict(set_target_classes=set_target_classes,
                                                                      filter_machine_traffic=filter_machine_traffic)

        # self._turn_set_of_classes_into_zeros_dict(set_target_classes)
        # self._classes_query_mentions = self._turn_set_of_classes_into_zeros_dict(set_target_classes)



        self._default_namespaces = namespaces

        self._queries_with_mentions = 0
        self._queries_without_mentions = 0
        self._bad_prefixed_uris = 0
        self._number_of_valid_queries = 0
        self._number_of_queries = 0
        self._wrong_uris_in_queries = 0
        self._wrong_entries = 0

        self._instances_dict = None  # Will be initialized later
        self._domran_dict = None # Will be initilized later. Same structure as instances_dict, but it contains
        # entities which are considered instances due to ontology domain/range inferences

    @property
    def wrong_uris_in_queries(self):
        return self._wrong_uris_in_queries

    @property
    def bad_prefixed_uris(self):
        return self._bad_prefixed_uris

    @property
    def wrong_entries(self):
        return self._wrong_entries

    @property
    def class_total_mentions(self):
        return self._classes_total_mentions

    @property
    def number_of_valid_queries(self):
        return self._number_of_valid_queries

    @property
    def number_of_queries(self):
        return self._number_of_queries


    def mine_entries(self):
        self._initialize_dicts()
        self._process_entries()

    def _initialize_dicts(self):
        self._initialize_instances_dict()
        self._initialize_domran_dict()

    def _process_entries(self):
        counter = 0
        for an_entry in self._entities_yielder_func():
            self._process_an_entry(an_entry)
            counter += 1
            if counter % 5000 == 0:
                print(counter)

    def _process_an_entry(self, an_entry):
        try:
            self._increment_queries()
            index_type_of_query = self._detect_index_type_of_query(an_entry)
            if index_type_of_query != -1:
                self._increment_valid_queries()
                new_prefixes_dict = parse_new_prefixes(an_entry.str_query[:index_type_of_query])
                query_without_prefixes = an_entry.str_query[index_type_of_query:]
                literal_spaces = detect_literal_spaces(query_without_prefixes)
                if len(literal_spaces) != 0:
                    query_without_prefixes = \
                        replace_literal_spaces_with_blank(query=query_without_prefixes,
                                                          literal_spaces=literal_spaces)
                uri_mentions = self._detect_uri_mentions(str_query=query_without_prefixes,
                                                         priority_namespaces=new_prefixes_dict)
                class_mention_dict = self._build_class_mention_dict_of_query(uri_mentions)
                self._add_mentions_to_class_dicts(class_mention_dict, an_entry)
        except BaseException as e:
            print(e)
            self._increment_wrong_entries()

    def _increment_queries(self):
        self._number_of_queries += 1

    def _increment_valid_queries(self):
        self._number_of_valid_queries += 1

    def _increment_wrong_entries(self):
        self._wrong_entries += 1

    def _adpat_dict_machine_traffic(self, dicts_ips_machine_traffic):
        result = {}
        for a_key, an_ip_list in dicts_ips_machine_traffic.items():
            for an_ip in an_ip_list:
                result[an_ip] = a_key
        return result

    def _init_class_mentions_dict(self, set_target_classes, filter_machine_traffic=False):
        result = {}
        if not filter_machine_traffic:
            for a_class in set_target_classes:
                result[a_class] = {_CLASS_QUERY_MENTIONS: 0,
                                   _CLASS_DIRECT_MENTIONS: 0,
                                   _CLASS_INSTANCE_MENTIONS: 0,
                                   _CLASS_DOMRAN_MENTIONS : 0}
        else:
            for a_class in set_target_classes:
                result[a_class] = {_MACHINE_KEY: {_CLASS_QUERY_MENTIONS: 0,
                                                  _CLASS_DIRECT_MENTIONS: 0,
                                                  _CLASS_INSTANCE_MENTIONS: 0,
                                                  _CLASS_DOMRAN_MENTIONS : 0},
                                   _HUMAN_KEY: {_CLASS_QUERY_MENTIONS: 0,
                                                _CLASS_DIRECT_MENTIONS: 0,
                                                _CLASS_INSTANCE_MENTIONS: 0,
                                                _CLASS_DOMRAN_MENTIONS : 0}
                    ,
                                   _UNKNOWN_KEY: {_CLASS_QUERY_MENTIONS: 0,
                                                _CLASS_DIRECT_MENTIONS: 0,
                                                _CLASS_INSTANCE_MENTIONS: 0,
                                                _CLASS_DOMRAN_MENTIONS: 0}
                                   }

        return result

    def _initialize_instances_dict(self):
        if self._instances_dict is None:
            self._instances_dict = self._instance_tracker.track_instances()
            # self._instances_dict = {}

    def _initialize_domran_dict(self):
        if self._domran_tracker is None:
            self._domran_dict = {}
            return
        if self._domran_dict is None:
            self._domran_dict = self._domran_tracker.track_domrans()

    def _turn_set_of_classes_into_zeros_dict(self, target_set):
        return {class_uri: 0 for class_uri in target_set}

    # def _turn_set_of_classes_into_zeros_dict(self, target_set):
    #     result = {}
    #     for elem in target_set:
    #         result[elem] = {}

    def _set_internal_yielder_func(self):
        if self._list_of_log_entries is not None:
            return self._yielder_func_on_list
        return self._external_yielder_func

    def _set_internal_annotation_func(self):
        if self._filter_machine_traffic:
            return self._add_mentions_to_human_or_machine_dicts
        return self._add_mentions_to_general_class_dicts

    def _yielder_func_on_list(self):
        for elem in self._list_of_log_entries:
            yield elem

    def _add_mentions_to_class_dicts(self, class_mention_dict, an_entry):
        pass  # TODO WILL BE OVERWRITTEN

    def _add_mentions_to_general_class_dicts(self, class_mention_dict, an_entry):
        if len(class_mention_dict) == 0:
            self._queries_without_mentions += 1
        else:
            self._queries_with_mentions += 1
            for a_class_key in class_mention_dict:
                if a_class_key in self._classes_total_mentions:
                    self._classes_total_mentions[a_class_key][_CLASS_DIRECT_MENTIONS] += \
                    class_mention_dict[a_class_key][_DIRECT_MENTIONS]
                    self._classes_total_mentions[a_class_key][_CLASS_QUERY_MENTIONS] += 1
                    self._classes_total_mentions[a_class_key][_CLASS_INSTANCE_MENTIONS] += \
                    class_mention_dict[a_class_key][_INSTANCE_MENTIONS]
                    self._classes_total_mentions[a_class_key][_CLASS_DOMRAN_MENTIONS] += \
                    class_mention_dict[a_class_key][_CLASS_DOMRAN_MENTIONS]

    def _add_mentions_to_human_or_machine_dicts(self, class_mention_dict, an_entry):
        if len(class_mention_dict) == 0:
            self._increment_queries_without_mentions()
        else:
            self._increment_queries_with_mentions()
            agent_key = self._decide_agent_key(an_entry)
            for a_class_key in class_mention_dict:
                if a_class_key in self._classes_total_mentions:
                    self._classes_total_mentions[a_class_key][agent_key][_CLASS_DIRECT_MENTIONS] += \
                        class_mention_dict[a_class_key][_DIRECT_MENTIONS]
                    self._classes_total_mentions[a_class_key][agent_key][_CLASS_QUERY_MENTIONS] += 1
                    self._classes_total_mentions[a_class_key][agent_key][_CLASS_INSTANCE_MENTIONS] += \
                        class_mention_dict[a_class_key][_INSTANCE_MENTIONS]
                    self._classes_total_mentions[a_class_key][agent_key][_CLASS_DOMRAN_MENTIONS] += \
                        class_mention_dict[a_class_key][_CLASS_DOMRAN_MENTIONS]

    def _increment_queries_with_mentions(self):
        self._queries_with_mentions += 1

    def _increment_queries_without_mentions(self):
        self._queries_without_mentions += 1

    def _decide_agent_key(self, an_entry):
        target_ip = an_entry.ip
        if target_ip in self._dict_ips_machine_traffic:
            return self._dict_ips_machine_traffic[target_ip]
        return _UNKNOWN_KEY
        # if an_entry.ip not in self._dict_ips_machine_traffic:
        #     return _HUMAN_KEY
        # if str(an_entry.hour) in self._dict_ips_machine_traffic[an_entry.ip]:
        #     return _MACHINE_KEY
        # return _HUMAN_KEY

    def _build_class_mention_dict_of_query(self, uri_mentions):
        result = {}
        for a_mention in uri_mentions:
            if a_mention in self._classes_total_mentions:
                if a_mention not in result:
                    result[a_mention] = self._empty_mention_query_dict()
                result[a_mention][_DIRECT_MENTIONS] += 1

            if a_mention in self._instances_dict:
                target_class_keys = self._instances_dict[a_mention]
                for a_target_class_key in target_class_keys:
                    if a_target_class_key not in result:
                        result[a_target_class_key] = self._empty_mention_query_dict()
                    result[a_target_class_key][_INSTANCE_MENTIONS] += 1
            if a_mention in self._domran_dict and a_mention not in self._instances_dict:
                target_class_keys = self._domran_dict[a_mention]
                for a_target_class_key in target_class_keys:
                    if a_target_class_key not in result:
                        result[a_target_class_key] = self._empty_mention_query_dict()
                    result[a_target_class_key][_DOMRAN_MENTIONS] += 1

        return result

    @staticmethod
    def _empty_mention_query_dict():
        return {_DIRECT_MENTIONS: 0,
                _INSTANCE_MENTIONS: 0,
                _DOMRAN_MENTIONS: 0}

    def _detect_index_type_of_query(self, an_entry):
        res = re.search(REGEX_TYPE_QUERY, an_entry.str_query)
        if res is None:
            print("----", an_entry.is_valid_query, an_entry.str_query)
            return -1

        else:
            # print("++++", an_entry.str_query)
            return res.start()
        # return -1 if res is None else res.start()

    def _detect_uri_mentions(self, str_query, priority_namespaces):
        return detect_complete_uri_mentions(str_query) + self._unprefix_uris(
            list_of_prefixed_uris=detect_prefixed_uri_mentions(str_query),
            priority_namespaces=priority_namespaces)

    def _unprefix_uris(self, list_of_prefixed_uris, priority_namespaces):
        result = []
        for an_uri in list_of_prefixed_uris:
            try:
                result.append(self._unprefix_uri(an_uri, priority_namespaces))
            except BaseException as e:

                print(e)
                self._increment_wrong_uris_in_queries()
        return result
        # return [self._unprefix_uri(an_uri, priority_namespaces) for an_uri in list_of_prefixed_uris]

    def _increment_wrong_uris_in_queries(self):
        self._wrong_uris_in_queries += 1

    def _unprefix_uri(self, prefixed_uri, priority_namespaces):
        mid_index = prefixed_uri.find(":")
        target_prefix = prefixed_uri[:mid_index]
        if target_prefix in priority_namespaces:
            return priority_namespaces[target_prefix] + prefixed_uri[mid_index + 1:]
        if target_prefix in self._default_namespaces:
            return self._default_namespaces[target_prefix] + prefixed_uri[mid_index + 1:]
        self._increment_bad_prefixed_uris()
        raise ValueError("URIs with unknown prefixes are not supposed to be computed in this method: " + prefixed_uri)


    def _increment_bad_prefixed_uris(self):
        self._bad_prefixed_uris += 1



