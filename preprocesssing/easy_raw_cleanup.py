import pandas as pd
import os
import re

from util import *

tickers = os.listdir('../data/raw')

for ticker in tickers:
    csvFiles = os.listdir('../data/raw/'+ticker)
    for csvFile in csvFiles:
        print(ticker + csvFile)
        df = pd.read_csv('../data/raw/'+ticker+'/'+csvFile, header=None, keep_default_na=False)
        df = cleanFirstNumericRows(df)
        # drop x-1.csv files
        if len(df.index) < 5:
            continue

        df, period = cleanHeaderAndGetPeriod(df)
        print(df.iloc[0,:])
    break


