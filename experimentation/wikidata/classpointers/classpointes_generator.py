from classrank_io.json_io import read_json_obj_from_path

RANK_POSITION = 0
ID_POSITION = 1
CLASSES_POSITION = 2
INSTANCES_POSITION = 3
TOTALS_POSITION = 4
RATIO_POSITION = 5
LABEL_POSITION = 6

class ClasspointersGenerator(object):
    """
    Expected file format:
    [
      [
        1,  # Rank
        "P31",  # ID
        94119660,  # Classes
        0,  # Instances
        94119660,  # Total
        1.0,  # ratio
        "instance of"  # label
      ],
      [
        2,
        "P279",
        3025254,
        0,
        3025254,
        1.0,
        "subclass of"
      ],
    ....
    """

    def __init__(self, source_file):
        self._source_file = source_file
        self._internal_cp_table = self._load_cp_table()

    def cp_subset_by_ratio(self, min_class_ratio):
        return {a_cp_row[ID_POSITION]
                for a_cp_row in self._internal_cp_table
                if a_cp_row[RATIO_POSITION] >= min_class_ratio}

    def cp_subsets_by_ratios(self, ratios_list):
        return [self.cp_subset_by_ratio(a_ratio) for a_ratio in ratios_list]

    def _load_cp_table(self):
        return read_json_obj_from_path(target_path=self._source_file)
