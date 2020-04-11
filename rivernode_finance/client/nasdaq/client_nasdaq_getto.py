import sys
import os
import json
import requests
import time
import datetime





class ClientNasdaqGetto(object): #ClientBas
    def __init__(self, ):
        super(ClientNasdaqGetto, self).__init__()

    
    def get_list_price_time(self, symbol):
        url_request = 'https://api.nasdaq.com/api/quote/' + symbol +'/chart?assetclass=stocks'
        response = requests.get(url_request) 
        if response.status_code == 200:
            return self.format_response_list_price_time(response.json())               
        else:
            print(response.content)
            raise RuntimeError('not 200')

    def get_option_chain(self, symbol):

        timestamp_request = int(time.time())
        url_request = 'https://api.nasdaq.com/api/quote/' + symbol +'/option-chain?assetclass=stocks&todate=2021-04-01&fromdate=2020-04-01&limit=0'
        response = requests.get(url_request) 
        if response.status_code == 200:
            return self.format_response_option_chain(symbol, timestamp_request, response.json())               
        else:
            print(response.content)
            raise RuntimeError('not 200')


    def format_response_list_price_time(self, json_response):
        list_point = json_response['data']['chart']
        list_price_time = []

        str_response_datetime = json_response['data']['timeAsOf']
        for point in list_point:
            str_time = point['z']['dateTime']
            str_value = point['z']['value']
            price_time = {}
            price_time['timestamp'] = [0]
            price_time['timestamp'] = float(str_value)
            list_price_time.append(price_time)


    def create_option_chain(self, expiry_date):
        option_chain = {}
        option_chain['expiryDate'] = expiry_date
        option_chain['list_strike'] = []
        option_chain['list_call_bid'] = []
        option_chain['list_call_ask'] = []
        option_chain['list_call_volume'] = []
        option_chain['list_call_openinterest'] = []
        option_chain['list_call_last_trade'] = []
        option_chain['list_put_bid'] = []
        option_chain['list_put_ask'] = []
        option_chain['list_put_volume'] = []
        option_chain['list_put_openinterest'] = []
        option_chain['list_put_last_trade'] = []

        return option_chain

    def format_response_option_chain(self, symbol, timestamp_request, json_response):
        response_option_chain = {}
        response_option_chain['symbol'] = symbol
        response_option_chain['timestamp_request'] = timestamp_request
        response_option_chain['str_datetime'] = ' '.join(json_response['data']['lastTrade'].split(' ')[-4:])[:-1]
        response_option_chain['spot'] = float(json_response['data']['lastTrade'].split(' ')[2][1:])
        response_option_chain['dict_option_chain'] = {}
        for row in json_response['data']['optionChainList']['rows']:
            expiry_date = row['call']['expiryDate']
            if not expiry_date in response_option_chain['dict_option_chain']:
                option_chain = self.create_option_chain(expiry_date)
                response_option_chain['dict_option_chain'][expiry_date] = option_chain


            option_chain['list_strike'].append(float(row['call']['strike']))

            option_chain['list_call_bid'].append(self.parse_float(row, 'call', 'bid'))
            option_chain['list_call_ask'].append(self.parse_float(row, 'call', 'ask'))
            option_chain['list_call_volume'].append(self.parse_float(row, 'call', 'volume'))
            option_chain['list_call_openinterest'].append(self.parse_float(row, 'call', 'openinterest'))
            option_chain['list_call_last_trade'].append(self.parse_float(row, 'call', 'last'))

            option_chain['list_put_bid'].append(self.parse_float(row, 'put', 'bid'))
            option_chain['list_put_ask'].append(self.parse_float(row, 'put', 'ask'))
            option_chain['list_put_volume'].append(self.parse_float(row, 'put', 'volume'))
            option_chain['list_put_openinterest'].append(self.parse_float(row, 'put', 'openinterest'))
            option_chain['list_put_last_trade'].append(self.parse_float(row, 'put', 'last'))
        return response_option_chain

    def parse_float(self, row, key_0, key_1):
        str_val = row[key_0][key_1]
        if str_val == '--':
            return 0
        else:
            return float(str_val)

			# "rows": [{
			# 		"call": {
			# 			"symbol": "@NFLX  200417C00335000",
			# 			"last": "36.70",
			# 			"change": "--",
			# 			"bid": "35.55",
			# 			"ask": "38.55",
			# 			"volume": "--",
			# 			"openinterest": "494",
			# 			"strike": "335.00",
			# 			"expiryDate": "04/17/2020",
			# 			"colour": true
			# 		},
			# 		"put": {
			# 			"symbol": "@NFLX  200417P00335000",
			# 			"last": "1.80",
			# 			"change": "0.05",
			# 			"bid": "1.65",
			# 			"ask": "1.88",
			# 			"volume": "24",
			# 			"openinterest": "1335",
			# 			"strike": "335.00",
			# 			"expiryDate": "04/17/2020",
			# 			"colour": false
 
            # date_time_str = '2018-06-29 08:15:27.243860'
            # date_time_obj = datetime.datetime.strptime(date_time_str, '%Y-%m-%d %H:%M:%S.%f')

            # print('Date:', date_time_obj.date())
            # print('Time:', date_time_obj.time())
            # print('Date-time:', date_time_obj)





