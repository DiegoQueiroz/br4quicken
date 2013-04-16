# -*- coding: utf-8 -*-

from datetime import date
from urllib2 import getproxies
from suds import client, WebFault

from quote import Quote


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

    def __init__(self, serie):
        '''
        Constructor
        '''
        super(SGS, self).__init__()

        # SOAP constant settings
        self.__sgs_url = 'https://www3.bcb.gov.br/sgspub/JSP/sgsgeral/' \
                         'FachadaWSSGS.wsdl'
        self.__xml_encoding = 'ISO-8859-1'
        self.__date_format = '%d/%m/%Y'

        self.__serie = serie
        self.__soap = None
        self.__uid = 'SGS_{0}'.format(self.__serie)

    def __soap_init(self):
        # An exception can be raised here if the service is
        # unavailable for some reason
        if not self.__soap:
            self.__soap = client.Client(self.__sgs_url, proxy=getproxies())

    def __soap_get_value(self, at_date):
        self.__soap_init()
        str_date = at_date.strftime(self.__date_format)
        return self.__soap.service.getValor(self.__serie, str_date)

    def __soap_get_value2(self, initial_date, final_date):
        self.__soap_init()
        str_ini_date = initial_date.strftime(self.__date_format)
        str_fin_date = final_date.strftime(self.__date_format)
        return self.__soap.service.getValorEspecial(self.__serie,
                                                    str_ini_date, str_fin_date)

    def __soap_get_last_value(self, xml=False):
        self.__soap_init()
        if xml:
            xml_ret = self.__soap.service.getUltimoValorXML(self.__serie)
            return xml_ret.encode(self.__xml_encoding)
        else:
            return self.__soap.service.getUltimoValorVO(self.__serie)

    def __soap_get_values(self, initial_date, final_date, xml=False):
        self.__soap_init()
        str_ini_date = initial_date.strftime(self.__date_format)
        str_fin_date = final_date.strftime(self.__date_format)
        if xml:
            xml_ret = self.__soap.service.getValoresSeriesXML([self.__serie],
                                                              str_ini_date,
                                                              str_fin_date)
            return xml_ret.encode(self.__xml_encoding)
        else:
            return self.__soap.service.getValoresSeriesVO([self.__serie],
                                                          str_ini_date,
                                                          str_fin_date)[0]

    def list_available_metadata(self):
        try:
            obj = self.__soap_get_last_value
            return [attr for attr in dir(obj) if not attr.startswith('__')]
        except WebFault:
            return []

    def get_metadata(self, metadata):
        try:
            obj = self.__soap_get_last_value
            return getattr(obj, metadata)
        except WebFault:
            return None

    def get_last_value(self):
        try:
            value = self.__soap_get_last_value.ultimoValor
            return date(value.ano, value.mes, value.dia), value.valor
        except WebFault:
            return None

    def get_value(self, at_date):
        try:
            return self.__soap_get_value(at_date)
        except WebFault:
            return None

    def get_values(self, initial_date, final_date):
        try:
            data = self.__soap_get_values(initial_date, final_date, xml=False)
            return {date(value.ano, value.mes, value.dia): value.valor
                        for value in data.valores}
        except WebFault:
            return {}

    def get_unique_ID(self):
        return self.__uid
