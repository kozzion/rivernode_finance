import sys
import os
import json
import datetime
import pytz
import numpy as np
class SeriesOptionChain(object):

    def __init__(self):
        super(SeriesOptionChain, self).__init__()

    @staticmethod
    def to_unit(series_option_chain):

        series_option_chain_unit = {}
        spot =  series_option_chain['spot']
        series_option_chain_unit['symbol'] = series_option_chain['symbol']
        series_option_chain_unit['spot'] = spot
        series_option_chain_unit['str_datetime'] = series_option_chain['str_datetime']
        series_option_chain_unit['timestamp_request'] = series_option_chain['timestamp_request']
        series_option_chain_unit['list_option_chain'] = []
        for option_chain in list(series_option_chain['dict_option_chain'].values()): 
            option_chain_unit = {}
            option_chain_unit['is_normalized'] = True
            option_chain_unit['symbol'] = series_option_chain_unit['symbol']
            option_chain_unit['spot'] = spot
            month = int(option_chain['expiryDate'].split('/')[0])
            day = int(option_chain['expiryDate'].split('/')[1])
            year = int(option_chain['expiryDate'].split('/')[2])
            option_chain_unit['timestamp_expiry'] =  int(datetime.datetime(year, month, day, tzinfo=pytz.timezone('US/Eastern')).timestamp())
            option_chain_unit['list_strike'] = SeriesOptionChain.minus_divide(option_chain['list_strike'], spot)

            option_chain_unit['list_call_bid'] = SeriesOptionChain.divide(option_chain['list_call_bid'], spot)
            option_chain_unit['list_call_ask'] = SeriesOptionChain.divide(option_chain['list_call_ask'], spot)
            option_chain_unit['list_call_volume'] = option_chain['list_call_volume']
            option_chain_unit['list_call_openinterest'] = option_chain['list_call_openinterest']
            option_chain_unit['list_call_last_trade'] = option_chain['list_call_last_trade']
            option_chain_unit['list_put_bid'] = SeriesOptionChain.divide(option_chain['list_put_bid'], spot)
            option_chain_unit['list_put_ask'] = SeriesOptionChain.divide(option_chain['list_put_ask'], spot)
            option_chain_unit['list_put_volume'] = option_chain['list_put_volume']
            option_chain_unit['list_put_openinterest'] = option_chain['list_put_openinterest']
            option_chain_unit['list_put_last_trade'] = option_chain['list_put_last_trade']
            series_option_chain_unit['list_option_chain'].append(option_chain_unit)
        return series_option_chain_unit

    @staticmethod
    def minus_divide(list_value, parameter):
        list_result = []
        for value in list_value:
            list_result.append((value - parameter) / parameter)
        return list_result

    @staticmethod
    def divide(list_value, parameter):
        list_result = []
        for value in list_value:
            list_result.append(value / parameter)
        return list_result