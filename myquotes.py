# -*- coding: utf-8 -*-

if __name__ == '__main__':
    from quickencsv import QuickenCSV
    from quotesource.sgs import SGS
    #from quotesource.gf import GF
    
    from datetime import date, timedelta
    from locale import setlocale, LC_TIME
    
    # Load the current locale from system settings
    # This is necessary to correct date formating
    setlocale(LC_TIME,'')
    
    INDEXES = {
        # Indexes
        'SGSID_INDEX_BOVESPA'         : SGS(7)    , # IBovespa
        'SGSID_INTEREST_SELIC'        : SGS(11)   , # Taxa de juros - SELIC
        'SGSID_INTEREST_CDI'          : SGS(12)   , # Taxa de juros - CDI
        'SGSID_INTEREST_REFERENCE'    : SGS(226)  , # Taxa Referencial de Juros (TR)
        'SGSID_INTEREST_SELIC_COPOM'  : SGS(432)  , # Taxa de juros - Meta SELIC definida pela COPOM
        'SGSID_INTEREST_SELIC_ANNUAL' : SGS(1178) , # Taxa de juros - SELIC anualizada com 252 dias úteis
        'SGSID_INTEREST_CDI_ANNUAL'   : SGS(4389) , # Taxa de juros - CDI anualizada com 252 dias úteis
            
        # Profitability
        'SGSID_PROFITABILITY_SAVINGS' : SGS(25)   , # Rentabilidade da poupança
        
        # Inflation indicators
        'SGSID_INFLATION_INPC'        : SGS(188)  , # Inflação: INPC
        'SGSID_INFLATION_IGP_M'       : SGS(189)  , # Inflação: IGP-M
        'SGSID_INFLATION_IPC_FIPE'    : SGS(193)  , # Inflação: IPC-Fipe
        'SGSID_INFLATION_IPCA'        : SGS(433)  , # Inflação: IPCA (oficial do Brasil)
    }
    
    filename = 'INDEXES_BR_QUICKEN.csv'
    interval = 90 # days
    
    endDate = date.today()
    iniDate = endDate - timedelta(days=interval)
    
    for seriename in sorted(INDEXES,key=lambda x: INDEXES[x]):
        try:
            print('Connecting to webservice...')
            datasource = INDEXES[seriename]
            qcsv = QuickenCSV(datasource)
        
            print('Retrieving data of serie %s (%s)...' % (seriename[6:], INDEXES[seriename].getUniqueID()) )
            qcsv.updateValues(iniDate, endDate)
        except:
            print('Service unavailable! Try again later.')
            exit()
            
        print('Exporting data...')
        lines = qcsv.exportToFile(filename,clearFile=False)
        
        print('Done! %d lines exported.' % lines)
