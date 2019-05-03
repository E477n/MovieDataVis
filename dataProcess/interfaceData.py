import pymongo

client = pymongo.MongoClient(host='127.0.0.1', port=27017)
db = client['movie_db']

col_fr = db['franchise']