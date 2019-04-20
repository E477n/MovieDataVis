import pymongo
from statsmodels.tsa.ar_model import AR
from statsmodels.tsa.arima_model import ARMA
from statsmodels.tsa.arima_model import ARIMA
from statsmodels.tsa.statespace.sarimax import SARIMAX

client = pymongo.MongoClient(host='127.0.0.1', port=27017)
db = client['movie_db']

def calculateActualValue(week):
    col_weekly = db['weekly']
    resultSet = {}
    for record in col_weekly.find({"Year": "2018", "Week#": week}):
        og = record['OverallGross($)'].replace(",", "")
        tm = record['TotalMovies']
        resultSet[week] = int(og)/int(tm)
    print(resultSet)

#data set 1
def weeklySimpleAvg(week):
    col_weekly = db['weekly']
    weeklyGrossSet = []
    simplesum = 0
    for record in col_weekly.find({"Week#": week}):
        year = record['Year']
        if int(year) >= 2018 or int(year) < 2008:
            continue
        og = record['OverallGross($)'].replace(",", "")
        tm = record['TotalMovies']
        weeklyGrossSet.append(int(og)/int(tm))
        simplesum += int(og)/int(tm)
    print(simplesum/len(weeklyGrossSet))

def weeklyWeightedMA1(week):
    col_weekly = db['weekly']
    weeklyGrossSet = []
    weightedSum = 0
    i = 8
    sum = 0
    for i in range (8, 18):
        sum += i
    i = 17 #the result from db was from 2017 to 2008
    for record in col_weekly.find({"Week#": week}):
        year = record['Year']
        if int(year) >= 2018 or int(year) < 2008:
            continue
        og = record['OverallGross($)'].replace(",", "")
        tm = record['TotalMovies']
        weightedSum += int(og)/int(tm) * i/sum
        i -= 1
    print(weightedSum, sum)

def weeklyWeightedMA2(week):
    col_weekly = db['weekly']
    weeklyGrossSet = []
    weightedSum = 0
    sum = 0
    for i in range (1, 11):
        sum += i
    i = 17 #the result from db was from 2017 to 2008
    for record in col_weekly.find({"Week#": week}):
        year = record['Year']
        if int(year) >= 2018 or int(year) < 2008:
            continue
        og = record['OverallGross($)'].replace(",", "")
        tm = record['TotalMovies']
        weightedSum += int(og)/int(tm) * (i-7)/sum
        i -= 1
    print(weightedSum, sum)

def movingAverage(week):
    col_weekly = db['weekly']
    weeklyGrossSet = []
    for record in col_weekly.find({"Week#": week}):
        year = record['Year']
        if int(year) >= 2018 or int(year) < 2008:
            continue
        og = record['OverallGross($)'].replace(",", "")
        tm = record['TotalMovies']
        weeklyGrossSet.append(int(og)/int(tm))
    #data from 2017 to 2008 need to be reversed
    weeklyGrossSet.reverse()
    print(weeklyGrossSet)
    # fit model
    model = ARMA(weeklyGrossSet, order=(0, 1))
    model_fit = model.fit(disp=False)
    # make prediction
    res = model_fit.predict(len(weeklyGrossSet), len(weeklyGrossSet))
    print(res)

def ar1(week):
    col_weekly = db['weekly']
    weeklyGrossSet = []
    for record in col_weekly.find({"Week#": week}):
        year = record['Year']
        if int(year) >= 2018 or int(year) < 2008:
            continue
        og = record['OverallGross($)'].replace(",", "")
        tm = record['TotalMovies']
        weeklyGrossSet.append(int(og)/int(tm))
    #data from 2017 to 2008 need to be reversed
    weeklyGrossSet.reverse()
    print(weeklyGrossSet)
    # fit model
    model = AR(weeklyGrossSet)
    model_fit = model.fit()
    # make prediction
    res = model_fit.predict(len(weeklyGrossSet), len(weeklyGrossSet))
    print(res)

# data set 2
def sa2(week):
    col_weekly = db['weekly']
    weeklyGrossSet = []
    sum = 0
    for record in col_weekly.find({"Year": "2018"}):
        wk = record['Week#']
        if int(wk) >= week:
            break
        og = record['OverallGross($)'].replace(",", "")
        tm = record['TotalMovies']
        weeklyGrossSet.append(int(og)/int(tm))
        sum += int(og)/int(tm)
    print(weeklyGrossSet)
    print(sum/len(weeklyGrossSet))

def ar2(week):
    col_weekly = db['weekly']
    weeklyGrossSet = []
    for record in col_weekly.find({"Year": "2018"}):
        wk = record['Week#']
        if int(wk) >= week:
            break
        og = record['OverallGross($)'].replace(",", "")
        tm = record['TotalMovies']
        weeklyGrossSet.append(int(og)/int(tm))
    print(weeklyGrossSet)
    # fit model
    model = AR(weeklyGrossSet)
    model_fit = model.fit()
    # make prediction
    res = model_fit.predict(len(weeklyGrossSet), len(weeklyGrossSet))
    print(res)

