import sys
import os
import time

class ToolsQuote(object): #ClientBas
    def __init__(self):
        super(ToolsQuote, self).__init__()

    @staticmethod
    def format_string(string, size):
        if size < len(string):
            raise RuntimeError('cannot format')
        else:
            for _ in range(size - len(string)):
                string = ' ' + string
        return string + ' '

    @staticmethod
    def format_number(number, size, decimals):
        if number == 0:
            return ToolsQuote.format_string('-', size)
        else:
            return ToolsQuote.format_string(format(number,'.' + str(decimals) + 'f'), size)

    @staticmethod
    def print_quote(quote):

        print(quote['symbol'] + ' - ' + quote['name_long'])
        s_price = ToolsQuote.format_string('price', 8)
        s_pte = ToolsQuote.format_string('ptp', 8)
        s_ptr = ToolsQuote.format_string('ptr', 8)
        s_int = ToolsQuote.format_string('int', 8)
        s_div = ToolsQuote.format_string('div', 8)

        print(s_price + s_pte + s_ptr + s_int + s_div)
        s_price = ToolsQuote.format_number(quote['price'], 8 , 2)
        s_pte = ToolsQuote.format_number(quote['ratio_price_to_profit'], 8 , 2)
        s_ptr = ToolsQuote.format_number(quote['ratio_price_to_revenue'], 8 , 2)
        s_int = ToolsQuote.format_number(quote['ratio_interest_to_revenue'], 8 , 2)
        s_div = ToolsQuote.format_number(quote['yield_dividend_trailing_annual'], 8 , 4)
        print(s_price + s_pte + s_ptr + s_int +  s_div)

        print(' ')
        year = ToolsQuote.format_string('year', 6)
        gain_rev = ToolsQuote.format_string('gain_rev', 10)
        gain_prof = ToolsQuote.format_string('gain_prof', 10)
        frac_prof = ToolsQuote.format_string('frac_prof', 10)
        print(year + gain_rev + gain_prof + frac_prof)  
        list_year = ['2018', '2017', '2016']
        for i in range(len(quote['list_ratio_revenue_change'])):
            year  = ToolsQuote.format_string(list_year[i], 6)
            gain_rev = ToolsQuote.format_number(quote['list_ratio_revenue_change'][i], 10, 2)
            gain_prof = ToolsQuote.format_number(quote['list_ratio_profit_change'][i], 10, 2)
            frac_prof = ToolsQuote.format_number(quote['list_ratio_profit'][i], 10, 2)
            print(year + gain_rev + gain_prof + frac_prof)
        print(' ')
        print(' ')

    @staticmethod
    def print_quote_short_header():
        s_symbol = ToolsQuote.format_string('symbol', 8)
        s_price = ToolsQuote.format_string('price', 8)
        s_pte = ToolsQuote.format_string('ptp', 8)
        s_ptr = ToolsQuote.format_string('ptr', 8)
        s_int = ToolsQuote.format_string('int', 8)
        s_div = ToolsQuote.format_string('div', 8)
        s_cou = ToolsQuote.format_string('country', 8)
        print(s_symbol + s_price + s_pte + s_ptr + s_int + s_div + s_cou)

    @staticmethod
    def print_quote_short(quote, persistency_quote):
        s_symbol = ToolsQuote.format_string(quote['symbol'], 8)
        s_price = ToolsQuote.format_number(quote['price'], 8 , 2)
        s_pte = ToolsQuote.format_number(quote['ratio_price_to_profit'], 8 , 2)
        s_ptr = ToolsQuote.format_number(quote['ratio_price_to_revenue'], 8 , 2)
        s_int = ToolsQuote.format_number(quote['ratio_interest_to_revenue'], 8 , 2)
        s_div = ToolsQuote.format_number(quote['yield_dividend_trailing_annual'], 8 , 4)
        s_cou = persistency_quote.load_tag_country_work(quote['symbol'])
        print(s_symbol + s_price + s_pte + s_ptr + s_int +  s_div, s_cou)



    @staticmethod
    def get_value_or_default(dict_lookup, list_key, default, index=0):
        if not list_key[index] in dict_lookup:
            return default
        else:
            if index == (len(list_key) - 1):
                return dict_lookup[list_key[index]]
            else:
                return ToolsQuote.get_value_or_default(dict_lookup[list_key[index]], list_key, default, index + 1)



    @staticmethod
    def format_quote(json_config):
        quote_summary_store = json_config['context']['dispatcher']['stores']['QuoteSummaryStore']
        quote_time_series_store = json_config['context']['dispatcher']['stores']['QuoteTimeSeriesStore']
            
        quote = {}
        quote['format'] = 'quote_yahoo_stripped'
        quote['symbol'] = quote_summary_store['symbol']
        quote['timestamp'] = int(time.time())
        quote['price'] = ToolsQuote.get_value_or_default(quote_summary_store, ['price','regularMarketOpen','raw'], 0)
        quote['market_capitalization'] = ToolsQuote.get_value_or_default(quote_summary_store, ['price','marketCap','raw'], 0)
        quote['count_share'] =  quote['market_capitalization'] / quote['price']
        

        quote['exchange'] = quote_summary_store['price']['exchange']
        quote['currency'] = quote_summary_store['price']['currency']
        quote['name_short'] = quote_summary_store['price']['shortName']
        quote['name_long'] = quote_summary_store['price']['longName']

        quote['yield_dividend_trailing_annual'] = ToolsQuote.get_value_or_default(quote_summary_store, ['summaryDetail', 'trailingAnnualDividendYield', 'raw'], 0)
        #TODO there is something with dilution happening here ratio_price_to_earnings
        # quote['ratio_price_to_earnings'] = self.get_value_or_default(quote_summary_store, ['summaryDetail', 'trailingPE', 'raw'], 0)
        quote['list_ratio_revenue_change'] = []
        quote['list_ratio_profit'] = []
        quote['list_ratio_profit_change'] = []
        # quote['cost_interest'] = quote_summary_store['incomeStatementHistory']['incomeStatementHistory'][0]['interestExpense']['raw']
        for i in range(len(quote_summary_store['incomeStatementHistory']['incomeStatementHistory']) - 1):
            income_statement_c = quote_summary_store['incomeStatementHistory']['incomeStatementHistory'][i]
            income_statement_l = quote_summary_store['incomeStatementHistory']['incomeStatementHistory'][i + 1]
            total_revenue_c = income_statement_c['totalRevenue']['raw']
            total_revenue_l = income_statement_l['totalRevenue']['raw']
            quote['list_ratio_revenue_change'].append(total_revenue_c / total_revenue_l)
            profit_c = income_statement_c['netIncomeApplicableToCommonShares']['raw']
            profit_l = income_statement_l['netIncomeApplicableToCommonShares']['raw']
            quote['list_ratio_profit'].append(profit_c/ total_revenue_c)
            quote['list_ratio_profit_change'].append(profit_c / profit_l)
            
        quote['profit_ttm'] = 0
        quote['revenue_ttm'] = 0
        quote['interest_ttm'] = 0
        for i in range(4):
            income_statement = quote_summary_store['incomeStatementHistoryQuarterly']['incomeStatementHistory'][i]
            quote['profit_ttm'] += ToolsQuote.get_value_or_default(income_statement, ['netIncome', 'raw'], 0)
            quote['revenue_ttm'] += ToolsQuote.get_value_or_default(income_statement, ['totalRevenue','raw'], 0)
            quote['interest_ttm'] += ToolsQuote.get_value_or_default(income_statement, ['interestExpense','raw'], 0) * -1

        quote['ratio_price_to_profit'] = quote['market_capitalization'] / quote['profit_ttm']
        quote['ratio_price_to_revenue'] = quote['market_capitalization'] / quote['revenue_ttm']
        quote['earnings_per_share'] =  quote['profit_ttm'] / quote['count_share']
        quote['ratio_interest_to_revenue'] = quote['interest_ttm'] / quote['revenue_ttm']

        # print(quote['earnings_per_share'])
        # print(quote['ratio_price_to_profit'])
        # print(quote['ratio_price_to_revenue'])
        # print(quote['ratio_interest_to_revenue'])
        # print(quote['list_ratio_revenue_change'])
        # print(quote['list_ratio_profit'])
        # print(quote['list_ratio_profit_change'])


        # quote['stat_eps'] = quote['earnings_per_share']
    
        return quote
