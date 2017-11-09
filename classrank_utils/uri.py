
def remove_corners(a_uri):
    if a_uri.startswith("<") and a_uri.endswith(">"):
        return a_uri[1:-1]
    else:
        raise RuntimeError("Wrong parameter ofr function: '" + a_uri + "'")

def add_prefix_if_possible(a_uri, prefixes):
    """

    :param a_uri: string, no corners
    :param prefixes: dictionary {prefix: uri}
    :return:
    """
    for a_pre in prefixes:
        if a_uri.startswith(prefixes[a_pre]):
            return a_uri.replace(prefixes[a_pre], a_pre + ":")
    return a_uri