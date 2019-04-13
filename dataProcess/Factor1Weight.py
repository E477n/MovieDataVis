import pymongo

client = pymongo.MongoClient(host='127.0.0.1', port=27017)
db = client['movie_db']

#startyear = 8 means using data from 2008
#saved data is from 2002 to 2018
startYear = 8

def calculateDailyAvg():
    col_daily = db['daily']
    dailyGrossSet = []
    for record in col_daily.find({"Date": "May 1"}):
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

    # # simple average
    # simplesum = 0
    # for i in range(startYear,startYear+10):
    #     simplesum += dailyGrossSet[i-startYear]
    # print(simplesum/10)

    #another try on weight



if __name__ == "__main__":
    calculateDailyAvg()