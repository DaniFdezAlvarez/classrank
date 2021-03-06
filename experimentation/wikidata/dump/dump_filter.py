from classrank_io.json_io import write_obj_to_json
from classrank_io.tsv_io import write_tsv_lines

S = 0
P = 1
O = 2


class _BaseDumpFilter(object):
    """
    abstract, do not isntantiate
    """

    def __init__(self, triples_yielder):
        self._triples_yielder = triples_yielder

    def generate_filter(self):
        """
        Invoke to execute the DumpFilter and write to file in standalone mode (not multifilter)
        :return:
        """
        raise NotImplementedError()

    def process_triple(self, triple):
        """
        This is thought to be used just with multifilter mode, do not use it
        outside of this class or MultiFilterDump.
        Invoke to process a single triple.

        :param triple:
        :return:
        """
        raise NotImplementedError()

    def close_filter(self):
        """
        This is thought to be used just with multifilter mode, do not use it
        outside of this class or MultiFilterDump.
        Invoke when all the triples has been processed

        :return:
        """
        raise NotImplementedError()


class _BaseDirectedGraphDumpFilter(_BaseDumpFilter):
    """
    abstract, do not isntantiate
    """

    def __init__(self, triples_yielder, separator, multifilter_compatibility):
        super().__init__(triples_yielder=triples_yielder)
        self._multifilter_compatibility = multifilter_compatibility
        self._separator = separator

    def _triple_to_adequate_line(self, a_triple):
        return self._separator.join([a_triple[0], a_triple[2]])

    def _write_line(self, line, stream):
        stream.write(line + "\n")


class DirectedGraphDumpFilter(_BaseDirectedGraphDumpFilter):

    def __init__(self, triples_yielder, target_file, separator="\t", multifilter_compatibility=False):
        super().__init__(triples_yielder=triples_yielder,
                         separator=separator,
                         multifilter_compatibility=multifilter_compatibility)
        self._target_file = target_file
        self._out_stream = None if not multifilter_compatibility else open(self._target_file, "w")

    def generate_filter(self):
        with open(self._target_file, "w") as out_stream:
            for a_triple in self._triples_yielder:
                self._write_line(line=self._triple_to_adequate_line(a_triple),
                                 stream=out_stream)

    def process_triple(self, triple):
        """
        This is thought to be used just with multifilter_compatibility mode.
        Invoke to process a single triple.

        :param triple:
        :return:
        """
        self._write_line(line=self._triple_to_adequate_line(triple),
                         stream=self._out_stream)

    def close_filter(self):
        """
        This is thought to be used just with multifilter_compatibility mode.
        Invoke when all the triples has been processed

        :return:
        """
        self._out_stream.close()


class DirectedGraphSlicerDumpFilter(_BaseDirectedGraphDumpFilter):
    def __init__(self, triples_yielder, base_file_path, separator="\t", extension="tsv", max_triples_per_file=1000000):
        super().__init__(triples_yielder=triples_yielder,
                         separator=separator,
                         multifilter_compatibility=True)  # Doesnt matter, we do not need it

        self._base_file_path = base_file_path
        self._extension = extension
        self._max_triples = max_triples_per_file
        self._triples_count = 0
        self._current_file_id = 0
        self._out_stream = None  # It will be initialized with _open_new_stream()

        self._open_new_stream()

    def generate_filter(self):
        """
        Invoke to execute the DumpFilter and write to file in standalone mode (not multifilter)
        :return:
        """
        for a_triple in self._triples_yielder.yield_triples():
            self.process_triple(a_triple)

        self.close_filter()

    def process_triple(self, triple):
        self._triples_count += 1
        if self._triples_count % self._max_triples == 0:
            self._open_new_stream()
        self._write_line(line=self._triple_to_adequate_line(triple),
                         stream=self._out_stream)

    def close_filter(self):
        if self._out_stream is not None:
            self._out_stream.close()

    def _open_new_stream(self):
        if self._out_stream is not None:
            self._out_stream.close()
        self._out_stream = open(self._path_to_new_stream(), "w")

    def _path_to_new_stream(self):
        self._current_file_id += 1
        return self._base_file_path + str(self._current_file_id) + "." + self._extension


