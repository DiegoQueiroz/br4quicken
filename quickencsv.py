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
    from datetime import date, timedelta
    from locale import setlocale, LC_TIME
    
    # Load the current locale from system settings
    # This is necessary to correct date formating
    setlocale(LC_TIME,'')
    
    INDEXES = {
        # Indexes
        'SGSID_INDEX_BOVESPA'         : 7    , # IBovespa
        
        'SGSID_INTEREST_SELIC'        : 11   , # Taxa de juros - SELIC
        'SGSID_INTEREST_CDI'          : 12   , # Taxa de juros - CDI
        'SGSID_INTEREST_REFERENCE'    : 226  , # Taxa Referencial de Juros (TR)
        'SGSID_INTEREST_SELIC_COPOM'  : 432  , # Taxa de juros - Meta SELIC definida pela COPOM
        'SGSID_INTEREST_SELIC_ANNUAL' : 1178 , # Taxa de juros - SELIC anualizada com 252 dias úteis
        'SGSID_INTEREST_CDI_ANNUAL'   : 4389 , # Taxa de juros - CDI anualizada com 252 dias úteis
            
        # Profitability
        'SGSID_PROFITABILITY_SAVINGS' : 25   , # Rentabilidade da poupança
        
        # Inflation indicators
        'SGSID_INFLATION_INPC'        : 188  , # Inflação: INPC
        'SGSID_INFLATION_IGP_M'       : 189  , # Inflação: IGP-M
        'SGSID_INFLATION_IPC_FIPE'    : 193  , # Inflação: IPC-Fipe
        'SGSID_INFLATION_IPCA'        : 433  , # Inflação: IPCA (oficial do Brasil)
    }
    
    filename = 'INDEXES_BR_QUICKEN.csv'
    interval = 90
    
    endDate = date.today()
    iniDate = endDate - timedelta(days=interval)
    
    for serie in sorted(INDEXES,key=lambda x: INDEXES[x]):
        try:
            print('Connecting to webservice...')
            qcsv = QuickenCSV(INDEXES[serie])
            print('Retrieving data of serie %s (%d)...' % (serie[6:], INDEXES[serie]) )
            qcsv.updateValues(iniDate, endDate)
        except:
            print('Service unavailable! Try again later.')
            exit()
            
        print('Exporting data...')
        lines = qcsv.exportToFile(filename,clearFile=False)
        
        print('Done! %d lines exported.' % lines)

