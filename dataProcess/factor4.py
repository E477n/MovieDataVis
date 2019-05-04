import pymongo

client = pymongo.MongoClient(host='127.0.0.1', port=27017)
db = client['movie_db']

col_fr = db['franchise']
col_gd = db['genre_details']

def findFranchise(franchise):
    wk = None
    for record in col_fr.find({'Franchise': franchise}):
        movie_name = record['#1Picture']
        for item in col_gd.find({'Title': movie_name}):
            wk = item['week#']
    return  wk