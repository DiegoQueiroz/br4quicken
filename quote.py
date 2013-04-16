class Quote(object):
    '''
    Abstract base class for quote downloading.
    '''

    def __init__(self):
        '''
        Constructor
        '''
        pass

    def get_last_value(self):
        '''
        Get last available value for the quote
        Returns:
         - A floating point with the value.
        '''
        raise NotImplementedError()

    def get_value(self, at_date):
        '''
        Get quote value on a specified date.
        Returns:
         - A floating point with the value.
        '''
        raise NotImplementedError()

    def get_values(self, initial_date, final_date):
        '''
        Get all available values of a quote in a interval of dates.
        Returns:
         - A dictionary with pairs "date: quotation". If there are multiple
           quotations for different times of the same date, the dictionary
           can be pairs of "datetime: quotation".
        '''
        raise NotImplementedError()

    def get_unique_ID(self):
        '''
        Get a unique identification for the quote.
        Returns:
         - A string with the quote ID.
        '''
        raise NotImplementedError()
