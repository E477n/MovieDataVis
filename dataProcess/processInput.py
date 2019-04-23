import pandas as pd

def extractFriday(start, end):

    date_list = [d.strftime("%Y-%m-%d") for d in pd.date_range(start, end, freq="B")]
    res = []
    for i in range(4, len(date_list), 5):
        res.append(date_list[i])
    return res


if __name__ == "__main__":
    res = extractFriday('2019-04-01', '2019-05-11')
    print(res)
