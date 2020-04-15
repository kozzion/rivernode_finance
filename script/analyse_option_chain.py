import sys
import os
import json

sys.path.append(os.path.abspath('../../rivernode_core'))
from rivernode_core.client.tools_client import ToolsClient
from rivernode_core.system_config import SystemConfig

sys.path.append(os.path.abspath('../../rivernode_finance'))
from rivernode_finance.tools_option import ToolsOption

system_config = SystemConfig()
loader_table = TableObjectLoaderDisk(system_config.load_path_dir_database())
for symbol in list_symbol:
    table_source = loader_table.load_table_for_list_key(['trading', 'option', symbol])
    table_target = loader_table.load_table_for_list_key(['trading', 'option_result', symbol])

    series_option_chain = load_series_option_chain(symbol)
    result_series_option_chain = ToolsOption.analyse_series_option_chain(series_option_chain)
