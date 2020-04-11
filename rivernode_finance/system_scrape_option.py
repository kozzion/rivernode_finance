import sys
import os
import json
import time
import datetime
import pytz

sys.path.append(os.path.abspath('../../rivernode_core'))
from rivernode_core.system_config import SystemConfig
from rivernode_core.persistency.table_object_loader_disk import TableObjectLoaderDisk


sys.path.append(os.path.abspath('../../rivernode_finance'))
from rivernode_finance.client.nasdaq.client_nasdaq_getto import ClientNasdaqGetto
from rivernode_finance.tools_option import ToolsOption




class SystemScrapeOption(object):

    def __init__(self):
        super(SystemScrapeOption, self).__init__()
        self.client = ClientNasdaqGetto()
        system_config = SystemConfig()
        loader_table = TableObjectLoaderDisk(system_config.load_path_dir_database())
        self.table = loader_table.load_table_for_list_key(['trading', 'option'])
        self.list_symbol = ['fb', 'nflx']
        self.timestamp_scape_last = 0



    def run(self):
        while(True):
            timestamp_current = int(time.time())
            print('flip')
            sys.stdout.flush()
            if self.is_scrape_time(timestamp_current):
                print('is_scrape_time')
                sys.stdout.flush()
                self.timestamp_scape_last = timestamp_current
                for symbol in self.list_symbol:
                    print(symbol)
                    sys.stdout.flush()
                    response_option_chain = self.client.get_option_chain(symbol)
                    table_symbol = self.table.load_table_for_list_key([symbol])
                    key = str(response_option_chain['timestamp_request'])
                    sys.stdout.flush()
                    table_symbol.save_json_for_key(key, response_option_chain)

            print('sleep')
            sys.stdout.flush()
            time.sleep(3600)
    
    def is_scrape_time(self, timestamp_current):
        now = datetime.datetime.now(tz=pytz.timezone('US/Eastern'))

        #is less than 12 hours after last scrape
        if timestamp_current - self.timestamp_scape_last < 3600 * 12:
            return False

        #is on a saturday or sunday # apparantly not
        # if now.weekday() == 5 or now.weekday() == 6:
        #     return False
 
        #is before 11 o clock in usa or after 1600
        if now.time().hour < 11 or 15 <= now.time().hour:
            return False

        return True

        