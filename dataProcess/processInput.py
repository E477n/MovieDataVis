import pandas as pd
import datetime

def extractFriday(start, end):
    offset = {0: 4, 1: 3, 2: 2, 3: 1, 4: 0, 5: 6, 6: 5}

    date_list = [d.strftime("%Y-%m-%d") for d in pd.date_range(start, end, freq="B")]
    d = start.split('-')
    weekday = datetime.date(int(d[0]), int(d[1]), int(d[2])).weekday()
    res = []
    for i in range(offset[weekday], len(date_list), 5):
        res.append(date_list[i])
    return res

if __name__ == "__main__":
    print(extractFriday("2020-05-01", "2020-09-30"))
