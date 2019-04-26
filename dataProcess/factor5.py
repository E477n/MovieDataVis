import pymongo

client = pymongo.MongoClient(host='127.0.0.1', port=27017)
db = client['movie_db']

col_wl = db['weekly']

def weeklyGrossTrendByYear():
    years = ["2015", "2016", "2017", "2018"]
    for year in years:
        for record in col_wl.find({"Year": year}):
            print(record["Week#"])

if __name__ == "__main__":
    weeklyGrossTrendByYear()