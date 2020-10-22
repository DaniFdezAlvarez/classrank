from classrank_io.tsv_io import yield_tsv_lines
import urllib.parse
from experimentation.consts import REGEX_WHOLE_URI, REGEX_PREFIXED_URI, REGEX_PREFIX, REGEX_TYPE_QUERY, re, MIN_LENGHT_PREFIX
from classrank_utils.uri import remove_corners
from classrank_io.json_io import write_obj_to_json

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

    def __init__(self, source_file, instances_dict, target_classes, wikidata_prefixes, sort_by=SORT_BY_ALL):
        self._source_file = source_file
        self._instances_dict = instances_dict
        self._default_prefixes = wikidata_prefixes
        self._classes_dict = self._build_classes_dict(target_classes)
        self._sort_by = sort_by

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

    def _turn_dict_into_list(self):
        self._classes_dict = [a_dict for a_dict in self._classes_dict.values()] # at this point, it is still a dict

    def _sort_results(self):
        self._classes_dict.sort(reverse=True,  # At this point, it is a list
                                key=self._get_lambda_to_sort())

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
        line_count = 0  #########
        for a_line in yield_tsv_lines(self._source_file, skip_first=True):
            pieces = a_line.split("\t")
            uris_mentioned = self._get_uris_from_raw_query(pieces[_QUERY_POSITION])
            uris_mentioned = self._remove_wikidata_namespaces(uris_mentioned)
            self._annotate_mentions(uris_mentioned=uris_mentioned,
                                    organic=self._is_organic(pieces[_CATEGORY_POSITION]))
            line_count += 1 #########
            if line_count >= 10: #########
                break  #########


    def _remove_wikidata_namespaces(self, uris):
        result = []
        for an_uri in uris:
            if an_uri.startswith(_WIKIDATA_NAMESPACE_ENTITY):
                result.append(an_uri.replace(_WIKIDATA_NAMESPACE_ENTITY,""))
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
            new_prefixes_dict = {} if prefixes is None else self._parse_new_prefixes(prefixes)
            prefixed_uris = self._unprefixize_uris(uris=prefixed_uris,
                                                   new_prefixes=new_prefixes_dict)

        return set(complete_uris + prefixed_uris)  # PREFIXED HAVE BEEN UNPREFIXED AT THIS POINT IF THERE WERE ANY


    def _unprefixize_uris(self, uris, new_prefixes):
        return [self._unprefixize_uri(prefixed_uri=an_uri, new_prefixes=new_prefixes) for an_uri in uris]


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


    def _parse_new_prefixes(self, str_prefixes_list):  # TODO REFACTOR
        pieces = re.split(REGEX_PREFIX, str_prefixes_list)
        if len(pieces) < 2:  # The first piece does not contain a nampespace, thats before the first PREFIX keyword
            return {}
        result = {}
        for a_piece in pieces:
            index_end_prefix = a_piece.find(":")  # First ':' will be the ':' used after the prefix
            prefix = a_piece[:index_end_prefix].strip()

            index_beg_uri = a_piece.find("<") + 1
            index_end_uri = a_piece.find(">")

            result[prefix] = a_piece[index_beg_uri:index_end_uri]
        return result

    def _parse_uris(self, query):
        literal_spaces = self._detect_literal_spaces(query)
        if len(literal_spaces) != 0:
            query = self._replace_literal_spaces_with_blank(query=query,
                                                            literal_spaces=literal_spaces)
        return self._detect_complete_uri_mentions(query), self._detect_prefixed_uri_mentions(query)

    def _replace_literal_spaces_with_blank(self, query, literal_spaces):  # TODO REFACTOR
        result = query
        for a_space_tuple in reversed(literal_spaces):
            result = result[:a_space_tuple[0]] + " " + result[a_space_tuple[1] + 1:]
        return result

    def _detect_complete_uri_mentions(self, query):  # TODO REFACTOR
        return [remove_corners(a_uri) for a_uri in re.findall(REGEX_WHOLE_URI, query)]

    def _detect_prefixed_uri_mentions(self, query):  # TODO REFACTOR
        return [match[1:-1] for match in re.findall(REGEX_PREFIXED_URI, query)]

    def _detect_literal_spaces(self, str_query):  # TODO REFACTOR
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
