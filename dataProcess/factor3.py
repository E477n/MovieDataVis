import pymongo
import datetime

client = pymongo.MongoClient(host='127.0.0.1', port=27017)
db = client['movie_db']

col_gd = db['genre_details']

def updateWeek():
    for record in col_gd.find():
        id = record['_id']
        rd = record['Date']
        rd = rd.split('/')
        print(rd)
        if 0 <= int(rd[2]) <= 18:
            rd[2] = "20" + rd[2]
        else:
            rd[2] = "19" + rd[2]
        print(rd)
        dt = datetime.date(int(rd[2]), int(rd[0]), int(rd[1]))
        wk = dt.isocalendar()[1]
        print(wk)
        col_gd.find_one_and_update({"_id": id},
                            {"$set": {"week#": wk}})

def calTotalGrossofSameGenreSameWeek(dateSet, genre):
    res = []
    for day in dateSet:
        # convert date to corresponding week
        rd = day.split('-')
        dt = datetime.date(int(rd[0]), int(rd[1]), int(rd[2]))
        wk = dt.isocalendar()[1]
        weeksum = 0
        for record in col_gd.find({"week#": wk}):
            if record["Genre"] in genre:
                weeksum += record["OpeningGross($)"]
        res.append(weeksum)
    print(res)

if __name__ == "__main__":
    # updateWeek()
    calTotalGrossofSameGenreSameWeek([12, 13, 14, 15, 16, 17], "Animation")