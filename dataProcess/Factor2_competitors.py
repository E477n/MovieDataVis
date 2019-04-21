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
