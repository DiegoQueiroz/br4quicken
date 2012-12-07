# -*- coding: utf-8 -*-

from suds import client
from datetime import date
from quote import Quote
from urllib2 import getproxies

class SGS(Quote):
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
        # SOAP constant settings
        self.__sgsurl = 'https://www3.bcb.gov.br/sgspub/JSP/sgsgeral/FachadaWSSGS.wsdl'
        self.__xmlencoding = 'ISO-8859-1'
        self.__dateformat = '%d/%m/%Y'
        
        self.__serie = serie
        self.__soap = None
        self.__uid = 'SGS_{0}'.format(self.__serie)
    
    def __soapInit(self):
        # An exception can be raised here if the service is
        # unavailable for some reason
        if not self.__soap:
            self.__soap = client.Client(self.__sgsurl,proxy=getproxies())
    
    def __soapGetValue(self,atDate):
        self.__soapInit()
        strDate = atDate.strftime(self.__dateformat)
        return self.__soap.service.getValor(self.__serie,strDate)
    
    def __soapGetValue2(self,initialDate,finalDate):
        self.__soapInit()
        strIniDate = initialDate.strftime(self.__dateformat)
        strFinDate = finalDate.strftime(self.__dateformat)
        return self.__soap.service.getValorEspecial(self.__serie,strIniDate,strFinDate)
    
    def __soapGetLastValue(self,xml=False):
        self.__soapInit()
        if xml:
            xmlret = self.__soap.service.getUltimoValorXML(self.__serie)
            return xmlret.encode(self.__xmlencoding)
        else:
            return self.__soap.service.getUltimoValorVO(self.__serie)
    
    def __soapGetValues(self,initialDate,finalDate,xml=False):
        self.__soapInit()
        strIniDate = initialDate.strftime(self.__dateformat)
        strFinDate = finalDate.strftime(self.__dateformat)
        if xml:
            xmlret = self.__soap.service.getValoresSeriesXML([self.__serie],strIniDate,strFinDate)
            return xmlret.encode(self.__xmlencoding)
        else:
            return self.__soap.service.getValoresSeriesVO([self.__serie],strIniDate,strFinDate)[0]
    
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
            data = self.__soapGetValues(initialDate,finalDate,xml=False)
            return { date(value.ano,value.mes,value.dia): value.valor for value in data.valores }
        except:
            return {}

    def getUniqueID(self):
        return self.__uid
    