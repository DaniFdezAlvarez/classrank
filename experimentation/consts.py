import re

REGEX_WHOLE_URI = re.compile("<[^ ]+>")
REGEX_PREFIXED_URI = re.compile("[ ,;\.\(\{\[\n\t][^<>\? ,;\.\(\{\[\n\t/\^]*:[^<>\? ,;\.\)\}\]\n\t]*[ ,;\.\)\}\]\n\t]")
REGEX_PREFIX = re.compile("PREFIX", flags=re.IGNORECASE)

REGEX_TYPE_QUERY = re.compile("(^|[\s>])((SELECT)|(ASK)|(CONSTRUCT)|(DESCRIBE))[\*\s\{\(]",
                              flags=re.IGNORECASE)

MIN_LENGHT_PREFIX = 11