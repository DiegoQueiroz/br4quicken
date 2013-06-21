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
        Get last available value for the quote.
        @return: A floating point with the value.
        '''
        raise NotImplementedError()

    def get_value(self, at_date):
        '''
        Get quote value on a specified date.
        @return: A floating point with the value.
        '''
        raise NotImplementedError()

    def get_values(self, initial_date, final_date):
        '''
        Get all available values of a quote in a interval of dates.
        @return: A dictionary with pairs "ticker, date: quotation".  If there
           are multiple quotations for different times of the same date, the
           dictionary can use datetime instead of date.  Each quotation
           is a floating point.
        '''
        raise NotImplementedError()
