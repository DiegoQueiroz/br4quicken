# -*- coding: utf-8 -*-

from __future__ import print_function

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
        # Entry
        # Index long name : ( datasource, accumulate_ammount, accumulate_function)
        
        # accumulate function valid values:
        #  * sum
        #  * interest
        
        # Indexes
        'SGSID_INDEX_BOVESPA'         : ( SGS(7)   , 1 , ''        ) , # IBovespa
        'SGSID_INTEREST_SELIC'        : ( SGS(11)  , 1 , ''        ) , # Taxa de juros - SELIC
        'SGSID_INTEREST_CDI'          : ( SGS(12)  , 1 , ''        ) , # Taxa de juros - CDI
        'SGSID_INTEREST_REFERENCE'    : ( SGS(226) , 1 , ''        ) , # Taxa Referencial de Juros (TR)
        'SGSID_INTEREST_SELIC_COPOM'  : ( SGS(432) , 1 , ''        ) , # Taxa de juros - Meta SELIC definida pela COPOM
        'SGSID_INTEREST_SELIC_ANNUAL' : ( SGS(1178), 1 , ''        ) , # Taxa de juros - SELIC anualizada com 252 dias úteis
        'SGSID_INTEREST_CDI_ANNUAL'   : ( SGS(4389), 1 , ''        ) , # Taxa de juros - CDI anualizada com 252 dias úteis

        # Indexes - accumulated
        #'SGSID_INTEREST_REFERENCE'    : ( SGS(226) , 12, 'interest') , # Taxa Referencial de Juros (TR) - Acumulado 12 meses
        # BROKEN! - this index is daily, the accumulated amount is wrong
            
        # Profitability
        'SGSID_PROFITABILITY_SAVINGS' : ( SGS(25)  , 1 , ''        ) , # Rentabilidade da poupança
       
        # Profitability - accumulated
        #'SGSID_PROFITABILITY_SAVINGS' : ( SGS(25)  , 12, 'interest') , # Rentabilidade da poupança - Acumulado 12 meses
        # BROKEN! - this index is daily, the accumulated amount is wrong
       
        # Inflation indicators
        'SGSID_INFLATION_INPC'        : ( SGS(188) , 1 , ''        ) , # Inflação: INPC
        'SGSID_INFLATION_IGP_M'       : ( SGS(189) , 1 , ''        ) , # Inflação: IGP-M
        'SGSID_INFLATION_IPC_FIPE'    : ( SGS(193) , 1 , ''        ) , # Inflação: IPC-Fipe
        'SGSID_INFLATION_IPCA'        : ( SGS(433) , 1 , ''        ) , # Inflação: IPCA (oficial do Brasil)
                
        # Inflation indicators - accumulated
        'SGSID_INFLATION_INPC-AC12'   : ( SGS(188) , 12, 'interest') , # Inflação: INPC - Acumulado 12 meses
        'SGSID_INFLATION_IGP_M-AC12'  : ( SGS(189) , 12, 'interest') , # Inflação: IGP-M - Acumulado 12 meses
        'SGSID_INFLATION_IPC_FIPE-AC12':( SGS(193) , 12, 'interest') , # Inflação: IPC-Fipe - Acumulado 12 meses
        'SGSID_INFLATION_IPCA-AC12'   : ( SGS(433) , 12, 'interest') , # Inflação: IPCA (oficial do Brasil) - Acumulado 12 meses
    }
    
    filename = 'INDEXES_BR_QUICKEN.csv'
    interval = 90 # days
    
    endDate = date.today()
    iniDate = endDate - timedelta(days=interval)
    
    for seriename in sorted(INDEXES,key=lambda x: INDEXES[x]):
        try:            
            datasource, accumulate, accfunction = INDEXES[seriename]
            print('Downloading %-40s... ' % ( "%s (%s)" % (seriename[6:], datasource.getUniqueID()) ),end='')
            
            qcsv = QuickenCSV(datasource,accumulate,accfunction)
            
            if accumulate > 1:
                iniDate = endDate - timedelta(days=interval + 365)
        
            qcsv.updateValues(iniDate, endDate)
        except:
            print('ERROR!')
            exit()
            
        lines = qcsv.exportToFile(filename,clearFile=False)
        
        print('success! (%d lines)' % lines)
