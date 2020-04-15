import sys
import os
import json

sys.path.append(os.path.abspath('../../rivernode_core'))
from rivernode_core.client.tools_client import ToolsClient
from rivernode_core.system_config import SystemConfig

sys.path.append(os.path.abspath('../../rivernode_finance'))
from rivernode_finance.tools_option import ToolsOption

def load_series_option_chain(symbol):
    list_key_table = ['trading', 'option', symbol]
    table_loader = ToolsClient.create_client('XXXX', name_host='10.100.10.63', name_port='5001')
    # table_loader = ToolsClient.create_client('XXXX', name_host='127.0.0.1', name_port='5000') #localhost
    table_object = table_loader.load_table_for_list_key(list_key_table)
    system_config = SystemConfig()
    key_most_recent = sorted(table_object.load_list_key())[-1]
    series_option_chain = json.loads(table_object.load_bytearray_for_key(key_most_recent))
    return series_option_chain






symbol = 'nflx'
path_file = 'response_option_chain.json'
path_file_2 = 'list_result_option_chain.json'
if os.path.isfile(path_file):
    with open(path_file, 'r') as file:
        series_option_chain = json.load(file)    
else:
    series_option_chain = load_series_option_chain(symbol)
    with open(path_file, 'w') as file:
        json.dump(series_option_chain, file)


# option_chain = list(series_option_chain['dict_option_chain'].values())[0]
# ToolsOption.option_model_test_2(option_chain)
# exit()
# exit()
# print(series_option_chain)

if os.path.isfile(path_file_2):
    with open(path_file_2, 'r') as file:
        result_series_option_chain = json.load(file)    
else:
    result_series_option_chain = ToolsOption.analyse_series_option_chain(series_option_chain)
    with open(path_file_2, 'w') as file:
        json.dump(series_option_chain, file)

# print(-0.8879056047197906**0.5296874999999925)
# exit()
# result_series_option_chain = ToolsOption.analyse_series_option_chain(series_option_chain)
list_parameter_0 = []
for name_model in list(result_series_option_chain['dict_model'].keys())[2:]:
    list_parameter_0.append([name_model, 'error'])
ToolsOption.plot(result_series_option_chain, list_parameter_0)
# list_parameter_0.append('bs_inf_call_l2')
# list_parameter_0.append('bs_inffs_put_l2')
# list_parameter_0.append('bs_inffs_call_l2')
# list_parameter_1 = []
# list_parameter_1.append('bs_inffs_put_spot')
# # list_parameter_1.append('bs_inffs_call_spot')
# list_parameter_1 = []
# list_parameter_1.append(['nlr_bs_inf_fs_call', 'spot'])
# ToolsOption.plot(result_series_option_chain, list_parameter_0)
# ToolsOption.plot(result_series_option_chain, list_parameter_1)




'nlr_bs_inf_ls_put', 
'nlr_bs_inf_ls_call', 
'nlr_bs_inf_fs_put', 
'nlr_bs_inf_fs_call', 'nlr_pd_normal_put', 'nlr_pd_normal_call'
