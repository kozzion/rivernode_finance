import sys
import os
import json
import requests
import time

from rivernode_finance.tools_quote import ToolsQuote
class ClientYahoo(object): #ClientBas
    def __init__(self, ):
        super(ClientYahoo, self).__init__()

    
    def test(self):
        url_request = 'https://finance.yahoo.com/quote/NFLX/cash-flow?p=NFLX'
        # https://finance.yahoo.com/quote/NFLX/financials?p=NFLX
        response = requests.get(url_request) 
        if response.status_code == 200:

            with open('temp', 'wb') as file:
                file.write(response.content)
    
            string_from = 'root.App.main = '
            string_to = ';\n}(this));'
            string_content = response.content.decode("utf-8", errors='ignore')
            string_config = self.find_string(string_content, string_from, string_to)

            json_config = json.loads(string_config)
            
            with open('temp.json', 'w') as file:
                json.dump(json_config, file)
            

            return self.format_quote(json_config)
        else:
            raise RuntimeError('not 200')
    

    def load_quote_for_symbol(self, symbol):

        url_request = 'https://finance.yahoo.com/quote/' + symbol +'/cash-flow?p=' + symbol
        # url_request = 'https://finance.yahoo.com/quote/' + symbol + '?p=' + symbol + '&.tsrc=fin-srch'
        response = requests.get(url_request) 
        if response.status_code == 200:
            with open('temp', 'wb') as file:
                file.write(response.content)
    
            string_from = 'root.App.main = '
            string_to = ';\n}(this));'
            string_content = response.content.decode("utf-8", errors='ignore')
            string_config = self.find_string(string_content, string_from, string_to)

            json_config = json.loads(string_config)
            return ToolsQuote.format_quote(json_config)
        else:
            raise RuntimeError('not 200')

    def find_string(self, text, string_from, string_to):
        index_from = text.find(string_from) + len(string_from)
        index_to = text.find(string_to, index_from)
        # print(index_from)
        # print(index_to)
        return text[index_from:index_to]