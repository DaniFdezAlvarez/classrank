def load_data_list(target_path):
    result = []
    with open(target_path, "r") as in_stream:
        in_stream.readline()
        for a_line in in_stream:
            result.append(a_line.strip().split("\t"))
    return result