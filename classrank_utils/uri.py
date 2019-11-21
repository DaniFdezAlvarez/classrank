

_INVALID_CHARS_CORNERS = '<>" {}|\\^`'
_INVALID_CHARS_NO_CORNERS = '" {}|\\^`'

def remove_corners(a_uri, raise_error=True):
    if a_uri.startswith("<") and a_uri.endswith(">"):
        return a_uri[1:-1]
    if raise_error:
        raise RuntimeError("Wrong parameter of function: '" + a_uri + "'")
    else:
        return a_uri

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


def is_valid_uri(uri, there_are_corners=True):
    if there_are_corners:
        uri = uri[1:-1]
    for a_c in _INVALID_CHARS_CORNERS:
        if a_c in uri:
            return False
    # else:
    #     for a_c in _INVALID_CHARS_NO_CORNERS:
    #         if a_c in uri:
    #             return False
    return True

def is_valid_uri_soft_check(uri, there_are_corners=True):
    first_index = 1 if there_are_corners else 0
    # print(uri[first_index:])
    return uri[first_index:].startswith("http://")

def is_valid_triple(s,p,o, there_are_corners=True):
    if not is_valid_uri(s, there_are_corners):
        return False
    if not is_valid_uri(p, there_are_corners):
        return False
    if not is_valid_uri(o, there_are_corners):
        return False
    return True


