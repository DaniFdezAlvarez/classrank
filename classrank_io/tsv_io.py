def yield_tsv_lines(file_path, skip_first=False):
    with open(file_path, "r") as in_stream:
        if skip_first:
            in_stream.readline()
        for a_line in in_stream:
            yield a_line.strip()

