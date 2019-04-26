import pymongo
from dateutil import parser

client = pymongo.MongoClient(host='127.0.0.1', port=27017)
db = client['movie_db']

col_bg = db['budget']

# data collected by hand
set = [
    {'title': 'Justice League', 'budget': 300, 'ReleaseDate': parser.parse('2017/11/17') },
    {'title': 'Solo: A Star Wars Story', 'budget': 275, 'ReleaseDate': parser.parse('2018/05/25')},
    {'title': 'John Carter', 'budget': 264, 'ReleaseDate': parser.parse('2012/02/22')},
    {'title': 'Batman v Superman: Dawn of Justice', 'budget': 263, 'ReleaseDate': parser.parse('2016/03/25')},
    {'title': 'Star Wars: The Last Jedi', 'budget': 262, 'ReleaseDate': parser.parse('2017/12/15')},
    {'title': 'Tangled', 'budget': 260, 'ReleaseDate': parser.parse('2010/11/24')},
    {'title': 'Star Wars: The Force Awakens', 'budget': 259, 'ReleaseDate': parser.parse('2015/12/18')},
    {'title': 'Spider-Man 3', 'budget': 258, 'ReleaseDate': parser.parse('2007/05/04')},
    {'title': 'Beauty and the Beast', 'budget': 255, 'ReleaseDate': parser.parse('2017/03/17')},
    {'title': 'Harry Potter and the Half-Blood Prince', 'budget': 250, 'ReleaseDate': parser.parse('2009/07/15')},
    {'title': 'Transformers: The Last Knight', 'budget': 239, 'ReleaseDate': parser.parse('2017/06/21')},
    {'title': 'Avatar', 'budget': 237, 'ReleaseDate': parser.parse('2009/12/18')},
    {'title': 'The Dark Knight Rises', 'budget': 230, 'ReleaseDate': parser.parse('2012/07/20')},
    {'title': 'Spectre', 'budget': 230, 'ReleaseDate': parser.parse('2015/11/06')},
    {'title': 'Captain America: Civil War', 'budget': 230, 'ReleaseDate': parser.parse('2016/05/06')},
    {'title': 'The Fate of the Furious', 'budget': 230, 'ReleaseDate': parser.parse('2017/04/14')},
    {'title': 'Pirates of the Caribbean: Dead Men Tell No Tales', 'budget': 230, 'ReleaseDate': parser.parse('2017/05/26')},
    {'title': 'Maleficent', 'budget': 226, 'ReleaseDate': parser.parse('2014/05/30')},
    {'title': 'The Chronicles of Narnia: Prince Caspian', 'budget': 225, 'ReleaseDate': parser.parse('2008/06/26')},
    {'title': 'The Lone Ranger', 'budget': 225, 'ReleaseDate': parser.parse('2013/07/03')},
    {'title': 'Pirates of the Caribbean: Dead Mans Chest', 'budget': 225, 'ReleaseDate': parser.parse('2006/07/07')},
    {'title': 'Man of Steel', 'budget': 225, 'ReleaseDate': parser.parse('2013/06/14')},
    {'title': 'The Avengers', 'budget': 220, 'ReleaseDate': parser.parse('2012/05/04')},
    {'title': 'Rogue One', 'budget': 220, 'ReleaseDate': parser.parse('2016/12/16')},
    {'title': 'The Hobbit: The Desolation of Smaug', 'budget': 217, 'ReleaseDate': parser.parse('2013/12/13')},
    {'title': 'Men in Black 3', 'budget': 215, 'ReleaseDate': parser.parse('2012/05/25')},
    {'title': 'Oz the Great and Powerful', 'budget': 215, 'ReleaseDate': parser.parse('2013/03/08')},
    {'title': 'X-Men: The Last Stand', 'budget': 210, 'ReleaseDate': parser.parse('2006/05/26')},
    {'title': 'Transformers: Age of Extinction', 'budget': 210, 'ReleaseDate': parser.parse('2014/06/27')},
    {'title': 'Battleship', 'budget': 209, 'ReleaseDate': parser.parse('2012/05/18')},
    {'title': 'Dawn of the Planet of the Apes', 'budget': 209, 'ReleaseDate': parser.parse('2014/07/11')},
    {'title': 'The Hobbit: The Battle of the Five Armies', 'budget': 209, 'ReleaseDate': parser.parse('2017/12/17')},
    {'title': 'King Kong', 'budget': 207, 'ReleaseDate': parser.parse('2005/12/14')},
    {'title': 'X-Men: Days of Future Past', 'budget': 205, 'ReleaseDate': parser.parse('2014/05/23')},
    {'title': 'Superman Returns', 'budget': 204, 'ReleaseDate': parser.parse('2006/06/28')},
    {'title': 'Titanic', 'budget': 200, 'ReleaseDate': parser.parse('1997/12/19')},
    {'title': 'Spider-Man 2', 'budget': 200, 'ReleaseDate': parser.parse('2004/06/30')},
    {'title': 'Quantum of Solace', 'budget': 200, 'ReleaseDate': parser.parse('2008/11/14')},
    {'title': 'erminator Salvation', 'budget': 200, 'ReleaseDate': parser.parse('2009/05/21')},
    {'title': 'Transformers: Revenge of the Fallen', 'budget': 200, 'ReleaseDate': parser.parse('2009/06/24')},
    {'title': '2012', 'budget': 200, 'ReleaseDate': parser.parse('2009/11/13')},
    {'title': 'Toy Story 3', 'budget': 200, 'ReleaseDate': parser.parse('2010/06/18')},
    {'title': 'Green Lantern', 'budget': 200, 'ReleaseDate': parser.parse('2011/06/17')},
    {'title': 'Cars 2', 'budget': 200, 'ReleaseDate': parser.parse('2011/06/24')},
    {'title': 'The Amazing Spider-Man', 'budget': 200, 'ReleaseDate': parser.parse('2012/07/03')},
    {'title': 'The Hobbit: An Unexpected Journey', 'budget': 200, 'ReleaseDate': parser.parse('2012/12/14')},
    {'title': 'Iron Man 3', 'budget': 200, 'ReleaseDate': parser.parse('2013/05/03')},
    {'title': 'Monsters University', 'budget': 200, 'ReleaseDate': parser.parse('2013/06/21')},
    {'title': 'The Amazing Spider-Man 2', 'budget': 200, 'ReleaseDate': parser.parse('2014/05/02')},
    {'title': 'Exodus: Gods and Kings', 'budget': 200, 'ReleaseDate': parser.parse('2014/12/12')},
    {'title': 'Guardians of the Galaxy Vol. 2', 'budget': 200, 'ReleaseDate': parser.parse('2017/05/05')},
    {'title': 'Black Panther', 'budget': 200, 'ReleaseDate': parser.parse('2018/02/16')},
    {'title': 'Incredibles 2', 'budget': 200, 'ReleaseDate': parser.parse('2018/06/15')},
    {'title': 'Fantastic Beasts: The Crimes of Grindelwald', 'budget': 200, 'ReleaseDate': parser.parse('2018/11/16')},
]

for record in set:
    col_bg.insert_one(record)