# -*- coding: utf-8 -*-

from quote import Quote


class TN(Quote):
    '''
    Tesouro Nacional
    '''

    def __init__(self, tn_id):
        '''
        Constructor
        '''
        super(TN, self).__init__()
        self.__quote_id = tn_id

    def get_last_value(self):
        # FIXME: must implement
        raise NotImplementedError()

    def get_value(self, atDate):
        # FIXME: must implement
        raise NotImplementedError()

    def get_values(self, initial_date, final_date):
        # FIXME: must implement

        #for year in self.__yearRange(initial_date, final_date):
            # Download needed files
            #pass

        # detect years based on dates

        raise NotImplementedError()

    def __year_range(self, initialDate, finalDate):
        return range(initialDate.year, finalDate.year + 1)
