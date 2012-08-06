# -*- coding: utf-8 -*-

from suds import client
from datetime import date

class SGS(object):
    '''
    Class for access public data from Central Bank of Brazil through
    the "Sistema Gerenciador de Séries Temporais", acronym of SGS.
    
    More info at:
        http://www4.bcb.gov.br/pec/series/port/aviso.asp
    
    Access to the system:
        https://www3.bcb.gov.br/sgspub/
    Help on automated services (webservices):
        https://www3.bcb.gov.br/sgspub/JSP/sgsgeral/sgsAjuda.jsp#SA
    '''

    def __init__(self):
        '''
        Constructor
        '''
        self.sgsurl = 'https://www3.bcb.gov.br/sgspub/JSP/sgsgeral/FachadaWSSGS.wsdl'
        self.soap = client.Client(self.sgsurl)
      
    def getLastValue(self,serie):
        try:
            value = self.soap.service.getUltimoValorVO(serie).ultimoValor    
            return date(value.ano,value.mes,value.dia), value.valor
        except:
            return None
    
    def getValue(self,serie,atDate):
        try:
            strDate = atDate.strftime('%d/%m/%Y')
            return self.soap.service.getValue(serie,strDate)
        except:
            return None
    
    def getValues(self,serie,initialDate,finalDate):
        try:
            strIniDate = initialDate.strftime('%d/%m/%Y')
            strFinDate = finalDate.strftime('%d/%m/%Y')
            data = self.soap.service.getValoresSeriesVO([serie],strIniDate,strFinDate)[0]
            return { date(value.ano,value.mes,value.dia): value.valor for value in data.valores }
        except:
            return None
    
    