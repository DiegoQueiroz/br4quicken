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
        
        *1 - Decimal separator in Quicken IS DOT, regardless of system settings. 
        *2 - Date format in Quicken depends on system settings.
        
    More info at:
        http://quicken.intuit.com/support/help/backup--restore--file-issues/how-to-import-historical-security-data-into-quicken/GEN82637.html
    '''

    def __init__(self,quotesource,accumulate_amount=1,accumulate_function='sum'):
        '''
        Constructor
        '''
        self.fielddelimiter = ','
        self.quotechar      = '"'
        self.decimalsep     = '.'
        self.dateformat     = '%x' # use system locale
            
        self.values         = {}
        
        self.accumulatenum  = accumulate_amount
        self.accumulatefunc = accumulate_function
        
        self.datasource     = quotesource

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
            
            data = [ (self.datasource.getUniqueID(), qdate.strftime(self.dateformat), qvalue)
                    for qdate, qvalue in sorted(self.values.items()) ]
            
            if self.accumulatenum > 1:
                # Data must be accumulated
                data = self.accumulateData(data,self.accumulatenum)
            
            data = self.fixData(data)
            
            # write CSV
            csvfile.writerows(data)
            
            return len(data)
            
    def export(self,clearFile=True):
        return self.exportToFile(self.datasource.getUniqueID() + '.csv', clearFile)

    def fixData(self,data):
        newData = list()
        for symbol,date,price in data:
            
            try:
                # Quicken ignore near zero, zero or negative values
                if float(price) < 0.000001:
                    # trick to store negative values
                    # due to rounding, '0.00000001' is zero to Quicken
                    price = '0.00000001'
                    
                newData.append( (symbol, date, price) )
            except:
                # price is not numeric (probably 'None'), just ignore value
                pass
        
        return newData

    def accumulateData(self,data,num):        
        accFunc = getattr(self, 'accumulate_{0}'.format(self.accumulatefunc),None)
        
        if accFunc is not None:
            newData = list();
            for i in range(num-1,len(data)):                
                accValue = accFunc([ float(price) for _,_,price in data[i-num+1:i+1] ])
                
                # Symbol and date information matches the last item in the interval
                # All symbols are suffixed by "-ACx" where 'x' is the accumulated amount
                symbol, date, _ = data[i]
                symbol = '{0}-AC{1}'.format(symbol,num)
                
                newData.append( (symbol, date, accValue) )           
            
            return newData
        else:
            raise Exception("Unknown accumulate function named '{0}'.".format(self.accumulatefunc))

    def accumulate_interest(self,datainterval):
        return (reduce(lambda i,j:i*(1+j/100),datainterval,1)-1)*100

    def accumulate_sum(self,datainterval):
        return sum(datainterval)
