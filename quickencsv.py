# -*- coding: utf-8 -*-

from sgs import SGS
from csv import writer as csvwriter

class QuickenCSV(object):
    '''
    Class for generating CSV files for Quicken.
    
    Quicken CSV files use the following format:
        ID , DATE , VALUE
    
        Field delimiter   = comma (,)
        Quote char        = double quotes (")
        Decimal separator = dot (.)
        Date format       = dd/mm/yyyy
    '''

    def __init__(self,serie):
        '''
        Constructor
        '''
        self.fielddelimiter = ','
        self.quotechar      = '"'
        self.decimalsep     = '.'
        self.dateformat     = '%d/%m/%Y'
            
        self.quoteprefix    = 'SGS_'
        self.values         = {}
        
        self.__serie          = serie
        self.datasource = SGS(self.__serie)

    def updateValues(self,initialDate,finalDate,clearData=False):
        newValues = self.datasource.getValues(initialDate, finalDate)
        if clearData:
            self.values = newValues
        else:
            self.values.update(newValues)

    def exportToFile(self,targetFile,clearFile=True):
        if len(self.values) == 0:
            return 0
        
        with open(targetFile,'wb' if clearFile else 'ab') as f:
            csvfile = csvwriter(f, delimiter=self.fielddelimiter,quotechar=self.quotechar)
            
            data = [ (self.quoteprefix + str(self.__serie), qdate.strftime(self.dateformat), qvalue)
                    for qdate, qvalue in sorted(self.values.items()) ]
            
            # write CSV
            csvfile.writerows(data)
            
            return len(data)
            
    def export(self,clearFile=True):
        return self.exportToFile(self.quoteprefix + str(self.__serie) + '.csv', clearFile)

if __name__ == '__main__':
    from datetime import date
    
    SGSID_BOVESPA_INDEX        = 7
    SGSID_SAVING_PROFITABILITY = 25
    
    try:
        print('Connecting to webservice...')
        qcsv = QuickenCSV(25)
        print('Retrieving data...')
        qcsv.updateValues(date(1900,01,01), date.today())
    except:
        print('Service unavailable! Try again later.')
        exit()
        
    print('Exporting data...')
    lines = qcsv.export()
    
    print('Done!')
    print(str(lines) + ' lines exported.')

