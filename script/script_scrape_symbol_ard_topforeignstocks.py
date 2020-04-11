import sys
import os
import json
import hashlib


sys.path.append(os.path.abspath('../../rivernode_core'))
from rivernode_core.system_config import SystemConfig
from rivernode_core.persistency.table_object_loader_disk import TableObjectLoaderDisk

sys.path.append(os.path.abspath('../../rivernode_finance'))
from rivernode_finance.client_topforeignstocks import ClientTopforeignstocks
from rivernode_finance.persistency_quote import PersistencyQuote

system_config = SystemConfig()
loader_table = TableObjectLoaderDisk(system_config.load_path_dir_database())
pq = PersistencyQuote(loader_table.load_table_for_list_key(['trading']))
client = ClientTopforeignstocks(pq)

client.test()