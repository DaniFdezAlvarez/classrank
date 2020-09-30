import ijson
from classrank_io.graph.yielders.triples_yielder_interface import TriplesYielderInterface

class JsonWikidataDumpTriplesYielder(TriplesYielderInterface):

    def __init__(self, source_file):
        super(JsonWikidataDumpTriplesYielder, self).__init__()
        self._triple_count = 0
        self._error_count = 0
        self._ignored_count = 0
        self._source_file = source_file


    def yield_triples(self, max_triples=-1):
        self._reset_count()
        json_stream = open(self._source_file, "r")
        elem_id = None
        elem_type = None
        datatype = None
        datavalue_type = None
        current_claim_key = None
        datavalue_num_id = None
        possible_edges = []

        max_triples_reached = False

        for prefix, event, value in ijson.parse(json_stream):
            if max_triples_reached:
                break
            if event == 'end_map':
                if prefix == 'item':
                    for tuple_4 in possible_edges:
                        if self._is_valid_entity_edge(elem_type, tuple_4[0],
                                                      tuple_4[1]):  # triple: datatype, datavalue_type, datavalue_num_id
                            yield elem_id, tuple_4[2], 'Q' + tuple_4[3]
                            self._triple_count += 1
                            if self._triple_count == max_triples:
                                max_triples_reached = True
                                break
                            if self._triple_count % 100000 == 0:
                                print('parsed ' + str(self._triple_count))
                        else:
                            self._ignored_count += 1

                    elem_id = None
                    elem_type = None
                    current_claim_key = None
                    datavalue_num_id = None
                    datavalue_type = None
                    possible_edges = []
                elif prefix == "item.claims." + str(current_claim_key) + ".item":
                    possible_edges.append((datatype, datavalue_type, current_claim_key, str(datavalue_num_id)))

            elif event == 'string':
                if prefix == 'item.id':
                    elem_id = value
                elif prefix == 'item.type':
                    elem_type = value
                elif prefix == 'item.claims.' + str(current_claim_key) + '.item.mainsnak.datatype':
                    datatype = value
                elif prefix == 'item.claims.' + str(current_claim_key) + '.item.mainsnak.datavalue.value.entity-type':
                    datavalue_type = value
            elif event == 'map_key' and prefix == 'item.claims':
                current_claim_key = value
            elif event == 'number' and prefix == 'item.claims.' + str(
                    current_claim_key) + '.item.mainsnak.datavalue.value.numeric-id':
                datavalue_num_id = value

    @staticmethod
    def _is_valid_entity_edge(subj_type, data_nature, data_type):
        if subj_type == 'item' and data_nature == 'wikibase-item' and data_type == 'item':
            return True
        return False

    @property
    def yielded_triples(self):
        return self._triple_count

    @property
    def error_triples(self):
        return self._error_count

    @property
    def ignored_triples(self):
        return self._ignored_count

    def _reset_count(self):
        """
        Just to remember that the counts may be managed if the object is used to parse
        more than one time
        :return:
        """
        self._triple_count = 0
        self._error_count = 0
        self._ignored_count = 0

###############################################################

_MAP_KEY = "map_key"
_START_MAP = "start_map"
_END_MAP = "end_map"
_CLAIMS = "claims"
_END_ARRAY = "end_array"
_STRING = "string"
_DATATYPE = "datatype"
_WIKIBASE_ITEM = "wikibase-item"
_VALUE_ID = ".value.id"
_ITEM_DATAVALUE = ".item.datavalue"
_MAINSNAK = "mainsnak"
_ITEM_TITLE = "item.title"


class JsonWikidataDumpEntityTriplesYielder(TriplesYielderInterface):

    def __init__(self, source_file):
        super(JsonWikidataDumpEntityTriplesYielder, self).__init__()
        self._triple_count = 0
        self._error_count = 0
        self._ignored_count = 0
        self._source_file = source_file

        # tmp values

        self._current_entity = None
        self._current_prop = None
        self._current_objects = None
        self._looking_for_item = False
        self._statements_mode = False

    def yield_triples(self, max_triples=-1):
        self._reset_count()
        json_stream = open(self._source_file, "r")


        max_triples_reached = False

        for prefix, event, value in ijson.parse(json_stream):
            if max_triples_reached:
                break
            elif event == _START_MAP and prefix.endswith(_MAINSNAK):
                self._activate_statements_mode()

            elif event == _END_ARRAY and self._current_prop is not None and prefix.endswith(_CLAIMS + "." + self._current_prop):
                for a_triple in self._yield_current_triples():
                    yield a_triple
            elif event == _MAP_KEY and prefix.endswith(_CLAIMS):
                self._reset_current_prop(value)
            elif self._statements_mode:
                if event == _STRING:
                    if prefix.endswith(_DATATYPE) and value == _WIKIBASE_ITEM:
                        self._activate_looking_for_item_mode()
                    elif self._looking_for_item and prefix.endswith(_VALUE_ID):
                        self._store_object(value)
                elif self._looking_for_item and event == _END_MAP and prefix.endswith(self._current_prop + _ITEM_DATAVALUE):
                    self._deactivate_looking_for_item_mode()
                elif event == _END_MAP and prefix.endswith(_MAINSNAK):
                    self._deactivate_statements_mode()
            elif event == _STRING and prefix == _ITEM_TITLE:
                self._reset_current_entity(value)

    def _reset_current_entity(self, new_entity):
        self._current_entity = new_entity

    def _activate_statements_mode(self):
        self._statements_mode = True

    def _deactivate_statements_mode(self):
        self._statements_mode = False

    def _deactivate_looking_for_item_mode(self):
        self._looking_for_item = False

    def _store_object(self, an_obj):
        self._current_objects.append(an_obj)

    def _activate_looking_for_item_mode(self):
        self._looking_for_item = True

    def _reset_current_prop(self, new_prop):
        self._current_prop = new_prop
        self._current_objects = []

    def _yield_current_triples(self):
        for an_obj in self._current_objects:
            yield (self._current_entity, self._current_prop, an_obj)



    @staticmethod
    def _is_valid_entity_edge(subj_type, data_nature, data_type):
        if subj_type == 'item' and data_nature == 'wikibase-item' and data_type == 'item':
            return True
        return False

    @property
    def yielded_triples(self):
        return self._triple_count

    @property
    def error_triples(self):
        return self._error_count

    @property
    def ignored_triples(self):
        return self._ignored_count

    def _reset_count(self):
        """
        Just to remember that the counts may be managed if the object is used to parse
        more than one time
        :return:
        """
        self._triple_count = 0
        self._error_count = 0
        self._ignored_count = 0