from classrank_io.tsv_io import yield_tsv_lines
import urllib.parse
from experimentation.consts import REGEX_WHOLE_URI, REGEX_PREFIXED_URI, REGEX_TYPE_QUERY, re, MIN_LENGHT_PREFIX
from classrank_utils.uri import remove_corners
from classrank_io.json_io import write_obj_to_json
from experimentation.utils.query_mining_utils import parse_new_prefixes, replace_literal_spaces_with_blank, \
    detect_complete_uri_mentions, detect_prefixed_uri_mentions, detect_literal_spaces

KEY_ORGANIC_CLASS = "OC"
KEY_ORGANIC_INSTANCE = "OI"
KEY_ROBOTIC_CLASS = "RC"
KEY_ROBOTIC_INSTANCE = "RI"

KEY_ALL_MENTIONS = "all"
KEY_ROBOTIC = "R"
KEY_ORGANIC = "O"
KEY_RANK = "rank"
KEY_CLASS = "class"


SORT_BY_ORGANIC = "O"
SORT_BY_ROBOTIC = "R"
SORT_BY_ALL = "A"

_SEPARATOR = "\t"
_QUERY_POSITION = 0
_CATEGORY_POSITION = 2

_ORGANIC = "organic"  # todo : find organic label in the logs. or change to robotic.

_WIKIDATA_NAMESPACE_ENTITY = "http://www.wikidata.org/entity/"

