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

    Objects used by web service:
        WSSerieVO
         * Fields:  anoFim: integer
                    anoInicio: integer
                    aviso: Object (UNKNOWN, usually None)
                    diaFim: integer
                    diaInicio: integer
                    especial: boolean
                    fonte: string
                    fullName: string
                    gestorProprietario: string
                    mesFim: integer
                    mesInicio: integer
                    nomeAbreviado: string
                    nomeCompleto: string
                    oid: integer
                    periodicidade: string
                    periodicidadeSigla: string
                    possuiBloqueios: boolean
                    publica: boolean
                    shortName: string
                    ultimoValor: WSValorSerieVO
                    unidadePadrao: string
                    unidadePadraoIngles: string
                    valorDiaNaoUtil: boolean
                    valores: array of WSValorSerieVO

        WSValorSerieVO
         * Fields:  ano: integer
                    anoFim: integer
                    bloqueado: boolean
                    bloqueioLiberado: boolean
                    dia: integer
                    diaFim: integer
                    mes: integer
                    mesFim: integer
                    oid: integer
                    oidSerie: integer
                    svalor: string
                    valor: string
    '''

    def __init__(self, series):
        '''
        Constructor of the class.
        @param serie: Serie number to access.
        '''
        super(SGS, self).__init__()

        # SOAP constant settings
        self.__SGS_URL = 'https://www3.bcb.gov.br/sgspub/JSP/sgsgeral/' \
                         'FachadaWSSGS.wsdl'
        self.__XML_ENCODING = 'ISO-8859-1'
        self.__DATE_FORMAT = '%d/%m/%Y'

        self.__series = series
        self.__soap = None

    def __soap_init(self):
        '''
        Initializes the SOAP client if it is not already initialized.
        @return: nothing.
        @raise WebFault: if the service is unavailable for some reason.
        '''
        if not self.__soap:
            self.__soap = client.Client(self.__SGS_URL, proxy=getproxies())

    def __soap_get_value(self, at_date):
        '''
        Wrapper for "getValor" web service function that request a single
        value from a specified date.
        @return: A list of WSValorSerieVO values.  The list is guaranteed
                 to be in the same order of "series" parameter.
        @raise WebFault: if the service is unavailable for some reason.
        '''
        self.__soap_init()
        str_date = at_date.strftime(self.__DATE_FORMAT)

        return [self.__soap.service.getValor(serie, str_date)
                       for serie in self.__series]

    def __soap_get_value2(self, initial_date, final_date):
        '''
        Wrapper for "getValorEspecial" web service function that request
        the value of a interval of dates.  This function should be
        used for quotes whose each value depends of a initial and a final
        date.  It should not be confused with functions to get several quotes
        of a interval of dates (equivalent of several calls to get_value).
        @return: A list of WSValorSerieVO values. The list is guaranteed to be
                 in the same order of "series" parameter.
        @raise WebFault: if the service is unavailable for some reason.
        '''
        self.__soap_init()
        str_ini_date = initial_date.strftime(self.__DATE_FORMAT)
        str_fin_date = final_date.strftime(self.__DATE_FORMAT)

        return [self.__soap.service.getValorEspecial(serie,
                                                    str_ini_date, str_fin_date)
                                                    for serie in self.__series]

    def __soap_get_last_value(self, xml=False):
        '''
        Wrapper for "getUltimoValorVO" and "getUltimoValorXML" web service
        functions that request the last value of series (usually the most
        recent one).  The control of which function to use is determined by
        xml parameter.
        @param xml: if True, the result is a XML string instead of a
                    WSValorSerieVO object.
        @return: A list of WSValorSerieVO values or a list of XML strings.
                 The list is guaranteed to be in the same order of "series"
                 parameter.
        @raise WebFault: if the service is unavailable for some reason.
        '''
        self.__soap_init()
        if xml:
            webfunc = self.__soap.service.getUltimoValorXML
        else:
            webfunc = self.__soap.service.getUltimoValorVO

        ret_values = [webfunc(serie) for serie in self.__series]

        # Encode XML string according to its encoding
        if xml:
            ret_values = [ret_value.encode(self.__XML_ENCODING)
                            for ret_value in ret_values]

        return ret_values

    def __soap_get_values(self, initial_date, final_date, xml=False):
        '''
        Wrapper for "getValoresSeriesVO" and "getValoresSeriesXML" web service
        functions that request the values from a interval of dates.  The
        control of which function to use is determined by xml parameter.
        @param xml: if True, the result is a XML string instead of a
                    list of WSSerieVO objects.
        @return: A list of WSSerieVO objects holding all WSValorSerieVO values
                 or an XML string with the values of all series.
        @raise WebFault: if the service is unavailable for some reason.
        '''
        self.__soap_init()
        str_ini_date = initial_date.strftime(self.__DATE_FORMAT)
        str_fin_date = final_date.strftime(self.__DATE_FORMAT)
        if xml:
            webfunc = self.__soap.service.getValoresSeriesXML
        else:
            webfunc = self.__soap.service.getValoresSeriesVO

        ret_value = webfunc(self.__series, str_ini_date, str_fin_date)

        # Encode XML string according to its encoding
        if xml:
            ret_value.encode(self.__XML_ENCODING)

        return ret_value

    def get_last_value(self):
        '''
        Get last values of series.
        @return: A dictionary "ticker, date: quotation" with the last values
            or None if the service is unavailable.
        '''
        try:
            last_values = self.__soap_get_last_value(xml=False)

            # Convert array of WSSerieVO in an array of WSValorSerieVO.
            # All none "None" values are removed from the array
            last_values = [x.ultimoValor for x in last_values if x.ultimoValor]
        except WebFault:
            return list()

        return self.__build_result(last_values)

    def get_value(self, at_date):
        '''
        Get the quotation for the quotes for a specific date.
        Short call to get_values(at_date, at_date).
        @see: get_values
        '''
        return self.get_values(at_date, at_date)

    def get_values(self, initial_date, final_date):

        '''
        Get all quotations available for the quotes in a interval of
        dates.
        @return: A dictionary "ticker, date: quotation" with all values
            retrieved.
        '''
        try:
            data = self.__soap_get_values(initial_date, final_date, xml=False)

            # Flattening WSValorSerieVO array inside WSSerieVO in a single
            # list of WSValorSerieVO (that is, joining all series together)
            data = [entry for serie in data for entry in serie.valores]
        except WebFault:
            return list()

        return self.__build_result(data)

    def __tryfloat(self, num):
        '''
        Try to convert a variable to float.
        @param num: The number to be converted (usually a string).
        @return: The converted variable or None cause the conversion fails.
        '''
        try:
            return float(num)
        except TypeError:
            return None

    def __build_result(self, data):
        '''
        Build the result dictionary.
        @param data: List of WSValorSerieVO.
        @return: Dict in the form "ticker, date: quotation"
        '''
        quote_names = [self.build_ID(entry.oidSerie)
                   for entry in data]
        quote_dates = [date(entry.ano, entry.mes, entry.dia)
                       for entry in data]
        quote_values = [self.__tryfloat(entry.valor)
                        for entry in data]

        return dict(zip(zip(quote_names, quote_dates), quote_values))
