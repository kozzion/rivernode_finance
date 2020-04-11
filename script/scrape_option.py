import sys
import os
import json


sys.path.append(os.path.abspath('../../rivernode_finance'))
from rivernode_finance.system_scrape_option import SystemScrapeOption
system = SystemScrapeOption()
system.run()