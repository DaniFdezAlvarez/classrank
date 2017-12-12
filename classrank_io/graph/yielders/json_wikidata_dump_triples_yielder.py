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
                                print 'parsed ' + str(self._triple_count)
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