import sys
import os
import json
import hashlib


sys.path.append(os.path.abspath('../../rivernode_core'))
from rivernode_core.system_config import SystemConfig
from rivernode_core.persistency.table_object_loader_disk import TableObjectLoaderDisk

sys.path.append(os.path.abspath('../../rivernode_finance'))
from rivernode_finance.client_yahoo import ClientYahoo 
from rivernode_finance.persistency_quote import PersistencyQuote
from rivernode_finance.tools_quote import ToolsQuote

client_yahoo = ClientYahoo()
system_config = SystemConfig()
loader_table = TableObjectLoaderDisk(system_config.load_path_dir_database())
pq = PersistencyQuote(loader_table.load_table_for_list_key(['trading']))
# list_symbol = pq.load_list_symbol()

# do_short = False

# def reject(quote):
#     ratio_profit = (quote['list_ratio_profit'][0] + quote['list_ratio_profit'][1] + quote['list_ratio_profit'][2]) / 3
#     if ratio_profit < 0.05:
#         return True

#     gain_rev = (quote['list_ratio_revenue_change'][0] + quote['list_ratio_revenue_change'][1] + quote['list_ratio_revenue_change'][2]) / 3
#     if gain_rev < 1.1:
#         return True

#     if 0.1 < quote['ratio_interest_to_revenue']:
#         return True
#     return False
    


# if do_short:
# #     ToolsQuote.print_quote_short_header()

# for symbol in list_symbol:
#     ticker = symbol['ticker']
#     if pq.has_quote(ticker):
#         quote = pq.load_quote(ticker)
#         if not reject(quote):
#             ToolsQuote.print_quote(quote)


#   https://scikit-learn.org/stable/modules/generated/sklearn.preprocessing.QuantileTransformer.html#

list_symbol = pq.load_list_symbol()
print(len(list_symbol))

count_fail = 0
for symbol in list_symbol:
    ticker = symbol['ticker']
    # if pq.has_quote(ticker):
    #     quote = pq.load_quote(ticker)
    # else:
    try:
        quote = client_yahoo.load_quote_for_symbol(ticker)
        pq.save_quote(ticker, quote)
        ToolsQuote.print_quote(quote)
        sys.stdout.flush()
        count_fail = 0
    except Exception:
        count_fail += 1
        pass
