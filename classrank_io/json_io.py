import json

def write_obj_to_json(target_obj, out_path, indent=0):
    with open(out_path, "w") as out_stream:
        json.dump(target_obj, out_stream, indent=indent)

def json_obj_to_string(target_obj, indent=0):
    return json.dumps(target_obj, indent=indent)

def read_json_obj_from_path(target_path):
    with open(target_path, "r") as in_stream:
        return json.load(in_stream)

def json_obj_from_string(target_str):
    return json.loads(target_str)
