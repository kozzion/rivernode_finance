import sys
import os

sys.path.append(os.path.abspath('../../rivernode_finance'))
from rivernode_finance.client.ibapi.connection import Connection

# host = '64.190.197.40'
# port = 4000

host = '127.0.0.1'
port = 7496

from rivernode_finance.client.ibapi.connection import Connection
from rivernode_finance.client.ibapi.contract import Contract
from rivernode_finance.client.ibapi.order import Order

def make_contract(symbol, sec_type, exch, prim_exch, curr):

    Contract.m_symbol = symbol
    Contract.m_secType = sec_type
    Contract.m_exchange = exch
    Contract.m_primaryExch = prim_exch
    Contract.m_currency = curr
    return Contract



def make_order(action,quantity, price = None):

    if price is not None:
        order = Order()
        order.m_orderType = 'LMT'
        order.m_totalQuantity = quantity
        order.m_action = action
        order.m_lmtPrice = price

    else:
        order = Order()
        order.m_orderType = 'MKT'
        order.m_totalQuantity = quantity
        order.m_action = action

        
    return order



def make_mseage(action,quantity, price = None):

    if price is not None:
        order = Order()
        order.m_orderType = 'LMT'
        order.m_totalQuantity = quantity
        order.m_action = action
        order.m_lmtPrice = price

    else:
        order = Order()
        order.m_orderType = 'MKT'
        order.m_totalQuantity = quantity
        order.m_action = action

        
    return order







cid = 303
conn = Connection(host=host, port=port)
conn.connect()
# print("serverVersion:%s connectionTime:%s" % (conn.serverVersion(), conn.twsConnectionTime()))
conn.disconnect()

cid += 1