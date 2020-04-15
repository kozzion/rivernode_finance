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

    def __init__(self, list_symbol):
        self.list_symbol = list_symbol
        super(SystemScrapeOption, self).__init__()
        self.client = ClientNasdaqGetto()
        system_config = SystemConfig()
        loader_table = TableObjectLoaderDisk(system_config.load_path_dir_database())
        self.table = loader_table.load_table_for_list_key(['trading', 'option'])
        self.timestamp_scape_last = 0



    def run(self):
        while(True):
            print('work')
            sys.stdout.flush()    
            if self.is_scrape_time():
                print('is_scrape_time')
                sys.stdout.flush()
                for symbol in self.list_symbol:
                    try:
                        table_symbol = self.table.load_table_for_list_key([symbol])
                        list_key = sorted(table_symbol.load_list_key())
                        if 0 < len(list_key):
                            if self.is_today(int(list_key[-1])):
                                continue

                        print(symbol)
                        sys.stdout.flush()
                        response_option_chain = self.client.get_option_chain(symbol)
                        key = str(response_option_chain['timestamp_request'])
                        sys.stdout.flush()
                        table_symbol.save_json_for_key(key, response_option_chain)
                    except Exception:
                        print('Failed')
                        sys.stdout.flush()


            print('sleep')
            sys.stdout.flush()
            time.sleep(3600)

    def is_today(self, timestamp):
        datetime_last = datetime.datetime.fromtimestamp(timestamp, tz=pytz.timezone('US/Eastern'))
        datetime_now = datetime.datetime.now(tz=pytz.timezone('US/Eastern'))
        return datetime_last.date() == datetime_now.date()

    def is_scrape_time(self):
        now = datetime.datetime.now(tz=pytz.timezone('US/Eastern'))

        #is on a saturday or sunday # apparantly not
        if now.weekday() == 5 or now.weekday() == 6:
            return False
 
        #is before 11 o clock in usa or after 1600
        # if now.time().hour < 11 or 15 <= now.time().hour:
        #     return False

        return True

        