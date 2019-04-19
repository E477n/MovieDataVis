import pymongo
from statsmodels.tsa.ar_model import AR
from statsmodels.tsa.arima_model import ARMA
from statsmodels.tsa.arima_model import ARIMA
from statsmodels.tsa.statespace.sarimax import SARIMAX

client = pymongo.MongoClient(host='127.0.0.1', port=27017)
db = client['movie_db']

#startyear = 8 means using data from 2008
#saved data is from 2002 to 2018
startYear = 8

def dailySimpleAvg():
    col_daily = db['daily']
    dailyGrossSet = []
    for record in col_daily.find({"Date": "Dec. 28"}):
        year = record['Year']
        movieNumber = record['MoviesTracked']
        gross = record['Gross($)'].replace(",", "")
        dailyGrossSet.append(int(gross) / int(movieNumber))
    simplesum = 0
    for i in range(startYear,startYear+10):
        simplesum += dailyGrossSet[i-2]
    print(dailyGrossSet)
    print(simplesum/10)

def dailyMovingAvg1():
    col_daily = db['daily']
    dailyGrossSet = []
    for record in col_daily.find({"Date": "Dec. 28"}):
        year = record['Year']
        movieNumber = record['MoviesTracked']
        gross = record['Gross($)'].replace(",", "")
        dailyGrossSet.append(int(gross) / int(movieNumber))
    sum = 0 #sum of 8-17
    for i in range(startYear,startYear+10):
        sum += i
    movingAvg = 0
    for i in range(startYear,startYear+10):
        print(dailyGrossSet[i-2])
        movingAvg += dailyGrossSet[i-2]*i/sum
    print(sum)
    print(dailyGrossSet)
    print(movingAvg)

def dailyMovingAvg2():
    col_daily = db['daily']
    dailyGrossSet = []
    for record in col_daily.find({"Date": "Dec. 28"}):
        year = record['Year']
        movieNumber = record['MoviesTracked']
        gross = record['Gross($)'].replace(",", "")
        dailyGrossSet.append(int(gross) / int(movieNumber))
    sum = 55
    movingAvg = 0
    for i in range(startYear,startYear+10):
        print(dailyGrossSet[i-2])
        movingAvg += dailyGrossSet[i-2]*(i-7)/sum
    print(sum)
    print(dailyGrossSet)
    print(movingAvg)

def autoRegression():
    col_daily = db['daily']
    dailyGrossSet = []
    for record in col_daily.find({"Date": "Dec. 28"}):
        year = record['Year']
        movieNumber = record['MoviesTracked']
        gross = record['Gross($)'].replace(",", "")
        dailyGrossSet.append(int(gross) / int(movieNumber))
    del dailyGrossSet[len(dailyGrossSet)-1]
    print(dailyGrossSet)
    # fit model
    model = AR(dailyGrossSet)
    model_fit = model.fit()
    # make prediction
    res = model_fit.predict(len(dailyGrossSet), len(dailyGrossSet))
    print(res)

def movingAverage():
    col_daily = db['daily']
    dailyGrossSet = []
    for record in col_daily.find({"Date": "Nov. 30"}):
        year = record['Year']
        movieNumber = record['MoviesTracked']
        gross = record['Gross($)'].replace(",", "")
        dailyGrossSet.append(int(gross) / int(movieNumber))
    print(dailyGrossSet)
    del dailyGrossSet[len(dailyGrossSet)-1]
    print(dailyGrossSet)
    # fit model
    model = ARMA(dailyGrossSet, order=(0, 1))
    model_fit = model.fit(disp=False)
    # make prediction
    res = model_fit.predict(len(dailyGrossSet), len(dailyGrossSet))
    print(res)

def autoregressiveMovingAverage():
    col_daily = db['daily']
    dailyGrossSet = []
    for record in col_daily.find({"Date": "May 4"}):
        year = record['Year']
        movieNumber = record['MoviesTracked']
        gross = record['Gross($)'].replace(",", "")
        dailyGrossSet.append(int(gross) / int(movieNumber))
    print(dailyGrossSet)
    del dailyGrossSet[len(dailyGrossSet)-1]
    print(dailyGrossSet)
    # fit model
    model = ARMA(dailyGrossSet, order=(2, 1))
    model_fit = model.fit(disp=False)
    # make prediction
    res = model_fit.predict(len(dailyGrossSet), len(dailyGrossSet))
    print(res)

def autoregressiveIntegratedMovingAverage(date):
    col_daily = db['daily']
    dailyGrossSet = []
    for record in col_daily.find({"Date": date}):
        year = record['Year']
        movieNumber = record['MoviesTracked']
        gross = record['Gross($)'].replace(",", "")
        dailyGrossSet.append(int(gross) / int(movieNumber))
    print(dailyGrossSet)
    del dailyGrossSet[len(dailyGrossSet)-1]
    print(dailyGrossSet)

    # fit model
    model = ARIMA(dailyGrossSet, order=(1, 1, 1))
    model_fit = model.fit(disp=False)
    # make prediction
    yhat = model_fit.predict(len(dailyGrossSet), len(dailyGrossSet), typ='levels')
    print(yhat)

