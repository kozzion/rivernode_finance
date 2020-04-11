import sys
import os
import json
import requests
import time

class ClientTopforeignstocks(object):
    def __init__(self, persistency_qoute):
        super(ClientTopforeignstocks, self).__init__()
        self.persistency_qoute = persistency_qoute
        self.root_adr = 'https://topforeignstocks.com/foreign-adrs-list/'
        self.root_indices = 'https://topforeignstocks.com/indices/'

    def test(self):
        if os.path.isfile('temp_list'):
            with open('temp_list', 'rb') as file:
                bytearray_response = file.read() 
        else:
            response = requests.get(self.root_adr) 
            if response.status_code == 200:
                bytearray_response = response.content
                with open('temp_list', 'wb') as file:
                    file.write(bytearray_response) 
            else:
                string_response = response.content.decode("utf-8", errors='ignore')
                print(string_response)
                raise RuntimeError('not 200')

        list_tag_country, list_url_ard = self.format_response_root_adr(bytearray_response) 
        for tag_country, url in zip(list_tag_country, list_url_ard):
            self.scrape_country_adr(tag_country, url)

    def scrape_country_adr(self, tag_country, url):          

        response = requests.get(url) 
        if response.status_code == 200:
            bytearray_response = response.content
            # with open('temp_count', 'wb') as file:
            #     file.write(bytearray_response) 
            self.handle_response_country_adr(tag_country, bytearray_response)     
        else:
            string_response = response.content.decode("utf-8", errors='ignore')
            print(string_response)
            raise RuntimeError('not 200')



    def format_response_root_adr(self, bytearray_response):
        string_response = bytearray_response.decode("utf-8", errors='ignore')
        index_from = 0
        list_tag_country = []
        list_url_ard = []
        # table_row, index_from = self.find_string_from(string_response, 'gfdhdfgh', 'gdhfghf', index_from)
        while True:
            table_row, index_from = self.find_string_from(string_response, '<td ', '</td>', index_from)
            if index_from == -1:
                break
            if 'https://topforeignstocks.com/foreign-adrs-list/' in table_row:
                url, index_next = self.find_string_from(table_row, '<a href="', '"', 0)
                country, index_next = self.find_string_from(table_row, '>', '<', index_next)
                country = 'country_work_' + country.split(' ')[0].lower()
                # table_row = find_string_from
                list_url_ard.append(url)
                list_tag_country.append(country)
        return list_tag_country, list_url_ard



    def handle_response_country_adr(self, tag_country, bytearray_response):
        string_response = bytearray_response.decode("utf-8", errors='ignore')
        string_response, index_from = self.find_string_from(string_response, 'trading on the US Exchanges', 'trading on the US OTC', 0)
        
        
        index_from = 0
        while True:
            table_row, index_from = self.find_string_from(string_response, '<tr ', '</tr>', index_from)
            if index_from == -1:
                break

            index_next = 0
            name, index_next = self.find_string_from(table_row, '"column-2">', '</td>', index_next)
            # print(name)
            url_yahoo, index_next = self.find_string_from(table_row, '<a href="', '"', index_next)
            ticker, index_next = self.find_string_from(table_row, '>', '<', index_next)
            industry, index_next = self.find_string_from(table_row, '"column-4">', '<', index_next)
            if ticker:
                list_tag = [tag_country]
                if industry:
                    tag_industry = 'industry_' + industry
                    list_tag.append(tag_industry)
                print(ticker)
                self.persistency_qoute.add_list_tag(ticker, list_tag)
                self.persistency_qoute.add_url_yahoo(ticker, url_yahoo)


    def find_string(self, text, string_from, string_to):
        index_from = text.find(string_from) + len(string_from)
        index_to = text.find(string_to, index_from)
        # print(index_from)
        # print(index_to)
        return text[index_from:index_to]

    def find_string_from(self, text, string_from, string_to, index_from):
        index_from = text.find(string_from, index_from)
        if index_from == -1:
            return None, -1
        index_to = text.find(string_to, index_from + len(string_from))
        if index_to == -1:
            return None, -1
        return text[index_from + len(string_from):index_to], index_to + len(string_to)