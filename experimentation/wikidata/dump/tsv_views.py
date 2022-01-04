def classes_file_to_list(source_file):
    with open(source_file, "r") as in_stream:
        result = []
        for a_line in in_stream:
            a_line = a_line.strip()
            if a_line != "":
                result.append(a_line)
        return result


def classes_file_to_set(source_file):
    return set(classes_file_to_list(source_file))
