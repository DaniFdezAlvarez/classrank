import re

# _REGEX_PREFIX = re.compile("(PREFIX)|(prefix) +[\w\-]* *: *<.+>")
_REGEX_PREFIX = re.compile("PREFIX", flags=re.IGNORECASE)

_REGEX_TYPE_QUERY = re.compile("(^|[ \n]+)((SELECT)|(ASK)|(CONSTRUCT)|(DESCRIBE)|(select)|(ask)|(construct)|(describe))[ \n]+")
_REGEX_WHOLE_URI = re.compile("<.+>")
_REGEX_PREFIXED_URI = re.compile("[ ,;\.\(\{\[\n\t][^<>\? ,;\.\(\{\[\n\t]*:[^<>\? ,;\.\)\}\]\n\t]*[ ,;\.\)\}\]\n\t]")

# ([^<>"{}|^`\]-[#x00-#x20])*

class ClassUsageMiner(object):

    def __init__(self, set_target_classes, namespaces=None, list_of_log_entries=None, entries_yielder_func=None):
        self._list_of_log_entries = list_of_log_entries
        self._external_yielder_func = entries_yielder_func
        self._entities_yielder_func = self._set_internal_yielder_func()

        self._classes_total_mentions = self._turn_set_of_classes_into_zeros_dict(set_target_classes)
        self._classes_query_mentions = self._turn_set_of_classes_into_zeros_dict(set_target_classes)

        self._default_namespaces = namespaces

        self._queries_with_mentions = 0
        self._queries_without_mentions = 0


    def _turn_set_of_classes_into_zeros_dict(self, target_set):
        return { class_uri : 0 for class_uri in target_set }


    def _set_internal_yielder_func(self):
        if self._list_of_log_entries is not None:
            return self._yielder_func_on_list
        return self._external_yielder_func

    def _yielder_func_on_list(self):
        for elem in self._list_of_log_entries:
            yield elem


    def _mine_entries(self):
        for an_entry in self._entities_yielder_func():
            index_type_of_query = self._detect_index_type_of_query(an_entry)
            if index_type_of_query != -1:
                new_prefixes_dict = self._parse_new_prefixes(an_entry.str_query[:index_type_of_query])
                uri_mentions = self._detect_uri_mentions(str_query=an_entry.str_query[:index_type_of_query],
                                                         priority_namespaces=new_prefixes_dict)
                class_mention_dict = self._build_class_mention_dict_of_query(uri_mentions)
                self._add_mentions_to_class_dicts(class_mention_dict)

    def _add_mentions_to_class_dicts(self, class_mention_dict):
        if len(class_mention_dict) == 0:
            self._queries_without_mentions += 1
        else:
            self._queries_with_mentions += 1
            for a_class_key in class_mention_dict:
                self._classes_query_mentions[a_class_key] += 1
                self._classes_total_mentions[a_class_key] += class_mention_dict[a_class_key]


    def _build_class_mention_dict_of_query(self, uri_mentions):
        result = {}
        for a_mention in uri_mentions:
            if a_mention in self._classes_total_mentions:
                if a_mention not in result:
                    result[a_mention] = 0
                result[a_mention] += 1
        return result


    def _detect_index_type_of_query(self, an_entry):
        res = re.search(_REGEX_TYPE_QUERY, an_entry.str_query)
        return -1 if res is None else res.start()


    def _detect_uri_mentions(self, str_query, priority_namespaces):
        return self._detect_complete_uri_mentions(str_query) + self._unprefix_uris(list_of_prefixed_uris=self._dectect_prefixed_uri_mentions(str_query),
                                                                                   priority_namespaces=priority_namespaces)

    def _unprefix_uris(self, list_of_prefixed_uris, priority_namespaces):
        return [self._unprefix_uri(an_uri, priority_namespaces) for an_uri in list_of_prefixed_uris]

    def _unprefix_uri(self, prefixed_uri, priority_namespaces):
        mid_index = prefixed_uri.find(":")
        target_prefix = prefixed_uri[:mid_index]
        if target_prefix in priority_namespaces:
            return priority_namespaces[target_prefix] + prefixed_uri[mid_index+1:]
        if target_prefix in self._default_namespaces:
            return self._default_namespaces[target_prefix] + prefixed_uri[mid_index+1:]
        raise ValueError("URIs with unknown prefixes are not supposed to be computed in this method")

    def _detect_complete_uri_mentions(self, str_query):
        return re.findall(_REGEX_WHOLE_URI, str_query)

    def _dectect_prefixed_uri_mentions(self, str_query):
        matches = re.findall(_REGEX_PREFIXED_URI, str_query)
        return [match[1:-1] for match in matches]


    def _parse_new_prefixes(self, str_prefixes_list):
        if len(str_prefixes_list) < 11:  # len("prefix : <>")
            return {}
        pieces = re.split(_REGEX_PREFIX, str_prefixes_list)
        if len(pieces) < 2:  # The first piece does not contain a nampespace, it is an (probably empty string) prior to the first PREFIX keyword
            return {}
        result = {}
        for a_piece in pieces:
            index_end_prefix = a_piece.find(":")  # First ':' will be the ':' used after the prefix
            prefix = a_piece[:index_end_prefix].strip()

            index_beg_uri = a_piece.find("<") + 1
            index_end_uri = a_piece.find(">")

            result[prefix] = a_piece[index_beg_uri:index_end_uri]
        return result








