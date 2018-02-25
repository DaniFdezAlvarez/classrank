def build_dict_of_prefixes_from_tuples(prefix_tuples, inverse=True):
        result = {}
        if prefix_tuples is None:
            return result
        for a_tuple in prefix_tuples:
            if not inverse:
                result[a_tuple[0]] = a_tuple[1]
            else:
                result[a_tuple[1]] = a_tuple[0]
        return result