class TSVGraphSlicerDumpFilter(DirectedGraphSlicerDumpFilter):

    def __init__(self, triples_yielder, base_file_path, max_triples_per_file=1000000):
        super().__init__(triples_yielder=triples_yielder,
                         base_file_path=base_file_path,
                         separator="\t",
                         max_triples_per_file=max_triples_per_file)

    def _triple_to_adequate_line(self, a_triple):
        return self._separator.join(a_triple)


_TOTALS_KEY = "_TOTALS_"
_CLASS_KEY = "_CLASS_"
_POSITION_KEY = "_POS_"
_CLASS_POINTERS_KEY = "_CP_"


class ClassCountDumpFilter(_BaseDumpFilter):

    def __init__(self, triples_yielder, classpointers, target_path):
        super().__init__(triples_yielder=triples_yielder)

        self._class_pointers = classpointers
        self._target_path = target_path
        self._link_dict = {}

    def generate_filter(self):
        for a_triple in self._triples_yielder.yield_triples():
            self.process_triple(a_triple)
        self.close_filter()

    def process_triple(self, triple):
        if triple[P] in self._class_pointers:
            self._annotate_triple(triple)

    def _annotate_triple(self, triple):
        if triple[O] not in self._link_dict:
            self._link_dict[triple[O]] = {}
        if triple[P] not in self._link_dict[triple[O]]:
            self._link_dict[triple[O]][triple[P]] = 0
        self._link_dict[triple[O]][triple[P]] += 1

    def close_filter(self):
        self._compute_totals()
        self._dict_to_sorted_list()
        self._write_results()

    def _compute_totals(self):
        for a_class, a_class_dict in self._link_dict.items():
            self._link_dict[a_class] = {_CLASS_POINTERS_KEY: a_class_dict,
                                        _CLASS_KEY: a_class,
                                        _TOTALS_KEY: sum([a_count for a_count in a_class_dict.values()])}
            # a_class_dict[_TOTALS_KEY] = sum([a_count for a_count in a_class_dict.values()])

    def _dict_to_sorted_list(self):
        result = []
        for a_class_dict in self._link_dict.values():  # Dict to list in 'result'
            result.append(a_class_dict)
            # a_class_dict[_CLASS_KEY] = a_class
            # result.append({_CLASS_POINTERS_KEY : a_class_dict,
            #                _CLASS_KEY : a_class})
        self._link_dict = None  # Free memory
        result.sort(reverse=True, key=lambda x: x[_TOTALS_KEY])  # Sort
        rank = 0
        for a_class_dict in result:  # Add explicit position
            rank += 1
            a_class_dict[_POSITION_KEY] = rank
        self._link_dict = result  # Set the att to the resulting list

    def _write_results(self):
        write_obj_to_json(target_obj=self._link_dict,
                          out_path=self._target_path,
                          indent=2)

class ClassListDumpFilter(_BaseDumpFilter):


    def __init__(self, triples_yielder, target_file, just_o_props, s_and_o_props):
        super().__init__(triples_yielder)
        self._target_file = target_file
        self._just_o_props = just_o_props
        self._s_and_o_props = s_and_o_props

        self._classes_set = set()

    def generate_filter(self):
        for a_triple in self._triples_yielder.yield_triples():
            self.process_triple(a_triple)
        self.close_filter()

    def process_triple(self, triple):
        if triple[P] in self._just_o_props:
            self._classes_set.add(triple[O])
        elif triple[P] in self._s_and_o_props:
            self._classes_set.add(triple[O])
            self._classes_set.add(triple[S])

    def close_filter(self):
        write_tsv_lines(file_path=self._target_file,
                        iterable=self._classes_set)


class TBOXGraphDumpFilter(_BaseDumpFilter):

    def __init__(self, triples_yielder, target_file, set_target_classes, max_triples=-1):
        super().__init__(triples_yielder)
        self._target_file = target_file
        self._set_target_classes = set_target_classes
        self._max_triples = max_triples
        self._out_stream = open(target_file, "w")

    def generate_filter(self):
        for a_triple in self._triples_yielder.yield_triples(max_triples=self._max_triples):
            self.process_triple(a_triple)
        self.close_filter()

    def process_triple(self, triple):
        if triple[S] in self._set_target_classes and triple[O] in self._set_target_classes:
            self._write_triple(triple)

    def _write_triple(self, triple):
        self._out_stream.write("<{}> <{}> <{}> .\n".format(triple[S], triple[P], triple[O]))

    def close_filter(self):
        self._out_stream.close()


