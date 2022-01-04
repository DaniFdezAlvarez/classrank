import re
from experimentation.consts import REGEX_PREFIX, REGEX_WHOLE_URI, REGEX_PREFIXED_URI
from classrank_utils.uri import remove_corners


def parse_new_prefixes(str_prefixes_list):
    if len(str_prefixes_list) < 11:  # len("prefix : <>")
        return {}
    pieces = re.split(REGEX_PREFIX, str_prefixes_list)
    if len(pieces) < 2:  # The first piece does not contain a nampespace, thats before the first PREFIX keyword
        return {}
    result = {}
    for a_piece in pieces:
        index_end_prefix = a_piece.find(":")  # First ':' will be the ':' used after the prefix
        prefix = a_piece[:index_end_prefix].strip()

        index_beg_uri = a_piece.find("<") + 1
        index_end_uri = a_piece.find(">")

        result[prefix] = a_piece[index_beg_uri:index_end_uri]
    return result


def replace_literal_spaces_with_blank(query, literal_spaces):
    result = query
    for a_space_tuple in reversed(literal_spaces):
        result = result[:a_space_tuple[0]] + " " + result[a_space_tuple[1] + 1:]
    return result


def detect_complete_uri_mentions(query):
    return [remove_corners(a_uri) for a_uri in re.findall(REGEX_WHOLE_URI, query)]


def detect_prefixed_uri_mentions(query, complete_uris=None):
    if complete_uris is not None:
        for an_uri in complete_uris:
            query = query.replace("<"+an_uri+">", " ")
    return [match[1:-1] for match in re.findall(REGEX_PREFIXED_URI, query)]


def detect_literal_spaces(str_query):
    indexes = []
    index = 0
    for char in str_query:
        if char == '"':
            if index == 0:
                indexes.append(index)
            elif str_query[index - 1] == '\\':
                if index >= 2 and str_query[index - 2] == '\\':
                    indexes.append(index)
        index += 1
    if len(indexes) % 2 != 0:
        raise ValueError("The query has an odd number of non-scaped quotes: " + str_query)
    if len(indexes) == 0:
        return []
    result = []
    i = 0
    while i < len(indexes):
        result.append((indexes[i], indexes[i + 1]))
        i += 2
    return result