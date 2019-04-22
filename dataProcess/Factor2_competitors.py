import pymongo
from bson.son import SON
from dateutil import parser

client = pymongo.MongoClient(host='127.0.0.1', port=27017)
db = client['movie_db']

col_cd = db['competitor_detail']

def groupbyDate():
    # groupby release date and count
    # sort by release date
    groupby = 'ReleaseDate'
    group = {
        '_id': "$%s" % (groupby if groupby else None),
        'count': {'$sum': 1}

    }
    sort = {
        'ReleaseDate': 1
    }
    ret = col_cd.aggregate(
        [
            {'$group': group},
            {"$sort": SON([("ReleaseDate", 1), ("_id", -1)])}
        ]
    )
    for record in ret:
        print(record)

# Group by date and count genre
# create new collection competitor_count
def groupbyDateandCountGenre():
    col_cc = db['competitor_count']

    groupby = 'ReleaseDate'
    group = {
        '_id': "$%s" % (groupby if groupby else None),
        'count': {'$sum': 1},
    }
    ret = col_cd.aggregate(
        [
            {'$group': group},
            {'$sort': SON([("ReleaseDate", 1), ("_id", -1)])}
        ]
    )

    for record in ret:
        date = record['_id']
        row = {}
        genre = {}
        for r in col_cd.find({'ReleaseDate': date}):
            print(date)
            if r['Genre'] not in genre.keys():
                genre.update({r['Genre']: 1})
            else:
                n = genre[r['Genre']]
                n += 1
                genre.update({r['Genre']: n})
        for key in genre:
            row = {"ReleaseDate": date,
                   "Genre": key,
                   "Count": genre[key]}
            col_cc.insert(row)

# transfer release date from String to Datetime
def updateDate():
    for record in col_cd.find():
        dateStr = record['ReleaseDate']
        movieName = record['Movie']
        myDatetime = parser.parse(dateStr)
        col_cd.update_one({"Movie": movieName}, {"$set": {"ReleaseDate": myDatetime}}, upsert=False)

if __name__ == "__main__":
    # updateDate()
    groupbyDate()
    # groupbyDateandCountGenre()
