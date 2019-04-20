import pymongo
from statsmodels.tsa.ar_model import AR
from statsmodels.tsa.arima_model import ARMA
from statsmodels.tsa.arima_model import ARIMA

client = pymongo.MongoClient(host='127.0.0.1', port=27017)
db = client['movie_db']

#data set 1
def monthlySimpleAvg(month):
    col_monthly = db['monthly']
    monthlyGrossSet = []
    simplesum = 0
    for record in col_monthly.find({"month": month}):
        year = record['Year']
        if int(year) >= 2018 or int(year) < 2008:
            continue
        avgGross = record['MovieAvg($)']
        monthlyGrossSet.append(float(avgGross))
        simplesum += float(avgGross)
    # original data is from 2017 to 2008, which need to be reversed
    monthlyGrossSet.reverse()
    print(monthlyGrossSet)
    print(simplesum/len(monthlyGrossSet))

def wma1(month):
    col_monthly = db['monthly']
    monthlyGrossSet = []
    weightedSum = 0
    sum = 0
    for i in range (8, 18):
        sum += i
    i = 17 #the result from db was from 2017 to 2008

    for record in col_monthly.find({"month": month}):
        year = record['Year']
        if int(year) >= 2018 or int(year) < 2008:
            continue
        avgGross = record['MovieAvg($)']
        monthlyGrossSet.append(float(avgGross))
        weightedSum += float(avgGross) * i/sum
        i -= 1
    print(weightedSum, sum)

def wma2(month):
    col_monthly = db['monthly']
    monthlyGrossSet = []
    weightedSum = 0
    sum = 0
    for i in range (1, 11):
        sum += i
    i = 17 #the result from db was from 2017 to 2008
    for record in col_monthly.find({"month": month}):
        year = record['Year']
        if int(year) >= 2018 or int(year) < 2008:
            continue
        avgGross = record['MovieAvg($)']
        monthlyGrossSet.append(float(avgGross))
        weightedSum += float(avgGross) * (i-7)/sum
        i -= 1
    print(weightedSum, sum)

def ar1(month):
    col_monthly = db['monthly']
    monthlyGrossSet = []
    for record in col_monthly.find({"month": month}):
        year = record['Year']
        if int(year) >= 2018 or int(year) < 2008:
            continue
        avgGross = record['MovieAvg($)']
        monthlyGrossSet.append(float(avgGross))
    # original data is from 2017 to 2008, which need to be reversed
    monthlyGrossSet.reverse()
    print(monthlyGrossSet)
    # fit model
    model = AR(monthlyGrossSet)
    model_fit = model.fit()
    # make prediction
    res = model_fit.predict(len(monthlyGrossSet), len(monthlyGrossSet))
    print(res)


def movingAverage(month):
    col_monthly = db['monthly']
    monthlyGrossSet = []
    for record in col_monthly.find({"month": month}):
        year = record['Year']
        if int(year) >= 2018 or int(year) < 2008:
            continue
        avgGross = record['MovieAvg($)']
        monthlyGrossSet.append(float(avgGross))
    # original data is from 2017 to 2008, which need to be reversed
    monthlyGrossSet.reverse()
    print(monthlyGrossSet)
    # fit model
    model = ARMA(monthlyGrossSet, order=(0, 1))
    model_fit = model.fit(disp=False)
    # make prediction
    res = model_fit.predict(len(monthlyGrossSet), len(monthlyGrossSet))
    print(res)

def arma1(month):
    col_monthly = db['monthly']
    monthlyGrossSet = []
    for record in col_monthly.find({"month": month}):
        year = record['Year']
        if int(year) >= 2018 or int(year) < 2008:
            continue
        avgGross = record['MovieAvg($)']
        monthlyGrossSet.append(float(avgGross))
    # original data is from 2017 to 2008, which need to be reversed
    monthlyGrossSet.reverse()
    print(monthlyGrossSet)
    # fit model
    model = ARMA(monthlyGrossSet, order=(2, 1))
    model_fit = model.fit(disp=False)
    # make prediction
    res = model_fit.predict(len(monthlyGrossSet), len(monthlyGrossSet))
    print(res)

def arima1(month):
    col_monthly = db['monthly']
    monthlyGrossSet = []
    for record in col_monthly.find({"month": month}):
        year = record['Year']
        if int(year) >= 2018 or int(year) < 2008:
            continue
        avgGross = record['MovieAvg($)']
        monthlyGrossSet.append(float(avgGross))
    # original data is from 2017 to 2008, which need to be reversed
    monthlyGrossSet.reverse()
    print(monthlyGrossSet)
    # fit model
    model = ARIMA(monthlyGrossSet, order=(1, 1, 1))
    model_fit = model.fit(disp=False)
    # make prediction
    yhat = model_fit.predict(len(monthlyGrossSet), len(monthlyGrossSet), typ='levels')
    print(yhat)

