import re

def cleanFirstNumericRows(df):
    while True:
        wrong = [val == '' or val.isnumeric() for val in df.iloc[0, :]]
        if all(wrong):
            df = df.iloc[1:].reset_index(drop=True)
        else:
            break
    return df

# https://www.geeksforgeeks.org/python-find-most-frequent-element-in-a-list/
def most_frequent(List):
    return max(set(List), key=List.count)


# group by months period and need to get unit (millions etc). .? for capitalizing
def cleanHeaderAndGetPeriod(df):
    period = -1
    try:
        while True:
            periodTags = [re.search('^[0-9]+.?.?onths.?.?nd.*$', val) for val in df.iloc[0, :]]
            periodTags = [x for x in periodTags if x]
            if not any(periodTags):
                raise Exception('No period found - inside')
            periods = [int(re.search('^[0-9]+', x.group()).group()) for x in periodTags]
            period = most_frequent(periods)

            df = df.iloc[1:].reset_index(drop=True)
    except Exception as e:
        if period == -1:
            raise Exception('No period found')
    return df, period