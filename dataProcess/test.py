import pandas as pd

# def get_date_list(begin_date, end_date):
#     dates = []
#     dt = datetime.strptime(begin_date, "%Y-%m-%d")
#     date = begin_date[:]
#     while date <= end_date:
#         if dt.strftime("%w") in ["5"]:
#             dates.append(date)
#             dt += timedelta(days=1)
#             date = dt.strftime("%Y-%m-%d")
#     return dates

def get_date_list(start, end):

    date_list = [d.strftime("%Y-%m-%d") for d in pd.date_range(start, end, freq="B")]
    res = []
    for i in range(4, len(date_list), 5):
        res.append(date_list[i])
    return res

if __name__ == "__main__":
    res = get_date_list('2019-04-01', '2019-05-11')
    print(res)
