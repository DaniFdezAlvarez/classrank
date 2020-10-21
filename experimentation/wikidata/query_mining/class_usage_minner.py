from classrank_io.tsv_io import yield_tsv_lines

KEY_ORGANIC_CLASS = "OC"
KEY_ORGANIC_INSTANCE = "OI"
KEY_ROBOTIC_CLASS = "RC"
KEY_ROBOTIC_INSTANCE = "RI"

_SEPARATOR = "\t"
_QUERY_POSITION = 0
_CATEGORY_POSITION = 2

_ORGANIC = ""  # todo : find organic label in the logs. or change to robotic.

class WikidataClassUsageMiner(object):

    def __init__(self, source_file, instances_dict, target_clases, wikidata_prefixes):
        self._source_file = source_file
        self._instances_dict = instances_dict
        self._default_prefixes = wikidata_prefixes
        self._classes_dict = self._build_classes_dict(target_clases)



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

    def mine_log(self):
        self._mine_lines()
        self._adapt_results()
        return self._produce_results()


    def _mine_lines(self):
        for a_line in yield_tsv_lines(self._source_file):
            pieces = a_line.split("\t")
            uris_mentioned = self._get_uris_from_raw_query(pieces[_QUERY_POSITION])
            self._annotate_mentions(uris_mentioned=uris_mentioned,
                                    organic=self._is_organic(pieces[_CATEGORY_POSITION]))

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
        self._classes_dict[self._instances_dict[an_uri]][target_key] += 1

    def _get_uris_from_raw_query(self, raw_query):
        # SELECT+*%0AWHERE+%7B%0A++%3Fvar1++%3Chttp%3A%2F%2Fwww.wikidata.org%2Fprop%2Fdirect%2FP698%3E++%2229066813%22.%0A%7D%0A
        #
        # TURNS INTO
        #
        # SELECT+*
        # WHERE+{
        # ++?var1++<http://www.wikidata.org/prop/direct/P698>++"29066813".
        # }

        # TODO: URL_decode + substitute '+' by whites
        # Then reuse DBPedia's regex to detect prefixed and unprefixed URIS
        pass  # TODO: DECODE, MINE MENTIONES, UNPREFIX. Return absolute URIs



