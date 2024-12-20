import pandas as pd
import os
import re

from util import *

tickers = os.listdir('../data/raw')
dumpPath = '../data/processed/easy_raw_cleanup'

for ticker in tickers:
    csvFiles = os.listdir('../data/raw/'+ticker)
    for i, csvFile in enumerate(csvFiles):
        print(ticker + csvFile)
        df = pd.read_csv(os.path.join('../data/raw', ticker, csvFile), header=None, keep_default_na=False)
        # drop x-1.csv files
        if len(df.index) < 8 or (re.search('^.*-[1-9].csv$', csvFile) and len(df.index) < 15):
            continue

        df = cleanFirstNumericRows(df)
        df, period = cleanHeaderAndGetPeriod(df)
        df, unit = parseAnotherHeader(df)
        dirPath = os.path.join(dumpPath, ticker, str(period), str(unit))
        os.makedirs(dirPath, exist_ok=True)
        df.to_csv(os.path.join(dirPath, str(i) + '.csv'), header=False, index=False)

    print(ticker + ' done')
