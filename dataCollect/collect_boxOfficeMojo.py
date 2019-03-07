# domestic yearly
import requests
from requests.exceptions import RequestException
import re
from pyquery import PyQuery as pq
import pymongo

# def getPage(url):
#     res = requests.get(url)
#     res.encoding = 'utf-8'
#     try:
#         if res.status_code == 200:
#             return res.text
#         else:
#             return None
#     except RequestException:
#         return None
#
# def selectInfo(html):
#     pattern = re.compile('\d+')
#     movies_info = re.findall(pattern, html)
#     return movies_info

client = pymongo.MongoClient(host='127.0.0.1', port=27017)
db = client['movie_db']
collection = db['domestic_yearly']

url = 'https://www.boxofficemojo.com/'
addUrl = {'yearly': 'yearly/',
          'seasonal': 'seasonal/',
          'quarterly': 'quarterly/',
          'monthly': 'monthly/',
          'weekly': 'weekly/',
          'weekend': 'weekend/',
          'daily': 'daily/'}

if __name__ == "__main__":
    html = pq(url+addUrl['yearly'])
    html = html.find('tr td table tr')
    rows = html.items()
    rows.next()
    for tr in rows:
        items = (tr.text()).split('\n')
        items[1] = (items[1]).strip('$%')
        items[2] = (items[2]).strip('$%')
        row = {'Year': items[0],
               'TotalGross($)': items[1].strip('$'),
               'TGChange(%)': items[2].strip('%'),
               'TicketsSold': items[3],
               'TSChange(%)': items[4].strip('%'),
               'NumberOfMovies': items[5],
               'TotalScreens': items[6],
               'AvgTicketPrice($)': items[7].strip('$'),
               'AvgCost($)': items[8].strip('$'),
               '#1Movie': items[9]}
        collection.insert(row)
    # results = collection.find()
    #     # for i in results:
    #     #     print(i);