class WikidataClassUsageMiner(object):

    def __init__(self, source_file, instances_dict, target_classes, wikidata_prefixes, error_entries_file, sort_by=SORT_BY_ALL):
        self._source_file = source_file
        self._instances_dict = instances_dict
        self._default_prefixes = wikidata_prefixes
        self._classes_dict = self._build_classes_dict(target_classes)
        self._sort_by = sort_by
        self._error_entries_file = error_entries_file

        self._valid_queries = 0
        self._total_queries = 0
        self._wrong_prefixed_uris = 0



    def _build_classes_dict(self, target_classes):
        result = {}
        for a_class in target_classes:
            result[a_class] = {
                KEY_ORGANIC_CLASS : 0,
                KEY_ORGANIC_INSTANCE : 0,
                KEY_ROBOTIC_CLASS : 0,
                KEY_ROBOTIC_INSTANCE : 0
            }
        return result

    def mine_log(self, dest_file):
        self._mine_lines()
        self._adapt_results()
        self._serialize_results(dest_file)
        self._liberate_results_memory()

    def _liberate_results_memory(self):
        # The big memory waste will be tipically the isntances dict. But does make sense to erase it, it wouldnt
        # allow several calls of mine_logs
        self._classes_dict = None

    def _serialize_results(self, dest_file):
        write_obj_to_json(target_obj=self._classes_dict,
                          out_path=dest_file)

    def _adapt_results(self):
        self._include_aggregated_fields()
        self._turn_dict_into_list()
        self._sort_results()
        self._update_ranking_field()

    def _turn_dict_into_list(self):
        self._classes_dict = [a_dict for a_dict in self._classes_dict.values()] # at this point, it is still a dict

    def _sort_results(self):
        self._classes_dict.sort(reverse=True,  # At this point, it is a list
                                key=self._get_lambda_to_sort())

    def _update_ranking_field(self):
        i = 1
        for a_class_dict in self._classes_dict:  # At this point, it is a list of dicts
            a_class_dict[KEY_RANK] = i
            i += 1

    def _get_lambda_to_sort(self):
        if self._sort_by == SORT_BY_ALL:
            return lambda x: x[KEY_ALL_MENTIONS]
        elif self._sort_by == SORT_BY_ORGANIC:
            return lambda x: x[KEY_ORGANIC]
        elif self._sort_by == SORT_BY_ROBOTIC:
            return lambda x: x[KEY_ROBOTIC]

    def _include_aggregated_fields(self):
        for a_class, a_class_dict in self._classes_dict.items():
            a_class_dict[KEY_ROBOTIC] = a_class_dict[KEY_ROBOTIC_CLASS] + a_class_dict[KEY_ROBOTIC_INSTANCE]
            a_class_dict[KEY_ORGANIC] = a_class_dict[KEY_ORGANIC_CLASS] + a_class_dict[KEY_ORGANIC_INSTANCE]
            a_class_dict[KEY_ALL_MENTIONS] = a_class_dict[KEY_ROBOTIC] + a_class_dict[KEY_ORGANIC]
            a_class_dict[KEY_CLASS] = a_class
            a_class_dict[KEY_RANK] = 0


    def _mine_lines(self):
        for a_line in yield_tsv_lines(self._source_file, skip_first=True):
            try:
                pieces = a_line.split("\t")
                uris_mentioned = self._get_uris_from_raw_query(pieces[_QUERY_POSITION])
                uris_mentioned = self._remove_wikidata_namespaces(uris_mentioned)
                self._annotate_mentions(uris_mentioned=uris_mentioned,
                                        organic=self._is_organic(pieces[_CATEGORY_POSITION]))
            except BaseException as e:
                self._log_error_entry(a_line, e)

    def _log_error_entry(self, entry, error):
        with open(self._error_entries_file, "a") as out_stream:
            out_stream.write(entry + "\n")
            out_stream.write(str(error) + "\t")


    def _remove_wikidata_namespaces(self, uris):
        result = []
        for an_uri in uris:
            if an_uri.startswith(_WIKIDATA_NAMESPACE_ENTITY):
                result.append(an_uri.replace(_WIKIDATA_NAMESPACE_ENTITY, ""))
            else:
                result.append(an_uri)
        return result


    def _annotate_mentions(self, uris_mentioned, organic):
        for an_uri in uris_mentioned:  # Can be both (instance and class), one or none
            if an_uri in self._classes_dict:
                self._annotate_class_mention(an_uri, organic)
            if an_uri in self._instances_dict:
                self._annotate_instance_mention(an_uri, organic)

    def _is_organic(self, category):
        return _ORGANIC == category

    def _annotate_class_mention(self, an_uri, organic):
        target_key = KEY_ORGANIC_CLASS if organic else KEY_ROBOTIC_CLASS
        self._classes_dict[an_uri][target_key] += 1

    def _annotate_instance_mention(self, an_uri, organic):
        target_key = KEY_ORGANIC_INSTANCE if organic else KEY_ROBOTIC_INSTANCE
        for a_class in self._instances_dict[an_uri]:
            self._classes_dict[a_class][target_key] += 1

    def _get_uris_from_raw_query(self, raw_query):
        norm_query = urllib.parse.unquote_plus(raw_query)
        prefixes, query = self._split_into_prefixes_and_query(norm_query)
        complete_uris, prefixed_uris = self._parse_uris(query)
        if len(prefixed_uris) > 0:
            new_prefixes_dict = {} if prefixes is None else parse_new_prefixes(prefixes)
            prefixed_uris = self._unprefixize_uris(uris=prefixed_uris,
                                                   new_prefixes=new_prefixes_dict)

        return set(complete_uris + prefixed_uris)  # PREFIXED HAVE BEEN UNPREFIXED AT THIS POINT IF THERE WERE ANY


    def _unprefixize_uris(self, uris, new_prefixes):
        return [self._unprefixize_uri(prefixed_uri=an_uri, new_prefixes=new_prefixes)
                for an_uri in uris
                if not an_uri.startswith("_:")]  # We are discarding here BNodes


    def _unprefixize_uri(self, prefixed_uri, new_prefixes):
        mid_index = prefixed_uri.find(":")
        target_prefix = prefixed_uri[:mid_index]
        if target_prefix in new_prefixes:
            return new_prefixes[target_prefix] + prefixed_uri[mid_index + 1:]
        if target_prefix in self._default_prefixes:
            return self._default_prefixes[target_prefix] + prefixed_uri[mid_index + 1:]
        self._increment_bad_prefixed_uris()
        raise ValueError("URIs with unknown prefixes are not supposed to be here: " + prefixed_uri)


    def _increment_bad_prefixed_uris(self):
        self._wrong_prefixed_uris += 1

    def _parse_uris(self, query):
        literal_spaces = detect_literal_spaces(query)
        if len(literal_spaces) != 0:
            query = replace_literal_spaces_with_blank(query=query,
                                                      literal_spaces=literal_spaces)
        return detect_complete_uri_mentions(query), detect_prefixed_uri_mentions(query)

    def _split_into_prefixes_and_query(self, raw_query):
        index_type_of_query = self._detect_index_type_of_query(raw_query)
        if index_type_of_query == -1:
            raise ValueError("Unknownk type of query")
        if index_type_of_query < MIN_LENGHT_PREFIX:
            return None, raw_query
        return raw_query[:index_type_of_query], raw_query[index_type_of_query:]

    def _detect_index_type_of_query(self, raw_query):
        res = re.search(REGEX_TYPE_QUERY, raw_query)
        # res = REGEX_TYPE_QUERY.search(raw_query)
        if res is None:
            print("----", raw_query)
            return -1

        else:
            return res.start()
