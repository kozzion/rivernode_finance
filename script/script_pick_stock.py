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
list_symbol = pq.load_list_symbol()

def reject(quote):
    try:

        ptp = quote['ratio_price_to_profit']
        if ptp < 0.1:
            return True

        ptr = quote['ratio_price_to_revenue']
        if 0.5 < ptr:
            return True

        ratio_profit = (quote['list_ratio_profit'][0] + quote['list_ratio_profit'][1] + quote['list_ratio_profit'][2]) / 3
        if ratio_profit < 0.1:
            return True

        gain_rev = (quote['list_ratio_revenue_change'][0] * quote['list_ratio_revenue_change'][1] * quote['list_ratio_revenue_change'][2])
        if gain_rev < 1.2:
            return True

        if 0.05 < quote['ratio_interest_to_revenue']:
            return True
        return False
    except Exception:
        return True


list_ticker_prospect = [
    'TSM',#country_work_taiwan !!! semi conductor
    'MOMO',#country_work_china
    'YY',
    'TSLA',
    'RWEOY'] #country_work_china social

# for ticker in list_ticker_prospect:
#     symbol = pq.load_symbol(ticker)
#     print(symbol['list_tag'])
ToolsQuote.print_quote_short_header()
for ticker in list_ticker_prospect:
    quote = pq.load_quote(ticker)
    ToolsQuote.print_quote(quote)

# ToolsQuote.print_quote(pq.load_quote('AMZN'))

# list_ticker_current = ['SBS']
# for ticker in list_ticker_current:
#     if pq.has_quote(ticker):
#         quote = pq.load_quote(ticker)
#         ToolsQuote.print_quote(quote)



# NextEra Energy (NYSE: NEE)
# A utility focused on wind and solar power

# Tesla (NASDAQ: TSLA)
# Electric vehicles, solar panels, and battery storage

# First Solar (NASDAQ: FSLR)
# Solar panel manufacturer

# Brookfield Renewable Partners (NYSE: BEP)
# Hydroelectric power

# SolarEdge Technologies (NASDAQ: SEDG)
# Solar optimizers and inverters

# Enphase Energy (NASDAQ: ENPH)
# Microinverters

# Ormat Technologies (NYSE: ORA)
# Geothermal power

# TerraForm Power (NASDAQ: TERP)
# Wind and solar power generation

# NextEra Energy Partners (NYSE: NEP)
# Renewable power generation and natural gas pipelines

# Atlantica Yield (NASDAQ: AY)
# Clean power generation, electricity infrastructure, water assets