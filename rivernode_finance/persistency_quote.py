import time
import hashlib

from rivernode_finance.tools_quote import ToolsQuote

class PersistencyQuote(object):

    def __init__(self, table_trading):
        super(PersistencyQuote, self).__init__()
        self.table_symbol = table_trading.load_table_for_list_key(['symbol'])
        self.table_quote = table_trading.load_table_for_list_key(['qoute'])
        self.table_raw_yahoo = table_trading.load_table_for_list_key(['raw_yahoo'])
        
        if self.table_symbol.has_object_for_key('dict_symbol'):
            self.dict_symbol = self.table_symbol.load_json_for_key('dict_symbol')
        else:
            self.dict_symbol = {}
        # self.add_symbol_default()
        
    def load_list_tag_contains(self, contains):
        list_tag = []
        list_symbol = self.load_list_symbol()
        for symbol in list_symbol:
            for tag in symbol['list_tag']:
                if contains in tag:
                    if tag not in list_tag:
                        list_tag.append(tag)
        return list_tag

    def delete_tag(self, tag):
        list_symbol = self.load_list_symbol()
        for symbol in list_symbol:
            if tag in symbol['list_tag']:
                symbol['list_tag'].remove(tag)
                self.save_symbol(symbol['ticker'], symbol)

    def replace_tag(self, tag_find, tag_replace):
        list_symbol = self.load_list_symbol()
        for symbol in list_symbol:
            if tag_find in symbol['list_tag']:
                symbol['list_tag'].remove(tag_find)
                symbol['list_tag'].append(tag_replace)
                self.save_symbol(symbol['ticker'], symbol)

    def load_list_tag_exchange(self):
        return self.load_list_tag_contains('exchange')

    def load_list_tag_country(self):
        return self.load_list_tag_contains('country')

    def load_tag_country_work(self, ticker):
        if not ticker in self.dict_symbol:
            return '????'
        else:
            symbol = self.dict_symbol[ticker]
            for tag in symbol['list_tag']:
                if 'country_work' in tag:
                    return tag

    def load_list_tag_sector(self):
        return self.load_list_tag_contains('sector')

    def load_list_symbol(self):
        return list(self.dict_symbol.values())

    def has_list_tag(self, symbol, list_tag):
        for tag in list_tag:
            if tag not in symbol['list_tag']:
                return False
        return True

    def load_list_symbol_for_tag_all(self, list_tag):
        list_symbol = self.load_list_symbol()
        list_symbol_selected = []
        for symbol in list_symbol:
            if self.has_list_tag(symbol, list_tag):
                list_symbol_selected.append(symbol)
        return list_symbol_selected
    
    def load_list_symbol_for_tag_any(self, list_tag):
        list_symbol = self.load_list_symbol()
        list_symbol_selected = []
        for symbol in list_symbol:
            for tag in symbol['list_tag']:
                if tag in list_tag:
                    list_symbol_selected.append(symbol)
                    break
        return list_symbol_selected

    def has_symbol(self, ticker):
        return ticker in self.dict_symbol

    def save_symbol(self, ticker, symbol):
        self.dict_symbol[ticker] = symbol
        self.table_symbol.save_json_for_key('dict_symbol', self.dict_symbol)

    def load_symbol(self, ticker):
        if ticker in self.dict_symbol:
            return self.dict_symbol[ticker]
        else:
            raise RuntimeError()
        # path_file_quote = os.path.join('quote', name_hash + '.json')

    
    def add_list_tag(self, ticker, list_tag):
        if self.has_symbol(ticker):
            symbol = self.load_symbol(ticker)
        else:
            symbol = {'ticker':ticker, 'list_tag':[]}
        for tag in list_tag:
            if tag not in symbol['list_tag']:
                symbol['list_tag'].append(tag)
        symbol['list_tag'] = sorted(symbol['list_tag'])
        self.save_symbol(ticker, symbol)

    def add_url_yahoo(self, ticker, url_yahoo):
        if self.has_symbol(ticker):
            symbol = self.load_symbol(ticker)
        else:
            symbol = {'ticker':ticker, 'list_tag':[]}
        symbol['url_yahoo'] = url_yahoo
        self.save_symbol(ticker, symbol)

    def add_tag_default(self):
        list_ticker_co = []
        list_ticker_co.append('AVH')
        list_ticker_co.append('CIB')
        list_ticker_co.append('EC')
        list_ticker_co.append('AVAL')
        list_ticker_co.append('TGLS')
        for ticker in list_ticker_co:
            self.add_list_tag(ticker, ['country_work_co'])

        list_ticker_pe = []
        list_ticker_pe.append('CPAC') # Bank
        list_ticker_pe.append('BVN') # Bank
        list_ticker_pe.append('BAP') # eCommerce
        list_ticker_pe.append('GRAM') # Electricity
        for ticker in list_ticker_pe:
            self.add_list_tag(ticker, ['country_work_pe'])

        list_ticker_ar = []
        list_ticker_ar.append('BMA') # Bank
        list_ticker_ar.append('GGAL') # Bank
        list_ticker_ar.append('MELI') # eCommerce
        list_ticker_ar.append('CEPU') # Electricity
        list_ticker_ar.append('EDN') # Electricity
        list_ticker_ar.append('PAM') # Electricity
        list_ticker_ar.append('SUPV') # Financial Services
        list_ticker_ar.append('CRESY') # Food Producers
        list_ticker_ar.append('LOMA') # General Industrials
        list_ticker_ar.append('TS') # Indust.Metals&Mining
        list_ticker_ar.append('TX') # Indust.Metals&Mining
        list_ticker_ar.append('TEO') # Mobile Telecom.
        list_ticker_ar.append('TGS') # Oil
        list_ticker_ar.append('YPF') # oil
        list_ticker_ar.append('IRS') # Mobile Telecom.
        list_ticker_ar.append('IRCP') # Mobile Telecom.
        for ticker in list_ticker_ar:
            self.add_list_tag(ticker, ['country_work_ar'])

        list_ticker_cl = []
        list_ticker_cl.append('BCH')
        list_ticker_cl.append('BSAC')
        list_ticker_cl.append('CCU')
        list_ticker_cl.append('AKO-A')
        list_ticker_cl.append('AKO-B')
        list_ticker_cl.append('EOCCY')
        list_ticker_cl.append('ENIA')
        list_ticker_cl.append('ENIC')
        list_ticker_cl.append('ITCB') 
        list_ticker_cl.append('LFL.F')
        list_ticker_cl.append('SQM')
        for ticker in list_ticker_cl:
            self.add_list_tag(ticker, ['country_work_cl'])

        list_ticker_br = []
        list_ticker_br.append('ABEV')
        list_ticker_br.append('AZUL')
        list_ticker_br.append('BBD')
        list_ticker_br.append('BBDO')
        list_ticker_br.append('BSBR')
        list_ticker_br.append('LND')
        list_ticker_br.append('BRFS')
        list_ticker_br.append('EBR')
        list_ticker_br.append('ELP')
        list_ticker_br.append('CBD')
        list_ticker_br.append('CIG')
        list_ticker_br.append('SID')
        list_ticker_br.append('CPL')
        list_ticker_br.append('ERJ')
        list_ticker_br.append('FBR.AX')
        # list_ticker_br.append('GFAFX')
        list_ticker_br.append('GGB')
        list_ticker_br.append('GOL')
        list_ticker_br.append('ITUB')
        list_ticker_br.append('LINX')
        # list_ticker_br.append('OIBR')
        list_ticker_br.append('PBR')
        list_ticker_br.append('SBS')
        list_ticker_br.append('SUZ')
        list_ticker_br.append('VIV')
        list_ticker_br.append('TSU')
        list_ticker_br.append('UGP')
        list_ticker_br.append('VALE')
        for ticker in list_ticker_br:
            self.add_list_tag(ticker, ['country_work_br'])

    def extend_list(self, list_symbol, list_tag):
        pass




    def save_quote(self, ticker, qoute):
        key_quote = hashlib.sha256(ticker.encode('utf-8')).hexdigest()  
        self.table_quote.save_json_for_list_key([key_quote], qoute)

    def has_quote(self, ticker):
        key_quote = hashlib.sha256(ticker.encode('utf-8')).hexdigest()  
        return self.table_quote.has_object_for_list_key([key_quote])

    def load_quote(self, ticker):
        key_quote = hashlib.sha256(ticker.encode('utf-8')).hexdigest()
        return self.table_quote.load_json_for_list_key([key_quote])




    def save_raw_yahoo(self, ticker, json_object):
        key_quote = hashlib.sha256(ticker.encode('utf-8')).hexdigest()  
        self.table_raw_yahoo.save_json_for_list_key([key_quote], json_object)

    def has_raw_yahoo(self, ticker):
        key_quote = hashlib.sha256(ticker.encode('utf-8')).hexdigest()  
        return self.table_raw_yahoo.has_object_for_list_key([key_quote])

    def load_raw_yahoo(self, ticker):
        key_quote = hashlib.sha256(ticker.encode('utf-8')).hexdigest()
        return self.table_raw_yahoo.load_json_for_list_key([key_quote])



    # def save_price_day(self, asset_id, list_price_day):
    #     key_quote = hashlib.sha256(asset_id.encode('utf-8')).hexdigest()  
    #     self.table_price_day.save_json_for_list_key([key_quote], json_object)

    # def has_raw_yahoo(self, ticker):
    #     key_quote = hashlib.sha256(ticker.encode('utf-8')).hexdigest()  
    #     return self.table_raw_yahoo.has_object_for_list_key([key_quote])

    # def load_raw_yahoo(self, ticker):
    #     key_quote = hashlib.sha256(ticker.encode('utf-8')).hexdigest()
    #     return self.table_raw_yahoo.load_json_for_list_key([key_quote])



    def reformat_quotes(self):
        list_key = self.table_raw_yahoo.load_list_key()
        for key in list_key:
            raw_yahoo = self.table_quote.load_json_for_key(key)
            quote = ToolsQuote.format_quote(raw_yahoo)
            self.table_quote.save_json_for_key(key, quote)



# Tech symbols
# list_symbol.append('NFLX')
# list_symbol.append('AMZN')
# list_symbol.append('GOOGL')
# list_symbol.append('FB')
# list_symbol.append('AMD')

# list_symbol.append('MSFT')

# list_symbol.append('NVDA')
# list_symbol.append('AAPL')


# Motor companies
# list_symbol.append('TSLA')
# list_symbol.append('GM')
# list_symbol.append('FCAU')
# list_symbol.append('TM')
# list_symbol.append('RACE')


# Education symbols
# list_symbol.append('BFAM')
 
# Vopak
# list_symbol.append('VPK.AS')

# list_symbol.append('CSCO')
# list_symbol.append('CUBE')
# list_symbol.append('MCD')
# list_symbol.append('JNJ')


# # lithium miners
# list_symbol.append('SQM')
# list_symbol.append('ALB')
# list_symbol.append('FMC')


# list_symbol.append('LINX') # sector_tech 
# list_symbol.append('VALE') # sector_mining
# list_symbol.append('SBS') # sector_utility