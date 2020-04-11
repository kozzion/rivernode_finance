import sys
import os
import json
import csv
import datetime
from datetime import datetime
from datetime import timezone

sys.path.append(os.path.abspath('../../rivernode_finance'))
from rivernode_finance.tools_plot_finance import ToolsPlotFinance as tp
from rivernode_finance.tools_asset import ToolsAsset as ta


def load_dict_price(path_file_portefolio):
    dict_price = {}
    with open(path_file_portefolio) as csv_file:
        #Product,Symbool/ISIN,Aantal,Slotkoers,Lokale waarde,Waarde in EUR
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                pass
                line_count += 1
            else:
                asset_id = row[1]
                if 'CASH' in row[0]:
                    continue
                price = float(row[5].replace(',','.')) / float(row[2].replace(',','.'))
                print(asset_id)
                print(price)
                dict_price[asset_id] = price
                line_count += 1
    return dict_price


def load_list_transaction(path_file_transactions):
    list_transaction = []
    with open(path_file_transactions) as csv_file:
        #Datum,Tijd,Product,ISIN,Exchange,Aantal5,,Koers,,Lokale waarde,,Waarde11 ,Wisselkoers,,Kosten,,Totaal,Order Id
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                pass
                line_count += 1
            else:
                transaction = {}
                transaction['date'] = row[0]
                transaction['time'] = row[1]
                # transaction['datetime'] = datetime.strptime(row[0], '%d-%m-%Y')
                transaction['datetime'] = datetime.strptime(row[0] + ' ' + row[1], '%d-%m-%Y %H:%M')

                transaction['timestamp'] = int(transaction['datetime'].replace(tzinfo=timezone.utc).timestamp())

                transaction['product'] = row[2]
                transaction['id_asset'] = 'isin_' + row[3]
                transaction['exchange'] = row[4]
                transaction['volume'] = float(row[5])

                transaction['price_0'] = row[6]
                transaction['price_1'] = row[7]
                
                transaction['price_2'] = row[8]
                transaction['price_3'] = row[9]
                
                transaction['price_4'] = row[10]
                transaction['price_5'] = row[11]

                transaction['exchange_rate'] = row[12]

                transaction['cost_0'] = row[13]
                transaction['cost_1'] = row[14]

                transaction['change_money_symbol'] = row[15]
                transaction['change_money_value'] = float(row[16])
                list_transaction.append(transaction)
                line_count += 1
    return list_transaction



path_file_transactions = 'transactions.csv'
path_file_portefolio = 'portfolio.csv'
value_money_start = 40000
list_transaction = load_list_transaction(path_file_transactions)
dict_price = load_dict_price(path_file_portefolio)

tp.plot_return(list_transaction, value_money_start, )

# for transaction in list_transaction:
#     # print(transaction['total_value_0'])
#     print( transaction['datetime'])
#     print( transaction['timestamp'])
#     exit()
#     print(transaction['total_number'])

# datetime_str = '09/19/18 13:55:26'
# datetime_object = datetime.strptime(datetime_str, '%m-%d-%y %H:%M)

# print(type(datetime_object))
# print(datetime_object)

# get portefolio
# tt.get_portefolio(list_transaction)