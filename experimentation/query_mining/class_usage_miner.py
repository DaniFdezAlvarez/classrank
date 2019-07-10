import re

# _REGEX_PREFIX = re.compile("(PREFIX)|(prefix) +[\w\-]* *: *<.+>")
_REGEX_PREFIX = re.compile("PREFIX", flags=re.IGNORECASE)

_REGEX_TYPE_QUERY = re.compile("(^|[ \n]+)((SELECT)|(ASK)|(CONSTRUCT)|(DESCRIBE)|(select)|(ask)|(construct)|(describe))[ \n]+")

class ClassUsageMiner(object):

    def __init__(self, set_target_classes, namespaces=None, list_of_log_entries=None, entries_yielder_func=None):
        self._list_of_log_entries = list_of_log_entries
        self._external_yielder_func = entries_yielder_func
        self._entities_yielder_func = self._set_internal_yielder_func()
        self._classes_total_mentions = self._turn_set_of_classes_into_zeros_dict(set_target_classes)

        self._default_namespaces = namespaces


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
                uri_mentions = self._detect_uri_mentions(an_entry.str_query[:index_type_of_query])


    def _detect_index_type_of_query(self, an_entry):
        res = re.search(_REGEX_TYPE_QUERY, an_entry.str_query)
        return -1 if res is None else res.start()


    def _detect_uri_mentions(self, str_query):
        return self._detect_complete_uri_mentions() + self._dectect_prefixed_uri_mentions()

    def _detect_complete_uri_mentions(self):
        pass  # TODO

    def _dectect_prefixed_uri_mentions(self):
        pass  # TODO


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








