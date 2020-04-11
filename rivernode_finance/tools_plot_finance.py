import sys
import os
import time
import matplotlib.pyplot as plt
from rivernode_finance.tools_asset import ToolsAsset as ta


class ToolsPlotFinance(object):
    def __init__(self):
        super(ToolsPlotFinance, self).__init__()

    @staticmethod
    def plot_return(list_transaction, value_money_start, dict_price):
        series_money, series_assets, series_total = ta.compute_series_value(list_transaction, value_money_start=value_money_start)

        # for transaction in list_transaction:
        #     print(transaction['total_number'])


        plt.figure()
        plt.subplot(2, 2, 1)
        plt.title('value')
        plt.plot(series_money['x'], series_money['y'])
        plt.plot(series_assets['x'], series_assets['y'])
        plt.plot(series_total['x'], series_total['y'])

        series_return = {'x':[], 'y':[]}
        for i in range(len(series_total['x'])):
            series_return['x'].append(series_total['x'][i])
            series_return['y'].append(series_total['y'][i] / value_money_start)

        plt.subplot(2, 2, 2)
        plt.title('return')
        plt.plot(series_return['x'], series_return['y'])

        # plt.subplot(2, 2, 3)
        # plt.plot(x, y)

        # plt.subplot(2, 2, 4)
        # plt.plot(x, y)

        # plt.line(list_x, list_y)
        
        plt.show()
