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

def class_count_dict_to_instance_counting_ranking(class_count_list):
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

    It returns a ranking of classes sorted by instance counting, with the following format:

[
  [
    "http://dbpedia.org/ontology/Person",
    0.508387094565854,
    1
  ],
  [
    "http://dbpedia.org/ontology/Agent",
    0.5,
    2
  ],
  ...
]

    :param class_count_list:
    :return:
    """
    result = []
    for an_item in class_count_list:
        if "P31" in an_item["_CP_"]:
            result.append([an_item["_CLASS_"], an_item["_CP_"]["P31"]])
    result.sort(reverse=True, key=lambda x: x[1])
    i = 0
    for an_item in result:
        i += 1
        an_item.append(i)
    return result