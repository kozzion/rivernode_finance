import sys
import os
import json

sys.path.append(os.path.abspath('../../rivernode_core'))
from rivernode_core.system_config import SystemConfig
from rivernode_core.persistency.table_object_loader_disk import TableObjectLoaderDisk

sys.path.append(os.path.abspath('../../rivernode_finance'))
from rivernode_finance.tools_option import ToolsOption
from rivernode_finance.struct.series_option_chain import SeriesOptionChain

## functions
def get_most_recent_unit(symbol):
    system_config = SystemConfig()
    loader_table = TableObjectLoaderDisk(system_config.load_path_dir_database())
    table_source = loader_table.load_table_for_list_key(['trading', 'option', symbol])
    key = sorted(table_source.load_list_key())[-1]
    series_option_chain = table_source.load_json_for_list_key([key])
    series_option_chain_unit = SeriesOptionChain.to_unit(series_option_chain)
    return series_option_chain_unit

## functions
system_config = SystemConfig()
loader_table = TableObjectLoaderDisk(system_config.load_path_dir_database())
list_symbol = loader_table.load_table_for_list_key(['trading', 'option_result']).load_list_key_table()
print(list_symbol)

list_symbol = ['AAPL', 'FB', 'AMZN', 'ASML'] 

list_option_chain = []
for symbol in list_symbol:
    series_option_chain_unit = get_most_recent_unit(symbol)
    option_chain = series_option_chain_unit['list_option_chain'][0]
    list_option_chain.append(option_chain)
ToolsOption.compare(list_option_chain)

