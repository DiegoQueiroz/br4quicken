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
    
    def __init__(self,serie):
        '''
        Constructor
        '''
        self.sgsurl = 'https://www3.bcb.gov.br/sgspub/JSP/sgsgeral/FachadaWSSGS.wsdl'
        self.soap = client.Client(self.sgsurl)
        
        self.serie = serie
    
    def __soapGetValue(self,atDate):
        strDate = atDate.strftime('%d/%m/%Y')
        return self.soap.service.getValue(self.serie,strDate)
    
    def __soapGetValue2(self,initialDate,finalDate):
        strIniDate = initialDate.strftime('%d/%m/%Y')
        strFinDate = finalDate.strftime('%d/%m/%Y')
        return self.soap.service.getValorEspecial(self.serie,strIniDate,strFinDate)
    
    def __soapGetLastValue(self,xml=False):
        if xml:
            xmlret = self.soap.service.getUltimoValorXML(self.serie)
            return xmlret.encode('ISO-8859-1')
        else:
            return self.soap.service.getUltimoValorVO(self.serie)
    
    def __soapGetValues(self,initialDate,finalDate,xml=False):
        strIniDate = initialDate.strftime('%d/%m/%Y')
        strFinDate = finalDate.strftime('%d/%m/%Y')
        if xml:
            xmlret = self.soap.service.getValoresSeriesXML([self.serie],strIniDate,strFinDate)
            return xmlret.encode('ISO-8859-1')
        else:
            return self.soap.service.getValoresSeriesVO([self.serie],strIniDate,strFinDate)[0]
    
    def listAvailableMetadata(self):
        try:
            obj = self.__soapGetLastValue
            return [ attr for attr in dir(obj) if not attr.startswith('__') ]
        except:
            return []
    
    def getMetadata(self,metadata):
        try:
            obj = self.__soapGetLastValue
            return getattr(obj,metadata)
        except:
            return None
    
    def getLastValue(self):
        try:
            value = self.__soapGetLastValue.ultimoValor    
            return date(value.ano,value.mes,value.dia), value.valor
        except:
            return None
    
    def getValue(self,atDate):
        try:
            return self.__soapGetValue(atDate)
        except:
            return None
    
    def getValues(self,initialDate,finalDate):
        try:
            data = self.__soapGetValues(initialDate,finalDate)
            return { date(value.ano,value.mes,value.dia): value.valor for value in data.valores }
        except:
            return {}

