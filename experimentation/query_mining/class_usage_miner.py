import re

_REGEX_PREFIX = re.compile("(PREFIX)|(prefix) +[\w\-]* *: *<.+>")

class ClassUsageMiner(object):

    def __init__(self, set_target_classes, namespaces=None, list_of_log_entries=None, entries_yielder_func=None):
        self._list_of_log_entries = list_of_log_entries
        self._external_yielder_func = entries_yielder_func
        self._entities_yielder_func = self._set_internal_yielder_func()
        self._classes_total_mentions = self._turn_set_of_classes_into_zeros_dict(set_target_classes)


        self._namespaces


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
            prefixes_dict = self._parse_new_prefixes(an_entry)
            uri_mentions = self._detect_class_mentions(an_entry)


    def _detect_uri_mentions(self, an_entry):
        return self._detect_complete_uri_mentions


    def _parse_new_prefixes(self, an_entry):
        pass # TODO





