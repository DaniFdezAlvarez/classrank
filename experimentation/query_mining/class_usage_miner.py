import re
from classrank_utils.uri import remove_corners

# _REGEX_PREFIX = re.compile("(PREFIX)|(prefix) +[\w\-]* *: *<.+>")
_REGEX_PREFIX = re.compile("PREFIX", flags=re.IGNORECASE)

_REGEX_TYPE_QUERY = re.compile(
    "(^|[\s>])((SELECT)|(ASK)|(CONSTRUCT)|(DESCRIBE))[\*\s\{]", flags=re.IGNORECASE)
_REGEX_WHOLE_URI = re.compile("<[^ ]+>")
_REGEX_PREFIXED_URI = re.compile("[ ,;\.\(\{\[\n\t][^<>\? ,;\.\(\{\[\n\t/\^]*:[^<>\? ,;\.\)\}\]\n\t]*[ ,;\.\)\}\]\n\t]")

_DIRECT_MENTIONS = "d"
_INSTANCE_MENTIONS = "i"

_CLASS_DIRECT_MENTIONS = "T"
_CLASS_QUERY_MENTIONS = "Q"
_CLASS_INSTANCE_MENTIONS = "I"

_HUMAN_KEY = "H"
_MACHINE_KEY = "M"


# ([^<>"{}|^`\]-[#x00-#x20])*

