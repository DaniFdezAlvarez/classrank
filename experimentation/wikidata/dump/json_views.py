def class_count_dict_to_class_set(class_count_list):
    """
    It expects a list of dicts with the following structure:
    
    [
  {
    "_POS_": 1,
    "_CP_": {
      "P279": 19,
      "P31": 36338322
    },
    "_TOTALS_": 36338341,
    "_CLASS_": "Q13442814"
  },
  {
    "_POS_": 2,
    "_CP_": {
      "P279": 236,
      "P31": 8218111
    },
    "_TOTALS_": 8218347,
    "_CLASS_": "Q5"
  },
  
  ....
  ]
  
  It returns a set of every class mentioned in the dicts

    :param class_count_list: 
    :return: 
    """
    return set([a_dict["_CLASS_"] for a_dict in class_count_list])