def seasonalAutoregressiveIntegratedMovingAverage(date):
    col_daily = db['daily']
    dailyGrossSet = []
    for record in col_daily.find({"Date": date}):
        year = record['Year']
        movieNumber = record['MoviesTracked']
        gross = record['Gross($)'].replace(",", "")
        dailyGrossSet.append(int(gross) / int(movieNumber))
    print(dailyGrossSet)
    del dailyGrossSet[len(dailyGrossSet)-1]
    print(dailyGrossSet)

    # fit model
    model = SARIMAX(dailyGrossSet, order=(1, 1, 1), seasonal_order=(1, 1, 1, 1))
    model_fit = model.fit(disp=False)
    # make prediction
    yhat = model_fit.predict(len(dailyGrossSet), len(dailyGrossSet))
    print(yhat)


#using data from Jan 1 to Apr 30, 2018 to predict May 1
def dailySimpleAvg2(day):
    col_daily = db['daily']
    dailyGrossSet = []
    for record in col_daily.find({"Year": 2018}):
        year = record['Year']
        movieNumber = record['MoviesTracked']
        gross = record['Gross($)'].replace(",", "")
        dailyGrossSet.append(int(gross) / int(movieNumber))
    print(dailyGrossSet[day])
    dailyGrossSet = dailyGrossSet[0: day]
    print(dailyGrossSet)

    simplesum = 0
    for i in range(0, day):
        simplesum += dailyGrossSet[i]
    print(simplesum/day)


def autoRegression2(day):
    col_daily = db['daily']
    dailyGrossSet = []
    for record in col_daily.find({"Year": 2018}):
        year = record['Year']
        movieNumber = record['MoviesTracked']
        gross = record['Gross($)'].replace(",", "")
        dailyGrossSet.append(int(gross) / int(movieNumber))
    print(dailyGrossSet[day])
    dailyGrossSet = dailyGrossSet[0: day]
    print(dailyGrossSet)
    # fit model
    model = AR(dailyGrossSet)
    model_fit = model.fit()
    # make prediction
    res = model_fit.predict(len(dailyGrossSet), len(dailyGrossSet))
    print(res)

def movingAverage2(day):
    col_daily = db['daily']
    dailyGrossSet = []
    for record in col_daily.find({"Year": 2018}):
        year = record['Year']
        movieNumber = record['MoviesTracked']
        gross = record['Gross($)'].replace(",", "")
        dailyGrossSet.append(int(gross) / int(movieNumber))
    print(dailyGrossSet[day])
    dailyGrossSet = dailyGrossSet[0: day]
    print(dailyGrossSet)
    # fit model
    model = ARMA(dailyGrossSet, order=(0, 1))
    model_fit = model.fit(disp=False)
    # make prediction
    res = model_fit.predict(len(dailyGrossSet), len(dailyGrossSet))
    print(res)

def autoregressiveMovingAverage2(day):
    col_daily = db['daily']
    dailyGrossSet = []
    for record in col_daily.find({"Year": 2018}):
        year = record['Year']
        movieNumber = record['MoviesTracked']
        gross = record['Gross($)'].replace(",", "")
        dailyGrossSet.append(int(gross) / int(movieNumber))
    print(dailyGrossSet[day])
    dailyGrossSet = dailyGrossSet[0: day]
    print(dailyGrossSet)
    # fit model
    model = ARMA(dailyGrossSet, order=(2, 1))
    model_fit = model.fit(disp=False)
    # make prediction
    res = model_fit.predict(len(dailyGrossSet), len(dailyGrossSet))
    print(res)

def seasonalAutoregressiveIntegratedMovingAverage2(day):
    col_daily = db['daily']
    dailyGrossSet = []
    for record in col_daily.find({"Year": 2018}):
        year = record['Year']
        movieNumber = record['MoviesTracked']
        gross = record['Gross($)'].replace(",", "")
        dailyGrossSet.append(int(gross) / int(movieNumber))
    print(dailyGrossSet[day])
    dailyGrossSet = dailyGrossSet[0: day]
    print(dailyGrossSet)
    # fit model
    model = SARIMAX(dailyGrossSet, order=(1, 1, 1), seasonal_order=(1, 1, 1, 1))
    model_fit = model.fit(disp=False)
    # make prediction
    yhat = model_fit.predict(len(dailyGrossSet), len(dailyGrossSet))
    print(yhat)

# using data from Jan 1, 2008 to a specific date on 2018
def dailySimpleAvg3(day):
    col_daily = db['daily']
    dailyGrossSet = []
    for y in range(2008, 2018):
        for record in col_daily.find({"Year": y}):
            movieNumber = record['MoviesTracked']
            gross = record['Gross($)'].replace(",", "")
            dailyGrossSet.append(int(gross) / int(movieNumber))
    daycount = 0
    for record in col_daily.find({"Year": 2018}):
        movieNumber = record['MoviesTracked']
        gross = record['Gross($)'].replace(",", "")
        dailyGrossSet.append(int(gross) / int(movieNumber))
        daycount += 1
        if daycount >= day:
            break
    print(dailyGrossSet)
    simplesum = 0
    for i in dailyGrossSet:
        simplesum += i
    print(simplesum/len(dailyGrossSet))


