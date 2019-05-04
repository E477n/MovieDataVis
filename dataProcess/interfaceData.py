import pymongo

client = pymongo.MongoClient(host='127.0.0.1', port=27017)
db = client['movie_db']

col_gn = db['genres']
col_fr = db['franchise']

# find all genres
def findAllGenre():
    genre_set = []
    for record in col_gn.find():
        row = {'label': record['Genre'], 'value': record['Genre']}
        genre_set.append(row)
    return genre_set

# find all franchise
def findAllFran():
    fran_set = []
    for record in col_fr.find():
        row = {'label': record['Franchise'], 'value': record['Franchise']}
        fran_set.append(row)
    return fran_set

if __name__ == "__main__":
    print(findAllGenre())