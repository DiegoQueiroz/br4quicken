# -*- coding: utf-8 -*-

from quote import Quote
from urllib import urlencode


class GF(Quote):
    '''
    Class for access funds quotations from Geração Futuro (GF).

    The company does not provide API for accessing data, so
    all information is obtained through its web site, parsing
    the web page where the date is shown.  Therefore, changes
    on the structure of the web page should crash this class.

    There is no guarantee that this class will continue to
    function case this happens, so it need constant revision
    (have a look to the last time it was updated).  However,
    it worked during years (2012 and 2013) with no need to change.

    Warning: Sometimes Geração Futuro "renames" a quote, giving a
    new ID to it.  Be aware to also rename your downloaded quotes
    case this happens.

    Geração Futuro website:
        http://www.gerafuturo.com.br/
    '''

    def __init__(self, fund_id):
        '''
        Constructor
        '''
        super(GF, self).__init__()

        self.fund_id = fund_id
        self.fund_page = 'produtos.resultado_historico_cotas'
        self.portal_url = 'https://online.gerafuturo.com.br/onlineGeracao/' \
                          'PortalManager'

    def getLastValue(self):
        # FIXME: must implement
        raise NotImplementedError()

    def getValue(self, at_date):
        # FIXME: must implement
        raise NotImplementedError()

    def getValues(self, initial_date, final_date):
        # FIXME: must implement

        # detect years based on dates

        raise NotImplementedError()

    def getUniqueID(self):
        # FIXME: must implement
        raise NotImplementedError()

    def __buildURL(self, page, params):
        # 'show' must always be the first parameter

        str_params = urlencode(params)
        return self.portal_url + '?show=' + page + '&' + str_params

    def __download_page(self, fund_id, initial_date, final_date):

        #parser = GFParser()

        params = dict()
        params['id_fundo_clube'] = str(fund_id)
        params['busca'] = 's'
        params['dataInicio'] = initial_date.strftime('%d/%m/%Y')
        params['dataFim'] = final_date.strftime('%d/%m/%Y')

        try:
            raise NotImplementedError
            #parser.getPage(self.fundpage, params)
            #prices = parser.parsePage()
            #self.prices.update(prices)

            #return True
        except NotImplementedError:
            return False
