from wikidata.client import Client

_client = Client()


def label_of_property(prop):
    try:
        return _client.get(entity_id=prop, load=True).label
    except:
        return None


def label_of_properties(list_of_props):
    return {an_str_prop: label_of_property(an_str_prop) for an_str_prop in list_of_props}
