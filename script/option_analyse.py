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
series_option_chain_unit = get_most_recent_unit('AAPL')
result_series_option_chain = ToolsOption.analyse_series_option_chain_deconv(series_option_chain_unit)
list_name_model = ['deconvolution_put_0', 'normal_put']
list_name_parameter = ['error', 'cost', 'pdf_mu']
ToolsOption.plot_analyse_result(result_series_option_chain, list_name_model, list_name_parameter)

list_series_option_chain_unit = []
list_series_option_chain_unit.append(get_most_recent_unit('AAPL'))
list_series_option_chain_unit.append(get_most_recent_unit('FB'))
list_series_option_chain_unit.append(get_most_recent_unit('AMZN'))
list_series_option_chain_unit.append(get_most_recent_unit('ASML'))

list_result_series_option_chain = []
for series_option_chain_unit in list_series_option_chain_unit:
    list_result_series_option_chain.append(ToolsOption.analyse_series_option_chain_deconv(series_option_chain_unit))

list_tuple_model_parameter = []  
# list_tuple_model_parameter.append(('deconvolution_put_0', 'error'))
# list_tuple_model_parameter.append(('deconvolution_put_0', 'cost'))
# list_tuple_model_parameter.append(('deconvolution_put_0', 'pdf_mu'))
list_tuple_model_parameter.append(('normal_put', 'error'))
list_tuple_model_parameter.append(('normal_put', 'pdf_mu'))
list_tuple_model_parameter.append(('normal_put', 'pdf_sd'))
list_tuple_model_parameter.append(('normal_call', 'error'))
list_tuple_model_parameter.append(('normal_call', 'pdf_mu'))
list_tuple_model_parameter.append(('normal_call', 'pdf_sd'))
ToolsOption.plot_compare_result(list_result_series_option_chain, list_tuple_model_parameter)
