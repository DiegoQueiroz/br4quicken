# -*- coding: utf-8 -*-

from sgs import SGS
from csv import writer as csvwriter

class QuickenCSV(object):
    '''
    Class for generating CSV files for Quicken.
    
    Quicken CSV files use the following format:
        SYMBOL , PRICE , DATE
    
        Field delimiter   = comma (,) or double space (  )
        Quote char        = double quotes (")
        Decimal separator = dot (.), see *1
        Date format       = see *2
        
        *1 - Decimal separator in Quicken IS DOT, regardless of system settings. 
        *2 - Date format in Quicken depends on system settings.
        
    More info at:
        http://quicken.intuit.com/support/help/backup--restore--file-issues/how-to-import-historical-security-data-into-quicken/GEN82637.html
    '''

    def __init__(self,serie):
        '''
        Constructor
        '''
        self.fielddelimiter = ','
        self.quotechar      = '"'
        self.decimalsep     = '.'
        self.dateformat     = '%x' # use system locale
            
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
    from locale import setlocale, LC_TIME
    
    # Load the current locale from system settings
    # This is necessary to correct date formating
    setlocale(LC_TIME,'')
    
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
    
    print('Done! ' + str(lines) + ' lines exported.')