def ma2(week):
    col_weekly = db['weekly']
    weeklyGrossSet = []
    for record in col_weekly.find({"Year": "2018"}):
        wk = record['Week#']
        if int(wk) >= week:
            break
        og = record['OverallGross($)'].replace(",", "")
        tm = record['TotalMovies']
        weeklyGrossSet.append(int(og)/int(tm))
    print(weeklyGrossSet)
    # fit model
    model = ARMA(weeklyGrossSet, order=(0, 1))
    model_fit = model.fit(disp=False)
    # make prediction
    res = model_fit.predict(len(weeklyGrossSet), len(weeklyGrossSet))
    print(res)


def arma2(week):
    col_weekly = db['weekly']
    weeklyGrossSet = []
    for record in col_weekly.find({"Year": "2018"}):
        wk = record['Week#']
        if int(wk) >= week:
            break
        og = record['OverallGross($)'].replace(",", "")
        tm = record['TotalMovies']
        weeklyGrossSet.append(int(og)/int(tm))
    print(weeklyGrossSet)
    # fit model
    model = ARMA(weeklyGrossSet, order=(2, 1))
    model_fit = model.fit(disp=False)
    # make prediction
    res = model_fit.predict(len(weeklyGrossSet), len(weeklyGrossSet))
    print(res)

def arima2(week):
    col_weekly = db['weekly']
    weeklyGrossSet = []
    for record in col_weekly.find({"Year": "2018"}):
        wk = record['Week#']
        if int(wk) >= week:
            break
        og = record['OverallGross($)'].replace(",", "")
        tm = record['TotalMovies']
        weeklyGrossSet.append(int(og)/int(tm))
    print(weeklyGrossSet)

    # fit model
    model = ARIMA(weeklyGrossSet, order=(1, 1, 1))
    model_fit = model.fit(disp=False)
    # make prediction
    yhat = model_fit.predict(len(weeklyGrossSet), len(weeklyGrossSet), typ='levels')
    print(yhat)

# data set 3
def ar3(week):
    col_weekly = db['weekly']
    weeklyGrossSet = []
    for y in range(2008, 2019):
        for record in col_weekly.find({"Year": str(y)}):
            wk = record['Week#']
            yr = record['Year']
            if int(wk) >= week and int(yr) >= 2018:
                break
            og = record['OverallGross($)'].replace(",", "")
            tm = record['TotalMovies']
            weeklyGrossSet.append(int(og)/int(tm))
    print(weeklyGrossSet)
    # fit model
    model = AR(weeklyGrossSet)
    model_fit = model.fit()
    # make prediction
    res = model_fit.predict(len(weeklyGrossSet), len(weeklyGrossSet))
    print(res)

def ma3(week):
    col_weekly = db['weekly']
    weeklyGrossSet = []
    for y in range(2008, 2019):
        for record in col_weekly.find({"Year": str(y)}):
            wk = record['Week#']
            yr = record['Year']
            if int(wk) >= week and int(yr) >= 2018:
                break
            og = record['OverallGross($)'].replace(",", "")
            tm = record['TotalMovies']
            weeklyGrossSet.append(int(og)/int(tm))
    print(weeklyGrossSet)
    # fit model
    model = ARMA(weeklyGrossSet, order=(0, 1))
    model_fit = model.fit(disp=False)
    # make prediction
    res = model_fit.predict(len(weeklyGrossSet), len(weeklyGrossSet))
    print(res)

def arma3(week):
    col_weekly = db['weekly']
    weeklyGrossSet = []
    for y in range(2008, 2019):
        for record in col_weekly.find({"Year": str(y)}):
            wk = record['Week#']
            yr = record['Year']
            if int(wk) >= week and int(yr) >= 2018:
                break
            og = record['OverallGross($)'].replace(",", "")
            tm = record['TotalMovies']
            weeklyGrossSet.append(int(og)/int(tm))
    print(weeklyGrossSet)
    # fit model
    model = ARMA(weeklyGrossSet, order=(2, 1))
    model_fit = model.fit(disp=False)
    # make prediction
    res = model_fit.predict(len(weeklyGrossSet), len(weeklyGrossSet))
    print(res)

def arima3(week):
    col_weekly = db['weekly']
    weeklyGrossSet = []
    for y in range(2008, 2019):
        for record in col_weekly.find({"Year": str(y)}):
            wk = record['Week#']
            yr = record['Year']
            if int(wk) >= week and int(yr) >= 2018:
                break
            og = record['OverallGross($)'].replace(",", "")
            tm = record['TotalMovies']
            weeklyGrossSet.append(int(og)/int(tm))
    print(weeklyGrossSet)
    # fit model
    model = ARIMA(weeklyGrossSet, order=(1, 1, 1))
    model_fit = model.fit(disp=False)
    # make prediction
    yhat = model_fit.predict(len(weeklyGrossSet), len(weeklyGrossSet), typ='levels')
    print(yhat)


if __name__ == "__main__":
    # there are 52 records(weeks) for each year
    testweek = [7, 15, 21, 28, 36, 42, 51]
    testweek2 = [15, 21, 28, 36, 42, 51]
    for week in testweek:
        # calculateActualValue(week)
        # weeklySimpleAvg(week)
        # weeklyWeightedMA1(week)
        # weeklyWeightedMA2(week)
        # movingAverage(week)
        # ar1(week)
        # sa2(week)
        # ar2(week)
        # ma2(week)
        # arma2(week)
        # arima2(week)
        # ar3(week)
        # ma3(week)
        # arma3(week)
        arima2(week)