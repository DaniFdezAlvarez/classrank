"""
Functionallity encalsulated in hte method format_classrank_dict()

There must be always a return, but it could also happen to have some other
outputs of different type. Ex: result to a file.

"""

class ClassRankFormatterInterface(object):

    def __init__(self):
        pass


    def format_classrank_dict(self, a_dict):
        """
        It receives a dict and returns it in a given format. The expected form of this dict is:

        {
            "$Key_of_a_class1" : { "_KEY_OF_CLASSPOINTERS : { "$Key_of_cp_1" : set($key_of_e_1,
                                                                                   $key_of_e_2,
                                                                                    ...),
                                                              "$Key_of_cp_1" : set($key_of_e_1,
                                                                                   $key_of_e_2,
                                                                                    ...),

                                 , "_KEY_OF_INSTANCES: $integer_number
                                 , "_KEY_OF_SCORE: $f float_number
                                 },

            "$Key_of_a_class2" : { "_KEY_OF_CLASSPOINTERS : { "$Key_of_cp_1" : set($key_of_e_1,
                                                                                   $key_of_e_2,
                                                                                    ...),
                                                              "$Key_of_cp_1" : set($key_of_e_1,
                                                                                   $key_of_e_2,
                                                                                    ...),

                                 , "_KEY_OF_INSTANCES: $integer_number
                                 , "_KEY_OF_SCORE: $f float_number
                                 },

            ...
        }
        :param a_dict:
        :return:
        """
        raise NotImplementedError()