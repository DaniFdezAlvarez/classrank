from classrank_io.json_io import json_obj_from_string, write_obj_to_json

_ENTRY_ID_KEY = "id"
_LABELS_ID_KEY = "labels"
_LABEL_VALUE_ID_KEY = "value"

class WikidataLabelCollector(object):

    def __init__(self, dump_file, target_entities, out_file, target_language="en"):
        self._dump_file = dump_file
        self._target_entities = set(target_entities) if type(target_entities) != set else target_entities
        self._target_language = target_language
        self._out_file = out_file
        self._labels_dict = {}


    def collect_labels(self):
        self._parse_target_labels()
        self._serialize_target_labels()

    def _parse_target_labels(self):
        for a_json_entry in self._yield_json_entries():
            qid = a_json_entry[_ENTRY_ID_KEY]
            if qid in self._target_entities:
                self._annotate_label(qid=qid,
                                     label=self._entry_label(a_json_entry))

    def _serialize_target_labels(self):
        write_obj_to_json(target_obj=self._labels_dict,
                          out_path=self._out_file)

    def _yield_json_entries(self):
        with open(self._dump_file, "r") as in_stream:
            for a_line in in_stream:
                a_line = a_line.strip()
                content = a_line[:-1] if a_line.endswith(",") else a_line
                try:
                    yield json_obj_from_string(content)
                except:
                    print("Line with error: " + content)

    def _entry_label(self, json_entry):
        labels_dict = json_entry[_LABELS_ID_KEY]
        if self._target_language in labels_dict:  # target language found
            return labels_dict[self._target_language][_LABEL_VALUE_ID_KEY]
        if len(labels_dict) == 0:  # No label at all
            return ""
        else:  # No target language, but some label found
            for a_key_language in labels_dict.keys():  # NOT A FOR, JUST A O(1) acces to a random (the first) key
                return labels_dict[a_key_language][_LABEL_VALUE_ID_KEY] + "(" + a_key_language + ")"
            
    def _annotate_label(self, qid, label):
        self._labels_dict[qid] = label




