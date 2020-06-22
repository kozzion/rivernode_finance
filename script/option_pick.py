import sys
import os
import json

sys.path.append(os.path.abspath('../../rivernode_core'))
from rivernode_core.system_config import SystemConfig
from rivernode_core.persistency.table_object_loader_disk import TableObjectLoaderDisk

sys.path.append(os.path.abspath('../../rivernode_finance'))
from rivernode_finance.tools_option import ToolsOption

system_config = SystemConfig()
loader_table = TableObjectLoaderDisk(system_config.load_path_dir_database())
list_symbol = loader_table.load_table_for_list_key(['trading', 'option_result']).load_list_key_table()

for index, symbol in enumerate(list_symbol):
    print(symbol)
    table_target = loader_table.load_table_for_list_key(['trading', 'option_result', symbol])
    key = sorted(table_target.load_list_key())[-1]
    result_series_option_chain = table_target.load_json_for_list_key([key])
    ToolsOption.pick_option_value_put(result_series_option_chain)

    exit()

    #LBTYA