class ClassUsageMiner(object):

    def __init__(self, set_target_classes, instance_tracker, namespaces=None, list_of_log_entries=None,
                 entries_yielder_func=None, dict_ips_machine_traffic=None, filter_machine_traffic=False):
        self._instance_tracker = instance_tracker
        self._list_of_log_entries = list_of_log_entries
        self._external_yielder_func = entries_yielder_func
        self._filter_machine_traffic = filter_machine_traffic
        self._dict_ips_machine_traffic = dict_ips_machine_traffic

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
        self._initialize_instances_dict()
        print("Dict Done!")
        counter = 0
        for an_entry in self._entities_yielder_func():
            try:
                self._number_of_queries += 1
                index_type_of_query = self._detect_index_type_of_query(an_entry)
                if index_type_of_query != -1:
                    self._number_of_valid_queries += 1
                    new_prefixes_dict = self._parse_new_prefixes(an_entry.str_query[:index_type_of_query])
                    query_without_prefixes = an_entry.str_query[index_type_of_query:]
                    literal_spaces = self._detect_literal_spaces(query_without_prefixes)
                    # tunned_query = self._replace_literal_spaces_with_blank(query_without_prefixes, literal_spaces)
                    if len(literal_spaces) != 0:
                        query_without_prefixes = \
                            self._replace_literal_spaces_with_blank(query_without_prefixes=query_without_prefixes,
                                                                    literal_spaces=literal_spaces)
                    uri_mentions = self._detect_uri_mentions(str_query=query_without_prefixes,
                                                             priority_namespaces=new_prefixes_dict)
                    class_mention_dict = self._build_class_mention_dict_of_query(uri_mentions)
                    self._add_mentions_to_class_dicts(class_mention_dict, an_entry)
                    counter += 1
                    if counter % 1000 == 0:
                        print(counter)
            except BaseException as e:
                print(e)
                self._wrong_entries += 1

    def _init_class_mentions_dict(self, set_target_classes, filter_machine_traffic=False):
        result = {}
        if not filter_machine_traffic:
            for a_class in set_target_classes:
                result[a_class] = {_CLASS_QUERY_MENTIONS: 0,
                                   _CLASS_DIRECT_MENTIONS: 0,
                                   _CLASS_INSTANCE_MENTIONS: 0}
        else:
            for a_class in set_target_classes:
                result[a_class] = {_MACHINE_KEY: {_CLASS_QUERY_MENTIONS: 0,
                                                  _CLASS_DIRECT_MENTIONS: 0,
                                                  _CLASS_INSTANCE_MENTIONS: 0},
                                   _HUMAN_KEY: {_CLASS_QUERY_MENTIONS: 0,
                                                _CLASS_DIRECT_MENTIONS: 0,
                                                _CLASS_INSTANCE_MENTIONS: 0}}

        return result

    def _initialize_instances_dict(self):
        if self._instances_dict is None:
            self._instances_dict = self._instance_tracker.track_instances()
            # self._instances_dict = {}

    def _replace_literal_spaces_with_blank(self, query_without_prefixes, literal_spaces):
        result = query_without_prefixes
        for a_space_tuple in reversed(literal_spaces):
            result = result[:a_space_tuple[0]] + " " + result[a_space_tuple[1] + 1:]
        return result

    def _detect_literal_spaces(self, str_query):
        indexes = []
        index = 0
        for char in str_query:
            if char == '"':
                if index == 0:
                    indexes.append(index)
                elif str_query[index - 1] != '\\':
                    indexes.append(index)
            index += 1
        if len(indexes) % 2 != 0:
            raise ValueError("The query has an odd number of non-scaped quotes: " + str_query)
        if len(indexes) == 0:
            return []
        result = []
        i = 0
        while i < len(indexes):
            result.append((indexes[i], indexes[i + 1]))
            i += 2
        return result

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

    def _add_mentions_to_human_or_machine_dicts(self, class_mention_dict, an_entry):
        if len(class_mention_dict) == 0:
            self._queries_without_mentions += 1
        else:
            self._queries_with_mentions += 1
            agent_key = self._decide_agent_key(an_entry)
            for a_class_key in class_mention_dict:
                if a_class_key in self._classes_total_mentions:
                    self._classes_total_mentions[a_class_key][agent_key][_CLASS_DIRECT_MENTIONS] += \
                        class_mention_dict[a_class_key][_DIRECT_MENTIONS]
                    self._classes_total_mentions[a_class_key][agent_key][_CLASS_QUERY_MENTIONS] += 1
                    self._classes_total_mentions[a_class_key][agent_key][_CLASS_INSTANCE_MENTIONS] += \
                        class_mention_dict[a_class_key][_INSTANCE_MENTIONS]

    def _decide_agent_key(self, an_entry):
        if an_entry.ip not in self._dict_ips_machine_traffic:
            return _HUMAN_KEY
        if str(an_entry.hour) in self._dict_ips_machine_traffic[an_entry.ip]:
            return _MACHINE_KEY
        return _HUMAN_KEY

    def _build_class_mention_dict_of_query(self, uri_mentions):
        result = {}
        for a_mention in uri_mentions:
            if a_mention in self._classes_total_mentions:
                if a_mention not in result:
                    result[a_mention] = {_DIRECT_MENTIONS: 0,
                                         _INSTANCE_MENTIONS: 0}
                result[a_mention][_DIRECT_MENTIONS] += 1

            if a_mention in self._instances_dict:
                target_class_keys = self._instances_dict[a_mention]
                for a_target_class_key in target_class_keys:
                    if a_target_class_key not in result:
                        result[a_target_class_key] = {_DIRECT_MENTIONS: 0,
                                                      _INSTANCE_MENTIONS: 0}
                    result[a_target_class_key][_INSTANCE_MENTIONS] += 1
        return result

    def _detect_index_type_of_query(self, an_entry):
        res = re.search(_REGEX_TYPE_QUERY, an_entry.str_query)
        if res is None:
            print("----", an_entry.is_valid_query, an_entry.str_query)
            return -1

        else:
            # print("++++", an_entry.str_query)
            return res.start()
        # return -1 if res is None else res.start()

    def _detect_uri_mentions(self, str_query, priority_namespaces):
        return self._detect_complete_uri_mentions(str_query) + self._unprefix_uris(
            list_of_prefixed_uris=self._dectect_prefixed_uri_mentions(str_query),
            priority_namespaces=priority_namespaces)

    def _unprefix_uris(self, list_of_prefixed_uris, priority_namespaces):
        result = []
        for an_uri in list_of_prefixed_uris:
            try:
                result.append(self._unprefix_uri(an_uri, priority_namespaces))
            except BaseException as e:

                print(e)
                self._wrong_uris_in_queries += 1
        return result
        # return [self._unprefix_uri(an_uri, priority_namespaces) for an_uri in list_of_prefixed_uris]

    def _unprefix_uri(self, prefixed_uri, priority_namespaces):
        mid_index = prefixed_uri.find(":")
        target_prefix = prefixed_uri[:mid_index]
        if target_prefix in priority_namespaces:
            return priority_namespaces[target_prefix] + prefixed_uri[mid_index + 1:]
        if target_prefix in self._default_namespaces:
            return self._default_namespaces[target_prefix] + prefixed_uri[mid_index + 1:]
        self._bad_prefixed_uris += 1
        raise ValueError("URIs with unknown prefixes are not supposed to be computed in this method: " + prefixed_uri)

    def _detect_complete_uri_mentions(self, str_query):
        return [remove_corners(a_uri) for a_uri in re.findall(_REGEX_WHOLE_URI, str_query)]

    def _dectect_prefixed_uri_mentions(self, str_query):
        matches = re.findall(_REGEX_PREFIXED_URI, str_query)
        return [match[1:-1] for match in matches]

    def _parse_new_prefixes(self, str_prefixes_list):
        if len(str_prefixes_list) < 11:  # len("prefix : <>")
            return {}
        pieces = re.split(_REGEX_PREFIX, str_prefixes_list)
        if len(
                pieces) < 2:  # The first piece does not contain a nampespace, it is an (probably empty string) prior to the first PREFIX keyword
            return {}
        result = {}
        for a_piece in pieces:
            index_end_prefix = a_piece.find(":")  # First ':' will be the ':' used after the prefix
            prefix = a_piece[:index_end_prefix].strip()

            index_beg_uri = a_piece.find("<") + 1
            index_end_uri = a_piece.find(">")

            result[prefix] = a_piece[index_beg_uri:index_end_uri]
        return result