def autoRegression3(day):
    col_daily = db['daily']
    dailyGrossSet = []
    for y in range(2008, 2018):
        for record in col_daily.find({"Year": y}):
            movieNumber = record['MoviesTracked']
            gross = record['Gross($)'].replace(",", "")
            dailyGrossSet.append(int(gross) / int(movieNumber))
    daycount = 0
    for record in col_daily.find({"Year": 2018}):
        movieNumber = record['MoviesTracked']
        gross = record['Gross($)'].replace(",", "")
        dailyGrossSet.append(int(gross) / int(movieNumber))
        daycount += 1
        if daycount >= day:
            break
    print(dailyGrossSet)
    # fit model
    model = AR(dailyGrossSet)
    model_fit = model.fit()
    # make prediction
    res = model_fit.predict(len(dailyGrossSet), len(dailyGrossSet))
    print(res)

def movingAverage3(day):
    col_daily = db['daily']
    dailyGrossSet = []
    for y in range(2008, 2018):
        for record in col_daily.find({"Year": y}):
            movieNumber = record['MoviesTracked']
            gross = record['Gross($)'].replace(",", "")
            dailyGrossSet.append(int(gross) / int(movieNumber))
    daycount = 0
    for record in col_daily.find({"Year": 2018}):
        movieNumber = record['MoviesTracked']
        gross = record['Gross($)'].replace(",", "")
        dailyGrossSet.append(int(gross) / int(movieNumber))
        daycount += 1
        if daycount >= day:
            break
    print(dailyGrossSet)
    # fit model
    model = ARMA(dailyGrossSet, order=(0, 1))
    model_fit = model.fit(disp=False)
    # make prediction
    res = model_fit.predict(len(dailyGrossSet), len(dailyGrossSet))
    print(res)

def autoregressiveMovingAverage3(day):
    col_daily = db['daily']
    dailyGrossSet = []
    for y in range(2008, 2018):
        for record in col_daily.find({"Year": y}):
            movieNumber = record['MoviesTracked']
            gross = record['Gross($)'].replace(",", "")
            dailyGrossSet.append(int(gross) / int(movieNumber))
    daycount = 0
    for record in col_daily.find({"Year": 2018}):
        movieNumber = record['MoviesTracked']
        gross = record['Gross($)'].replace(",", "")
        dailyGrossSet.append(int(gross) / int(movieNumber))
        daycount += 1
        if daycount >= day:
            break
    print(dailyGrossSet)
    # fit model
    model = ARMA(dailyGrossSet, order=(2, 1))
    model_fit = model.fit(disp=False)
    # make prediction
    res = model_fit.predict(len(dailyGrossSet), len(dailyGrossSet))
    print(res)

def autoregressiveIntegratedMovingAverage3(day):
    col_daily = db['daily']
    dailyGrossSet = []
    for y in range(2008, 2018):
        for record in col_daily.find({"Year": y}):
            movieNumber = record['MoviesTracked']
            gross = record['Gross($)'].replace(",", "")
            dailyGrossSet.append(int(gross) / int(movieNumber))
    daycount = 0
    for record in col_daily.find({"Year": 2018}):
        movieNumber = record['MoviesTracked']
        gross = record['Gross($)'].replace(",", "")
        dailyGrossSet.append(int(gross) / int(movieNumber))
        daycount += 1
        if daycount >= day:
            break
    print(dailyGrossSet)
    # fit model
    model = ARIMA(dailyGrossSet, order=(1, 1, 1))
    model_fit = model.fit(disp=False)
    # make prediction
    yhat = model_fit.predict(len(dailyGrossSet), len(dailyGrossSet), typ='levels')
    print(yhat)





if __name__ == "__main__":
    testDateSet = ["May 1", "May 4", "Jul. 27", "Nov. 21", "Nov. 30", "Dec. 24", "Dec. 28"]
    testDateSet2 = [120, 123, 207, 324, 333, 357, 361]
    # dailySimpleAvg()
    # dailyMovingAvg1()
    # dailyMovingAvg2()
    # autoRegression()
    # movingAverage()
    # autoregressiveMovingAverage()
    # for date in testDateSet:
    #     # autoregressiveIntegratedMovingAverage(date)
    #     seasonalAutoregressiveIntegratedMovingAverage(date)
    for day in testDateSet2:
        # dailySimpleAvg2(day)
        # autoRegression2(day)
        # movingAverage2(day)
        # autoregressiveMovingAverage2(day)
        # seasonalAutoregressiveIntegratedMovingAverage2(day)

        dailySimpleAvg3(day)
        # autoRegression3(day)
        # movingAverage3(day)
        # autoregressiveMovingAverage3(day)
        # autoregressiveIntegratedMovingAverage3(day)

