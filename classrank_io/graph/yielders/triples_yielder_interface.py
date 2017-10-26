"""
Object able to transform a certain source (a file, some online content, raw text...) into a list of triples
which is returned with yield.

The main funcionallity of the instantiated objects should be encapsulated in the method "yield_triples()".
The params of the __init__ method may defer depending on the nature of the targeted source.
"""


class TriplesYielderInterface(object):
    def __init__(self):
        pass

    def yield_triples(self, max_triples=-1):
        """
        It returns a set of triples. If max_triples has a positive value,
        it returns $max_triples triples as most.

        :return:
        """
        raise NotImplementedError("Method should be redefined")

    @property
    def yielded_triples(self):
        raise NotImplementedError("Method should be redefined")

    @property
    def error_triples(self):
        raise NotImplementedError("Method should be redefined")

    @property
    def ignored_triples(self):
        raise NotImplementedError("Method should be redefined")

    def _reset_count(self):
        """
        Just to remember that the counts may be managed if the object is used to parse
        more than one time
        :return:
        """
        raise NotImplementedError("Method should be redefined")