import sys
import os
import json
import matplotlib.pyplot as plt

sys.path.append(os.path.abspath('../../rivernode_finance'))
from rivernode_finance.client.nasdaq.client_nasdaq_getto import ClientNasdaqGetto
from rivernode_finance.tools_option import ToolsOption

path_file = 'response_option_chain.json'
if os.path.isfile(path_file):
    with open(path_file, 'r') as file:
        response_option_chain = json.load(file)
else:
    client = ClientNasdaqGetto()
    response_option_chain = client.get_option_chain('nflx')
    with open(path_file, 'w') as file:
        json.dump(response_option_chain, file)

# print(dict_option_chain)



# ToolsPlotOption.analyse()
print(response_option_chain['spot'])
ToolsOption.analyse_response_option_chain(response_option_chain)
exit()
count_row = len(response_option_chain['dict_option_chain'])
symbol = response_option_chain['symbol']
plt.figure()
for index_row, option_chain in enumerate(list(response_option_chain['dict_option_chain'].values())):
    index_plot = index_row + 1
    plt.subplot(count_row, 1, index_plot)
    plt.title(symbol + ' ' + option_chain['expiryDate'])
    plt.plot(option_chain['list_strike'], option_chain['list_put_bid'])
    plt.plot(option_chain['list_strike'], option_chain['list_put_ask'])
    plt.plot(option_chain['list_strike'], option_chain['list_call_bid'])
    plt.plot(option_chain['list_strike'], option_chain['list_call_ask'])
    plt.legend(['put bid', 'put ask', 'call bid', 'call ask'])
plt.show()