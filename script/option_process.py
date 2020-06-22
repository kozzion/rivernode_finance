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
list_symbol = loader_table.load_table_for_list_key(['trading', 'option']).load_list_key_table()

for index, symbol in enumerate(list_symbol):
    print(symbol)
    table_source = loader_table.load_table_for_list_key(['trading', 'option', symbol])
    table_target = loader_table.load_table_for_list_key(['trading', 'option_result', symbol])


    if symbol in ['LBTYA','TMUS']:
        continue
    key = sorted(table_source.load_list_key())[-1]
    if not table_target.has_object_for_key(key):
        series_option_chain = table_source.load_json_for_list_key([key])
        result_series_option_chain = ToolsOption.analyse_series_option_chain(series_option_chain)
        table_target.save_json_for_list_key([key], result_series_option_chain)


    #LBTYA