# data set 3
def ar3(month):
    mdict = {"Jan": 1, "Feb": 2, "Mar": 3, "Apr": 4, "May": 5, "Jun": 6, "Jul": 7, "Aug": 8, "Sep": 9, "Oct": 10, "Nov": 11, "Dec": 12}
    col_monthly = db['monthly']
    monthlyGrossSet = []
    for y in range(2008, 2019):
        for record in col_monthly.find({"Year": str(y)}):
            mt = record['month']
            yr = record['Year']
            if mdict[mt] >= mdict[month] and int(yr) >= 2018:
                continue
            # print(mt, yr)
            avgGross = record['MovieAvg($)']
            monthlyGrossSet.append(float(avgGross))
    print(monthlyGrossSet)
    # fit model
    model = AR(monthlyGrossSet)
    model_fit = model.fit()
    # make prediction
    res = model_fit.predict(len(monthlyGrossSet), len(monthlyGrossSet))
    print(res)

def ma3(month):
    mdict = {"Jan": 1, "Feb": 2, "Mar": 3, "Apr": 4, "May": 5, "Jun": 6, "Jul": 7, "Aug": 8, "Sep": 9, "Oct": 10, "Nov": 11, "Dec": 12}
    col_monthly = db['monthly']
    monthlyGrossSet = []
    for y in range(2008, 2019):
        for record in col_monthly.find({"Year": str(y)}):
            mt = record['month']
            yr = record['Year']
            if mdict[mt] >= mdict[month] and int(yr) >= 2018:
                continue
            # print(mt, yr)
            avgGross = record['MovieAvg($)']
            monthlyGrossSet.append(float(avgGross))
    print(monthlyGrossSet)
    # fit model
    model = ARMA(monthlyGrossSet, order=(0, 1))
    model_fit = model.fit(disp=False)
    # make prediction
    res = model_fit.predict(len(monthlyGrossSet), len(monthlyGrossSet))
    print(res)

def arma3(month):
    mdict = {"Jan": 1, "Feb": 2, "Mar": 3, "Apr": 4, "May": 5, "Jun": 6, "Jul": 7, "Aug": 8, "Sep": 9, "Oct": 10, "Nov": 11, "Dec": 12}
    col_monthly = db['monthly']
    monthlyGrossSet = []
    for y in range(2008, 2019):
        for record in col_monthly.find({"Year": str(y)}):
            mt = record['month']
            yr = record['Year']
            if mdict[mt] >= mdict[month] and int(yr) >= 2018:
                continue
            # print(mt, yr)
            avgGross = record['MovieAvg($)']
            monthlyGrossSet.append(float(avgGross))
    print(monthlyGrossSet)
    # fit model
    model = ARMA(monthlyGrossSet, order=(2, 1))
    model_fit = model.fit(disp=False)
    # make prediction
    res = model_fit.predict(len(monthlyGrossSet), len(monthlyGrossSet))
    print(res)

def arima3(month):
    mdict = {"Jan": 1, "Feb": 2, "Mar": 3, "Apr": 4, "May": 5, "Jun": 6, "Jul": 7, "Aug": 8, "Sep": 9, "Oct": 10, "Nov": 11, "Dec": 12}
    col_monthly = db['monthly']
    monthlyGrossSet = []
    for y in range(2008, 2019):
        for record in col_monthly.find({"Year": str(y)}):
            mt = record['month']
            yr = record['Year']
            if mdict[mt] >= mdict[month] and int(yr) >= 2018:
                continue
            # print(mt, yr)
            avgGross = record['MovieAvg($)']
            monthlyGrossSet.append(float(avgGross))
    print(monthlyGrossSet)
    # fit model
    model = ARIMA(monthlyGrossSet, order=(1, 1, 1))
    model_fit = model.fit(disp=False)
    # make prediction
    yhat = model_fit.predict(len(monthlyGrossSet), len(monthlyGrossSet), typ='levels')
    print(yhat)


if __name__ == "__main__":
    # there are 52 records(weeks) for each year
    testmonth = ["Jan", "Mar", "May", "Jul", "Sep", "Oct", "Dec"]
    # for month in testmonth:
        # monthlySimpleAvg(month)
        # wma1(month)
        # wma2(month)
        # ar1(month)
        # movingAverage(month)
        # arma1((month))
        # arima1(month)
        # ar3(month)
        # ma3(month)
        # arma3(month)
        # arima3(month)

    set = [1, 2, 3, 4, 5, 6]
    # fit model
    model = ARMA(set, order=(0, 1))
    model_fit = model.fit(disp=False)
    # make prediction
    res = model_fit.predict(len(set), len(set))
    print(res)


