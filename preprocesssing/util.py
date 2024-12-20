import re
import pandas as pd

THOUSAND = 'thousand'
MILLION = 'million'
USD = 'usd'


def cleanFirstNumericRows(df):
    while all([x.isnumeric() or x == '' for x in df.iloc[0, 1:]]):
        df = df.iloc[1:].reset_index(drop=True)
    # while True:
    #     wrong = [val == '' or val.isnumeric() for val in df.iloc[0, :]]
    #     if all(wrong):
    #         df = df.iloc[1:].reset_index(drop=True)
    #     else:
    #         break
    return df


def trashRow(df):
    return all([x == ''
                or 'see note' in x.lower()
                or 'may not sum ' in x.lower()
                or 'intersegment revenues are not material' in x.lower()
                or 'based on continuing operations' in x.lower()
                or 'may not add ' in x.lower()
                or 'does not foot' in x.lower()
                or 'net of income taxes.' in x.lower()
                or re.search('^\[[0-9]\]$', x)
                or re.search('^\([0-9]\)$', x)
                or re.search('^\{[0-9]\}$', x)
                for x in df.iloc[0, 1:]])


# https://www.geeksforgeeks.org/python-find-most-frequent-element-in-a-list/
def most_frequent(List):
    return max(set(List), key=List.count)


def cleanHeaderAndGetPeriod(df: pd.DataFrame):
    period = -1
    while trashRow(df):
        df = df.iloc[1:].reset_index(drop=True)
    try:
        while True:
            periodTags = [re.search('^[0-9]+.?months.?end.*$', val.lower()) for val in df.iloc[0, :]]
            periodTags = [x for x in periodTags if x]
            if not any(periodTags):
                raise Exception('No period found - inside')
            periods = [int(re.search('^[0-9]+', x.group()).group()) for x in periodTags]
            period = most_frequent(periods)

            df = df.iloc[1:].reset_index(drop=True)
    except Exception as e:
        if period == -1:
            # junk row on top
            if any([len(x) > 40 for x in df.iloc[0, :]]) or all([x.isnumeric() for x in df.iloc[0, 1:]]):
                df = df.iloc[1:].reset_index(drop=True)
                return cleanHeaderAndGetPeriod(df)
            raise Exception('No period found')
    return df, period


def parseAnotherHeader(df: pd.DataFrame):
    isThousand = [re.search('^.*thousand.*$', val.lower()) for val in df.iloc[0, :]]
    thousandIndexes = [i for i, val in enumerate(isThousand) if bool(val)]
    thousandCount = len(thousandIndexes)
    isMillion = [re.search('^.*million.*$', val.lower()) for val in df.iloc[0, :]]
    millionIndexes = [i for i, val in enumerate(isMillion) if bool(val)]
    millionCount = len(millionIndexes)
    isUsd = [re.search('^.*usd.*$', val.lower()) for val in df.iloc[0, :]]
    usdIndexes = [i for i, val in enumerate(isUsd) if bool(val)]

    if thousandCount == 0 and millionCount == 0 and len(usdIndexes) == 0:
        print('ANOTHER HEADER FAILED TO GET UNIT!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
        raise Exception('ANOTHER HEADER')
    if thousandCount == 0 and millionCount == 0:
        res = USD
    elif thousandCount > millionCount:
        res = THOUSAND
    else:
        res = MILLION
    indexes = thousandIndexes + millionIndexes + usdIndexes
    for i in indexes:
        df.iloc[0, i] = ''
    return df, res
