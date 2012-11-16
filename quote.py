class Quote(object):
    '''
    Abstract base class for quote downloading.
    '''

    def __init__(self):
        '''
        Constructor
        '''
        pass
        
    def getLastValue(self):
        raise NotImplementedError()
    
    def getValue(self,atDate):
        raise NotImplementedError()
    
    def getValues(self,initialDate,finalDate):
        raise NotImplementedError()

    def getUniqueID(self):
        raise NotImplementedError()