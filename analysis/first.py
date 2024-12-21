import os

dumpPath = '../data/processed/easy_raw_cleanup'

i = 0
for filename in os.listdir(dumpPath):
    i += 1
print('Tickers to be analyzed: ' + str(i))