import pandas as pd
import os
import re
import json

from util import *

tickers = os.listdir('../data/raw')
dumpPath = '../data/processed/easy_raw_cleanup'
dumpPathV2 = '../data/processed/easy_raw_cleanup_v2'

periods = {}

for ticker in tickers:
    csvFiles = os.listdir('../data/raw/'+ticker)
    for i, csvFile in enumerate(csvFiles):
        # print(ticker + csvFile)
        df = pd.read_csv(os.path.join('../data/raw', ticker, csvFile), header=None, keep_default_na=False)
        # drop x-1.csv files
        if len(df.index) < 8 or (re.search('^.*-[1-9].csv$', csvFile) and len(df.index) < 15):
            continue

        df = cleanFirstNumericRows(df)
        df = cleanUpToPeriodOrDate(df)
        df, period = getPeriod(df)
        df, unit = parseAnotherHeader(df)

        # save by company
        dirPath = os.path.join(dumpPath, ticker, str(period), str(unit))
        os.makedirs(dirPath, exist_ok=True)
        df.to_csv(os.path.join(dirPath, csvFile), header=False, index=False)

        # save by period/unit/ticker
        dirPath = os.path.join(dumpPathV2, str(period), str(unit), ticker)
        os.makedirs(dirPath, exist_ok=True)
        df.to_csv(os.path.join(dirPath, csvFile), header=False, index=False)

        if period not in periods:
            periods[period] = {}
        periods[period][ticker] = 1


    print(ticker + ' done')

for period in periods.keys():
    print(period)
    if period != 12 and period != 3:
        print(json.dumps(periods[period]))