_KEY_PROPS_CLASS = "classes"
_KEY_PROPS_INSTANCE = "instance"

SORT_BY_CPS = "cps"
SORT_BY_NON_CPS = "not-cps"
SORT_BY_TOTAL = "all"
SORT_BY_RATIO = "ratio"

class CountSortAndClasiffyPropsDumpFilter(_BaseDumpFilter):

    def __init__(self, triples_yielder, classes_set, target_file, max_triples=-1, sort_by=SORT_BY_RATIO):
        super().__init__(triples_yielder)
        self._c_set = classes_set
        self._max_triples = max_triples
        self._target_file = target_file
        self._sort_by = sort_by

        self._props_dict = {}

    def generate_filter(self):
        for a_triple in self._triples_yielder.yield_triples():
            self.process_triple(a_triple)
        self.close_filter()

    def process_triple(self, triple):
        self._annotate_property_if_needed(triple[P])
        self._annotate_object(triple)

    def close_filter(self):
        self._adapt_internal_results()
        self._write_result()

    def _write_result(self):
        write_obj_to_json(target_obj=self._props_dict,
                          out_path=self._target_file)

    def _adapt_internal_results(self):
        self._props_dict = [
            [0, # 0
             a_key,  # 1
             a_dict[_KEY_PROPS_CLASS],  # 2
             a_dict[_KEY_PROPS_INSTANCE],  # 3
             a_dict[_KEY_PROPS_CLASS] + a_dict[_KEY_PROPS_INSTANCE],  # 4
             self._class_ratio(classes=a_dict[_KEY_PROPS_CLASS], instances=a_dict[_KEY_PROPS_INSTANCE])
             ]
            for a_key, a_dict in self._props_dict.items()
        ]
        self._props_dict.sort(reverse=True, key=self._lambda_to_sort())
        i = 1
        for a_list in self._props_dict:
            a_list[0] = i
            i += 1

    def _class_ratio(self, classes, instances):
        den = classes + instances
        return 0.0 if den == 0 else (classes / den)

    def _lambda_to_sort(self):
        if self._sort_by == SORT_BY_CPS:
            return lambda x:x[2]
        elif self._sort_by == SORT_BY_NON_CPS:
            return lambda x:x[3]
        elif self._sort_by == SORT_BY_TOTAL:
            return lambda x:x[4]
        elif self._sort_by == SORT_BY_RATIO:
            return lambda x:x[5]
        else:
            raise ValueError("Unknown key for sorting: '{}'. Acepted values are '{}', '{}', '{}', '{}'".format(
                self._sort_by,
                SORT_BY_RATIO,
                SORT_BY_TOTAL,
                SORT_BY_CPS,
                SORT_BY_NON_CPS
            ))

    def _annotate_object(self, triple):
        target_key = _KEY_PROPS_CLASS if triple[O] in self._c_set else _KEY_PROPS_INSTANCE
        self._props_dict[triple[P]][target_key] += 1

    def _annotate_property_if_needed(self, prop):
        if prop not in self._props_dict:
            self._props_dict[prop] = {_KEY_PROPS_CLASS: 0,
                                      _KEY_PROPS_INSTANCE: 0}


class MultiDumpFilter(_BaseDumpFilter):
    def __init__(self, triples_yielder, dump_filters):
        super().__init__(triples_yielder)
        self._dump_filers = dump_filters

    def generate_filter(self):
        """
        Executes all the filters at a time, using a single read to the triple_yielder for them all.
        :return:
        """
        self._process_triples()
        self._close_dump_filters()

    def _process_triples(self):
        for a_triple in self._triples_yielder.yield_triples():
            for a_dump_filter in self._dump_filers:
                a_dump_filter.process_triple(a_triple)

    def _close_dump_filters(self):
        for a_dump_filter in self._dump_filers:
            a_dump_filter.close_filter()

    def process_triple(self, triple):
        pass  # Not needed

    def close_filter(self):
        pass  # Nor needed
