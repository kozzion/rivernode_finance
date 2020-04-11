import sys
import os
import time
import copy

import matplotlib.pyplot as plt

class ToolsAsset(object):
    def __init__(self):
        super(ToolsAsset, self).__init__()

    @staticmethod
    def asset_create(id_asset):
        asset = {}
        asset['id_asset'] = id_asset
        asset['volume'] = 0
        # asset['total_purchase_price'] = 0
        # asset['current_unit_value'] = 0
        asset['current_unit_value'] = 0
        return asset
        
    @staticmethod
    def asset_transaction(asset, transaction):
        if not asset['id_asset'] == transaction['id_asset']:
            raise RuntimeError('id_asset_mismatch')
        asset_value_before = asset['volume'] * asset['current_unit_value']
    

        asset['current_unit_value'] = -transaction['change_money_value'] / transaction['volume']
        asset['volume'] += transaction['volume']
        asset_value_after = asset['volume'] * asset['current_unit_value']
        change_asset_value = asset_value_after - asset_value_before


        # print(transaction['change_money_value'])
        # print(asset['current_unit_value'])
        # print(asset['volume'])
        # print(change_asset_value)
        # exit()
        return transaction['change_money_value'], change_asset_value

    # @staticmethod
    # def asset_purchace(asset, transaction):
    #     if not asset['id_asset'] == transaction['id_asset']:
    #         raise RuntimeError('id_asset_mismatch')

    #     return change_value_currency, change_value_asset

    # @staticmethod
    # def asset_sell(asset, transaction):
    #     if not asset['id_asset'] == transaction['id_asset']:
    #         raise RuntimeError('id_asset_mismatch')
    #     asset['volume'] += transaction['volume']
    #     value_profit = transaction['total_number'] - (transaction['volume'] *  asset['average_purchase_price'])
    #     # rate_return = (transaction['volume'] *  asset['average_purchase_price'])
    #     return value_profit#, rate_return

    @staticmethod
    def portefolio_compute_value(dict_asset, dict_price=None):
        value = 0
        if dict_price:
            for id_asset, asset in dict_asset.items():
                value +=  asset['volume'] * dict_price[id_asset]
        else:
            for asset in dict_asset.values():
                 value += asset['volume'] * asset['current_unit_value']
        return value



    # @staticmethod
    # def compute_series_value(list_transaction):
    #     list_x = []
    #     list_y = []
    #     value = 0
    #     # sort by timestamp
    #     list_transaction = sorted(list_transaction, key=lambda x: x['timestamp'], reverse=False)
    #     for transaction in list_transaction:
    #         list_x.append(transaction['timestamp'] - 1)
    #         list_y.append(value)
    #         value -= float(transaction['change_money_number'])
    #         list_x.append(transaction['timestamp'])
    #         list_y.append(value)
    #         #TODO redo this with assets

    #         # print(transaction['timestamp'])

    #     return list_x, list_y



    @staticmethod
    def compute_series_value(list_transaction, value_money_start=40000, dict_asset_start={},  timestamp_start= None, timestamp_end=None, dict_price_end=None):
        # sort by timestamp
        list_transaction = sorted(list_transaction, key=lambda x: x['timestamp'], reverse=False)

        if not timestamp_start:
            timestamp_start = list_transaction[0]['timestamp']
        if not timestamp_end:
            timestamp_end = list_transaction[-1]['timestamp']

        series_money = {'x':[], 'y':[]}
        series_asset = {'x':[], 'y':[]}
        series_total = {'x':[], 'y':[]}
        
        # prepare asset dict    
        dict_asset = copy.deepcopy(dict_asset_start)
        for transaction in list_transaction:
            if transaction['id_asset'] not in dict_asset:
                dict_asset[transaction['id_asset']] = ToolsAsset.asset_create(transaction['id_asset'])


        value_money = value_money_start
        value_asset = ToolsAsset.portefolio_compute_value(dict_asset)
        value_total = value_money + value_asset

        timestamp = timestamp_start
        series_money['x'].append(timestamp)
        series_money['y'].append(value_money)
        series_asset['x'].append(timestamp)
        series_asset['y'].append(value_asset)
        series_total['x'].append(timestamp)
        series_total['y'].append(value_total)

        for transaction in list_transaction:
            if transaction['timestamp'] < timestamp_start:
                continue
            if timestamp_end < transaction['timestamp']:
                break
            change_money_value, change_asset_value = ToolsAsset.asset_transaction(dict_asset[transaction['id_asset']], transaction)
            value_money += change_money_value
            value_asset += change_asset_value
            value_total = value_money + value_asset

            timestamp = transaction['timestamp']
            series_money['x'].append(timestamp)
            series_money['y'].append(value_money)
            series_asset['x'].append(timestamp)
            series_asset['y'].append(value_asset)
            series_total['x'].append(timestamp)
            series_total['y'].append(value_total)

            # print(transaction['timestamp'])
        if dict_price_end:
            value_asset = ToolsAsset.portefolio_compute_value(dict_asset, dict_price_end)
            value_total = value_money + value_asset

        timestamp = timestamp_end
        series_money['x'].append(timestamp)
        series_money['y'].append(value_money)
        series_asset['x'].append(timestamp)
        series_asset['y'].append(value_asset)
        series_total['x'].append(timestamp)
        series_total['y'].append(value_total)

        return series_money, series_asset, series_total
