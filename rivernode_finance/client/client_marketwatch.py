import sys
import os
import json
import requests
import time

class ClientMarketwatch(object): #ClientBas
    def __init__(self, ):
        super(ClientMarketwatch, self).__init__()

    
    def scape_symbol(self, persistency_qoute):

        # <td class="name"><a href="/investing/Stock/KPLUY?countryCode=US">K+S AG ADR <small>(KPLUY)</small></a></td>
        # <td>United States</td>
        # <td>OOTC</td>
        # <td>Specialty Chemicals</td>

        list_page_letter = ['0-9']
        list_page_letter.extend([str(char) for char in 'TUVWXYZ'])
        list_page_index = [str(char) for char in '1234']
        # list_page_letter.extend([str(char) for char in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'])
        # list_page_index = [str(char) for char in '123456789']

        for page_letter in list_page_letter:
            for page_index in list_page_index:
                url_request = 'https://www.marketwatch.com/tools/markets/american-depository-receipt-stocks/a-z/' + page_letter + '/' + page_index
                response = requests.get(url_request) 
                if response.status_code == 200:
                    # with open('temp', 'wb') as file:
                    #     file.write(response.content)
     
                    self.format_response(response.content, persistency_qoute)               
                    # with open('temp.json', 'w') as file:
                    #     json.dump(json_config, file)
                    

                    # return self.format_quote(json_config)
                else:
                    print(response.content)
                    raise RuntimeError('not 200')
                
    def format_response(self, bytearray_response, persistency_qoute):
        string_response = bytearray_response.decode("utf-8", errors='ignore')
        string_from = '<table class="table table-condensed">'
        string_to = '</table>'
        string_table = self.find_string(string_response, string_from, string_to)
        list_string_table_row = ['<tr>' +tp for tp in string_table.split('<tr>')][2:]
        for string_table_row in list_string_table_row:
            self.format_table_row(string_table_row, persistency_qoute)
        

    def format_table_row(self, string_table_row, persistency_qoute):
        string_row_0, index_from = self.find_string_from(string_table_row, '<td ', '</td>', 0)
        string_row_1, index_from = self.find_string_from(string_table_row, '<td>', '</td>', index_from)
        string_row_2, index_from = self.find_string_from(string_table_row, '<td>', '</td>', index_from)
        string_row_3, _ = self.find_string_from(string_table_row, '<td>', '</td>', index_from)
        ticker = self.find_string(string_row_0, '<small>(', ')</small>')
        tag_country_trade = 'country_trade_' + self.find_string(string_row_0, 'countryCode=', '">').lower()
        tag_exchange = 'exchange_'  + string_row_2.lower()
        tag_sector = 'sector_'  + string_row_3.lower().replace(' ', '_')
        persistency_qoute.add_list_tag(ticker, [tag_country_trade, tag_exchange, tag_sector, 'is_ard'])
# PersistencyQoute
        
    def find_string(self, text, string_from, string_to):
        index_from = text.find(string_from) + len(string_from)
        index_to = text.find(string_to, index_from)
        # print(index_from)
        # print(index_to)
        return text[index_from:index_to]

    def find_string_from(self, text, string_from, string_to, index_from):
        index_from = text.find(string_from, index_from) + len(string_from)
        index_to = text.find(string_to, index_from)
        # print(index_from)
        # print(index_to)
        return text[index_from:index_to], index_to