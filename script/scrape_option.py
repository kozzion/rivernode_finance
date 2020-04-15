import sys
import os
import json


sys.path.append(os.path.abspath('../../rivernode_finance'))
from rivernode_finance.system_scrape_option import SystemScrapeOption

list_symbol = [
    'MSFT',
    'AAPL',
    'AMZN',
    'FB',
    'GOOG',
    'GOOGL',
    'INTC',
    'PEP',
    'CSCO',
    'NFLX',
    'CMCSA',
    'NVDA',
    'ADBE',
    'COST',
    'AMGN',
    'PYPL',
    'TSLA',
    'AVGO',
    'CHTR',
    'TXN',
    'GILD',
    'SBUX',
    'QCOM',
    'MDLZ',
    'TMUS',
    'FISV',
    'INTU',
    'VRTX',
    'ADP',
    'BKNG',
    'BIIB',
    'ISRG',
    'AMD',
    'REGN',
    'MU',
    'ATVI',
    'CSX',
    'AMAT',
    'ILMN',
    'JD',
    'WBA',
    'LRCX',
    'ADI',
    'EXC',
    'ADSK',
    'XEL', #TODO problematic
    'KHC',
    'MNST',
    'EA',
    'ROST',
    'CTSH',
    'EBAY',
    'BIDU',
    'MELI',
    'ORLY',#TODO problematic
    'MAR',
    'NXPI',
    'NTES',
    'WLTW',#TODO problematic
    'LULU',
    'KLAC',
    'VRSK',
    'VRSN',
    'WDAY',
    'PAYX',
    'CSGP',
    'PCAR',
    'SIRI',
    'IDXX',
    'ALXN',
    'SNPS',
    'XLNX',
    'CERN',
    'SGEN',
    'ANSS',
    'ASML',
    'CTAS',
    'CDNS',
    'SPLK',
    'MCHP',
    'INCY',
    'FAST',
    'CTXS',
    'DLTR',
    'CPRT',
    'CHKP',
    'SWKS',
    'BMRN',
    'CDW',
    'ALGN',
    'MXIM', 
    'TTWO',
    'WDC',
    'TCOM',
    'ULTA',
    'NTAP',
    'FOXA',
    'EXPE',
    'LBTYK',
    'UAL',
    'FOX',
    'AAL',
    'LBTYA']


#blacklist
list_symbol.remove('XEL')
list_symbol.remove('FOX')
list_symbol.remove('WLTW')
list_symbol.remove('ORLY')
list_symbol.remove('CDW')
list_symbol.remove('MXIM')
list_symbol.remove('CHKP')
list_symbol.remove('CPRT')
list_symbol.remove('CTAS')
list_symbol.remove('ANSS')
list_symbol.remove('SNPS')
list_symbol.remove('VRSK')
list_symbol.remove('VRSN')
list_symbol.remove('CSGP')
list_symbol.remove('PCAR')
list_symbol.remove('IDXX')


system = SystemScrapeOption(list_symbol)
system.run()