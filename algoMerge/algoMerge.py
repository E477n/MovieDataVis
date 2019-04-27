import pymongo
import datetime
from statsmodels.tsa.arima_model import ARMA
from dataProcess import processInput
from dataProcess import Factor2_competitors
from dataProcess import factor3

client = pymongo.MongoClient(host='127.0.0.1', port=27017)
db = client['movie_db']

input = ["Moana2", "2020-05-01", "2020-09-30", ["Animation", "Adventure"], "Moana", 200]
startYear = 8
monthConvert = {1: "Jan.", 2: "Feb.", 3: "Mar.", 4: "Apr.", 5: "May", 6: "Jun.", 7: "Jul.", 8: "Aug.", 9: "Sept.", 10: "Oct.", 11: "Nov.", 12: "Dec."}
monthConvert2 = {1: "Jan", 2: "Feb", 3: "Mar", 4: "Apr", 5: "May", 6: "Jun", 7: "Jul", 8: "Aug", 9: "Sep", 10: "Oct", 11: "Nov", 12: "Dec"}

# factor 1 - historical box office receipts forecast
def historicalBoxOfficeForecast(dateSet):
    res = []

    # Friday forecast
    # using simple sum and data on specific day
    col_daily = db['daily']
    dailyGrossSet = []
    for day in dateSet:
        # e.g. day = '2020-05-01'
        day = day.split('-')
        searchDay = monthConvert[int(day[1])] + " " + str(int(day[2]))
        row = []
        for record in col_daily.find({"Date": searchDay}):
            movieNumber = record['MoviesTracked']
            gross = record['Gross($)'].replace(",", "")
            row.append(int(gross) / int(movieNumber))
        simplesum = 0
        for i in range(startYear, startYear + 10):
            simplesum += row[i - 2]
        dailyGrossSet.append(simplesum/10)
    res.append(dailyGrossSet)

    # Weekly forecast
    # using weighted moving average 2 and data on specific week
    col_weekly = db['weekly']
    weeklyGrossSet = []
    sum = 55
    for day in dateSet:
        # convert date to corresponding week
        rd = day.split('-')
        dt = datetime.date(int(rd[0]), int(rd[1]), int(rd[2]))
        wk = dt.isocalendar()[1]
        weightedSum = 0
        i = 17  # the result from db was from 2017 to 2008
        for record in col_weekly.find({"Week#": wk}):
            year = record['Year']
            if int(year) >= 2018 or int(year) < 2008:
                continue
            og = record['OverallGross($)'].replace(",", "")
            tm = record['TotalMovies']
            weightedSum += int(og)/int(tm) * (i-7)/sum
            i -= 1
        weeklyGrossSet.append(weightedSum)
    res.append(weeklyGrossSet)

    # Monthly forecast
    # using moving average and data on specific month
    col_monthly = db['monthly']
    monthlyGrossSet = []
    for day in dateSet:
        rd = day.split('-')
        month = monthConvert2[int(rd[1])]
        gs = []
        for record in col_monthly.find({"month": month}):
            year = record['Year']
            if int(year) >= 2018 or int(year) < 2008:
                continue
            avgGross = record['MovieAvg($)']
            gs.append(float(avgGross))
        # original data is from 2017 to 2008, which needs to be reversed
        gs.reverse()
        # fit model
        model = ARMA(gs, order=(0, 1))
        model_fit = model.fit(disp=False)
        # make prediction
        g = model_fit.predict(len(gs), len(gs))
        g = float(g)
        monthlyGrossSet.append(g)
    res.append(monthlyGrossSet)

    return res

def quantifyFactor1(dateSet):
    q_daily = []
    q_weekly = []
    q_monthly = []
    f1_res = []

    res = historicalBoxOfficeForecast(dateSet)
    daily = res[0]
    weekly = res[1]
    monthly = res[2]

    daily_max = max(daily)
    # V_11i / (max⁡(V_11i))*100
    for item in daily:
        item = round(item / daily_max * 100, 2)
        q_daily.append(item)

    weekly_max = max(weekly)
    for item in weekly:
        item = round(item / weekly_max * 100, 2)
        q_weekly.append(item)

    monthly_max = max(monthly)
    for item in monthly:
        item = round(item / monthly_max * 100, 2)
        q_monthly.append(item)

    # print(q_daily)
    # print(q_weekly)
    # print(q_monthly)
    for i in range(0, len(q_daily)):
        q = round((q_daily[i] + q_weekly[i] + q_monthly[i]) / 3, 2)
        f1_res.append(q)
    print(f1_res)

def quantifyFactor2(dateStart, dateEnd, genre):
    q_1 = []
    q_2 = []
    f2_res = []

    res = Factor2_competitors.gradeFridaywithCompetitor(dateStart, dateEnd, genre)

    # 100 - 10 * V_21i
    for item in res[0]:
        item = 100 - 10 * item
        q_1.append(item)
    for item in res[1]:
        item = 100 - 10 * item
        q_2.append(item)
    for i in range(0, len(q_1)):
        q = round((q_1[i] + q_2[i]) / 2, 2)
        f2_res.append(q)

    print(q_1)
    print(q_2)
    print(f2_res)

def quantifyFactor3(dateSet, genre):
    res = factor3.calTotalGrossofSameGenreSameWeek(dateSet, genre)
    print(res)

def merge(input):
    movieName = input[0]
    dateStart = input[1]
    dateEnd = input[2]
    genre = input[3]

    dateSet = processInput.extractFriday(dateStart, dateEnd)

    quantifyFactor1(dateSet)
    quantifyFactor2(dateStart, dateEnd, genre)
    quantifyFactor3(dateSet, genre)

if __name__ == "__main__":
    merge(input)