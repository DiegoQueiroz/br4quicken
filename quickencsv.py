# -*- coding: utf-8 -*-

from csv import writer as csvwriter


class QuickenCSV(object):
    '''
    Class for generating CSV files for Quicken.

    Quicken CSV files use the following format:
        SYMBOL , DATE , PRICE

        Field delimiter   = comma (,) or double space (  )
        Quote char        = double quotes (")
        Decimal separator = dot (.), see *1
        Date format       = see *2

        *1 - Decimal separator in Quicken IS DOT, regardless of system settings
        *2 - Date format in Quicken depends on system settings

    More info at:
        http://quicken.intuit.com/support/help/
        backup--restore--file-issues/
        how-to-import-historical-security-data-into-quicken/GEN82637.html
    '''

    def __init__(self, quote_source, accumulate_amount=1,
                 accumulate_function='sum'):
        '''
        Constructor
        '''
        self.field_delimiter = ','
        self.quote_char = '"'
        self.decimal_sep = '.'
        self.date_format = '%x'  # use system locale

        self.values = {}

        self.accumulate_amount = accumulate_amount
        self.accumulate_func = accumulate_function

        self.data_source = quote_source

    def update_values(self, initial_date, final_date, clear_data=False):
        new_values = self.data_source.get_values(initial_date, final_date)
        if clear_data:
            self.values = new_values
        else:
            self.values.update(new_values)

    def export_to_file(self, target_file, clear_file=True):
        if len(self.values) == 0:
            return 0

        with open(target_file, 'wb' if clear_file else 'ab') as f:
            csvfile = csvwriter(f, delimiter=self.field_delimiter,
                                quotechar=self.quote_char)

            data = [(qserie, qdate.strftime(self.date_format), qvalue)
                     for (qserie, qdate), qvalue in
                        sorted(self.values.items())]

            if self.accumulate_amount > 1:
                # Data must be accumulated
                data = self.accumulate_data(data, self.accumulate_amount)

            data = self.fix_data(data)

            # write CSV
            csvfile.writerows(data)

            return len(data)

    def export(self, clear_file=True):
        filename = self.data_source.get_unique_ID() + '.csv'
        return self.export_to_file(filename, clear_file)

    def fix_data(self, data):
        new_data = list()
        for symbol, date, price in data:

            try:
                # Quicken ignore near zero, zero or negative values.
                # This is a trick to trick to store zero and negative values:
                # due to rounding, '0.00000001' is ZERO to Quicken
                if float(price) < 0.000001:
                    price = '0.00000001'

                new_data.append((symbol, date, price))
            except TypeError:
                # Price is not numeric (probably 'None'),
                # so just ignore this value.
                pass

        return new_data

    def accumulate_data(self, data, num):
        acc_func_name = 'accumulate_{0}'.format(self.accumulate_func)
        acc_func = getattr(self, acc_func_name, None)

        if acc_func is not None:
            new_data = list()
            for i in range(num - 1, len(data)):
                acc_value = acc_func([float(price)
                                      for _, _, price in
                                      data[i - num + 1:i + 1]])

                # Symbol and date information matches the last item
                # in the interval suffixed by "-ACx"
                # where 'x' is the accumulated amount
                symbol, date, _ = data[i]
                symbol = '{0}-AC{1}'.format(symbol, num)

                new_data.append((symbol, date, acc_value))

            return new_data
        else:
            msg = "Unknown accumulate function named '{0}'."
            raise Exception(msg.format(self.accumulate_func))

    def accumulate_interest(self, data_interval):
        product = reduce(lambda i, j: i * (1 + j / 100), data_interval, 1)
        return (product - 1) * 100

    def accumulate_sum(self, data_interval):
        return sum(data_interval)
