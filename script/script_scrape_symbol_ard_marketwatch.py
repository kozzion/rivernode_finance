import sys
import os
import json
import hashlib


sys.path.append(os.path.abspath('../../rivernode_core'))
from rivernode_core.system_config import SystemConfig
from rivernode_core.persistency.table_object_loader_disk import TableObjectLoaderDisk

sys.path.append(os.path.abspath('../../rivernode_finance'))
from rivernode_finance.client_marketwatch import ClientMarketwatch
from rivernode_finance.persistency_quote import PersistencyQuote

system_config = SystemConfig()
loader_table = TableObjectLoaderDisk(system_config.load_path_dir_database())
pq = PersistencyQuote(loader_table.load_table_for_list_key(['trading']))
client = ClientMarketwatch()

## scrape
# client.scape_symbol(pq)  

## clean up
# pq.delete_tag('sector_')
# pq.replace_tag('country_trade_de&amp;iso=xber', 'country_trade_de')
# pq.replace_tag('country_trade_de&amp;iso=xfra', 'country_trade_de')
# pq.replace_tag('country_trade_de&amp;iso=xstu', 'country_trade_de')
# pq.replace_tag('country_trade_de&amp;iso=xdus', 'country_trade_de')
# pq.replace_tag('country_trade_de&amp;iso=xham', 'country_trade_de')
# pq.replace_tag('country_trade_de&amp;iso=xhan', 'country_trade_de')
# pq.replace_tag('country_trade_de&amp;iso=xmun', 'country_trade_de')

pq.add_tag_default()

# # country_ar = 'argentina'

list_symbol = pq.load_list_symbol_for_tag_all(['country_work_pe', 'exchange_xnys'])
for symbol in list_symbol:
    print(symbol)


list_symbol = pq.load_list_symbol_for_tag_all(['country_work_pe', 'exchange_xnas'])
for symbol in list_symbol:
    print(symbol)
    
