# -*- coding: utf-8 -*-

from __future__ import print_function
from datetime import date, timedelta
from locale import setlocale, LC_TIME

if __name__ == '__main__':
    from quickencsv import QuickenCSV
    from quotesource.sgs import SGS
    #from quotesource.gf import GF

    # Load the current locale from system settings
    # This is necessary to correct date formating
    setlocale(LC_TIME, '')

    # Entry
    # Index long name : ( data_source, accumulate_ammount, accumulate_function)

    # accumulate function valid values:
    #  * sum
    #  * interest

    INDEXES = {
        'SIMPLE DAILY INDEXES': ([
            # Indexes
            7,  # IBovespa
            11,  # Taxa de juros - SELIC
            12,  # Taxa de juros - CDI
            432,  # Taxa de juros - Meta SELIC definida pela COPOM
            1178,  # Taxa de juros - SELIC anualizada com 252 dias úteis
            4389,  # Taxa de juros - CDI anualizada com 252 dias úteis
        ], 1, ''),
        'SPECIAL DAILY INDEXES': ([
            # Indexes
            226,  # Taxa Referencial de Juros - TR
            253,  # Taxa Básica Financeira - TBF
            # Profitability
            25,  # Rentabilidade da poupança
        ], 1, ''),
        'SIMPLE MONTHLY INDEXES': ([
            # Inflation indicators
            188,  # Inflação: INPC
            189,  # Inflação: IGP-M
            193,  # Inflação: IPC-Fipe
            433,  # Inflação: IPCA (oficial do Brasil)
        ], 1, ''),
        'IPCA ACCUMULATED': ([
            # Inflation indicators - accumulated
            433,  # Inflação: IPCA (oficial do Brasil) - Acumulado 12 meses
        ], 12, 'interest'),
        'IGP-M ACCUMULATED': ([
            # Inflation indicators - accumulated
            189,  # Inflação: IGP-M - Acumulado 12 meses
        ], 12, 'interest'),
        'IPC-Fipe ACCUMULATED': ([
            # Inflation indicators - accumulated
            193,  # Inflação: IPC-Fipe - Acumulado 12 meses
        ], 12, 'interest'),
        'INPC ACCUMULATED': ([
            # Inflation indicators - accumulated
            188,  # Inflação: INPC - Acumulado 12 meses
        ], 12, 'interest'),
    }

    FILENAME = 'INDEXES_BR_QUICKEN.csv'
    INTERVAL = 60  # days

    END_DATE = date.today()
    INI_DATE = END_DATE - timedelta(days=INTERVAL)

    for indexjob in INDEXES:
        series, accumulate, accfunction = INDEXES[indexjob]
        datasource = SGS(series)

        print('Downloading %-40s... ' % (indexjob), end='')

        qcsv = QuickenCSV(datasource, accumulate, accfunction)

        if accumulate > 1:
            INI_DATE = END_DATE - timedelta(days=INTERVAL + 365)

        qcsv.update_values(INI_DATE, END_DATE)

        lines = qcsv.export_to_file(FILENAME, clear_file=False)

        print('success! (%d lines)' % lines)
