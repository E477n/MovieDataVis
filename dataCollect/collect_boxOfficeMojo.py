# -*- coding: utf-8 -*-
from pyquery import PyQuery as pq
from bson import json_util as jsonb
import pymongo

client = pymongo.MongoClient(host='127.0.0.1', port=27017)
db = client['movie_db']

url = 'https://www.boxofficemojo.com/'

def update_domestic_yearly():
    collection = db['domestic_yearly']
    html = pq(url + 'yearly/')
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

def update_seasonal():
    seasons = ['Spring', 'Summer', 'Fall', 'Winter', 'Holiday']
    collection = db['seasonal']

    for season in seasons:
        html = pq(url + 'seasonal/?chart=byseason&season=' + season + '&view=releasedate')
        html = html.find('center table:first tr')
        rows = html.items()
        rows.next()
        for tr in rows:
            items = (tr.text()).split('\n')
            items[1] = (items[1]).strip('$%')
            items[2] = (items[2]).strip('$%')
            row = {'Season': season,
                   'Year': items[0],
                   'TotalGross($)': items[1].strip('$'),
                   'TGChange(%)': items[2].strip('%'),
                   'DaysInSeason': items[3],
                   'DSAvg($)': items[4].strip('$'),
                   'NumberOfMovies': items[5],
                   'MovieAvg($)': items[6].strip('$'),
                   'AvgDrop(%)': items[7].strip('%'),
                   '#1Movie': items[8],
                   '#1MovieGross($)': items[9].strip('$'),
                   '%OfTotal(%)': items[10].strip('%')}
            collection.insert(row)

def update_quarterly():
    quarters = ['Q1', 'Q2', 'Q3', 'Q4']
    collection = db['quarterly']

    for quarter in quarters:
        html = pq(url + 'quarterly/?chart=byquarter&quarter=' + quarter + '&view=releasedate')
        html = html.find('center table:first tr')
        rows = html.items()
        rows.next()
        for tr in rows:
            items = (tr.text()).split('\n')
            items[1] = (items[1]).strip('$%')
            items[2] = (items[2]).strip('$%')
            row = {'Quarter': quarter,
                   'Year': items[0],
                   'TotalGross($)': items[1].strip('$'),
                   'TGChange(%)': items[2].strip('%'),
                   'NumberOfMovies': items[3],
                   'MovieAvg($)': items[4].strip('$'),
                   'AvgDrop(%)': items[5].strip('%'),
                   '#1Movie': items[6],
                   '#1MovieGross($)': items[7].strip('$'),
                   '%OfTotal(%)': items[8].strip('%')}
            collection.insert(row)

def update_monthly():
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    collection = db['monthly']

    for month in range(1, 13):
        html = pq(url + 'monthly/?view=releasedate&chart=bymonth&month=' + str(month) + '&view=releasedate')
        html = html.find('center table:first tr')
        rows = html.items()
        rows.next()
        for tr in rows:
            items = (tr.text()).split('\n')
            items[1] = (items[1]).strip('$%')
            items[2] = (items[2]).strip('$%')
            row = {'month': months[month-1],
                   'Year': items[0],
                   'TotalGross($)': items[1].strip('$'),
                   'TGChange(%)': items[2].strip('%'),
                   'NumberOfMovies': items[3],
                   'MovieAvg($)': items[4].strip('$'),
                   'AvgDrop(%)': items[5].strip('%'),
                   '#1Movie': items[6],
                   '#1MovieGross($)': items[7].strip('$'),
                   '%OfTotal(%)': items[8].strip('%')}
            # print(row)
            collection.insert(row)

def update_weekly():
    collection = db['weekly']

    for week in range(1, 54):
        html = pq(url + 'weekly/?view=wk&wk=' + str(week) + '&p=.htm')
        html = html.find('center table:first tr')
        rows = html.items()
        rows.next()
        for tr in rows:
            items = (tr.text().encode('raw_unicode_escape')).split('\n')
            date = items[1].split('\x96')
            row = {'Week#': week,
                   'Year': items[0],
                   'Week': date[0] + '-' + date[1],
                   'Top12Gross($)': items[2].strip('$'),
                   'TG12Change(%)': items[3].strip('%'),
                   'OverallGross($)': items[4].strip('$'),
                   'OGChange(%)': items[5].strip('%'),
                   'TotalMovies': items[6],
                   '#1Movie': items[7]}
            # print(row)
            collection.insert(row)

def update_weekend():
    collection = db['weekend']

    for week in range(1, 54):
        html = pq(url + 'weekend/?view=wknd&wknd=' + str(week) + '&sort=year&order=DESC&p=.htm')
        html = html.find('center table:first tr')
        rows = html.items()
        rows.next()
        rows.next()
        for tr in rows:
            items = (tr.text().encode('raw_unicode_escape')).split('\n')
            date = items[1].split('\x96')
            row = {'Week#': week,
                   'Year': items[0],
                   'Week': date[0] + '-' + date[1],
                   'Top12Gross($)': items[2].strip('$'),
                   'TG12Change(%)': items[3].strip('%'),
                   'OverallGross($)': items[4].strip('$'),
                   'OGChange(%)': items[5].strip('%'),
                   'TotalMovies': items[6],
                   '#1Movie': items[7]}
            # print(row)
            collection.insert(row)

def update_daily():
    collection = db['daily']

    for year in range(2002, 2020):
        html = pq(url + 'daily/?view=year&yr=' + str(year) + '&p=.htm')
        html = html.find('center table:first tr')
        rows = html.items()
        rows.next()
        for tr in rows:
            items = (tr.text().encode('raw_unicode_escape')).split('\n')
            row = {'Year': year,
                   'Row': items[0],
                   'Date': items[1],
                   'Day': items[2],
                   'Day#': items[3],
                   'Top10Gross($)': items[4].strip('$'),
                   'TG10ChangeYD(%)': items[5].strip('%'),
                   'TG10ChangeLW(%)': items[6].strip('%'),
                   'MoviesTracked': items[7],
                   '#1Movie': items[8],
                   'Gross($)': items[9].strip('$')}
            # print(row)
            collection.insert(row)

def update_studio():
    collection = db['studio']
    for year in range(2000, 2020):
        html = pq(url + 'studio/?view=company&view2=yearly&yr=' + str(year) + '&p=.htm')
        html = html.find('table table:first tr')
        rows = html.items()
        rows.next()
        for tr in rows:
            items = (tr.text().encode('raw_unicode_escape')).split('\n')
            if len(items) < 6:
                items.append(items[4])
                items[4] = items[3]
                items[3] = items[2]
                items[2] = items[1]
                items[1] = '-'
            if items[3].find('k') != -1:
                items[3] = items[3].strip('$ | k').replace(",", "")
                items[3] = '%.4f' % (float(items[3])/1000)
            else:
                items[3] = float(items[3].strip('$').replace(",", ""))
            row = {'Year': year,
                   'Rank': int(items[0]),
                   'Distributor': items[1],
                   'MarketShare(%)': float(items[2].strip('%')),
                   'TotalGross($)': items[3],
                   'MoviesTracked': int(items[4]),
                   'YearMovies': int(items[5])}
            # print(row)
            collection.insert(row)

def update_actor():
    collection = db['actor']
    for i in range(1, 4):
        html = pq(url + 'people/?view=Actor&pagenum=' + str(i) + '&sort=person&order=ASC&p=.htm')
        html = html.find('table table:first tr')
        rows = html.items()
        rows.next()
        for tr in rows:
            items = (tr.text().encode('raw_unicode_escape')).split('\n')
            res = []
            for item in [items[1], items[3], items[5]]:
                if item.find('k') != -1:
                    item = item.strip('$ | k').replace(",", "")
                    item = '%.4f' % (float(item) / 1000)
                else:
                    item = float(item.strip('$').replace(",", ""))
                res.append(item)
            row = {'Person': items[0].decode("unicode_escape"),
                   'TotalGross($)': res[0],
                   'Movies#': items[2],
                   'MovieAverage($)': res[1],
                   '#1Picture': items[4],
                   'Gross': res[2]}
            # print(row)
            collection.insert(row)

def update_director():
    collection = db['director']
    for i in range(1, 3):
        html = pq(url + 'people/?view=Director&pagenum=' + str(i) + '&sort=person&order=ASC&p=.htm')
        html = html.find('table table:first tr')
        rows = html.items()
        rows.next()
        for tr in rows:
            items = (tr.text().encode('raw_unicode_escape')).split('\n')
            res = []
            for item in [items[1], items[3], items[5]]:
                if item.find('k') != -1:
                    item = item.strip('$ | k').replace(",", "")
                    item = float('%.4f' % (float(item) / 1000))
                else:
                    item = float(item.strip('$').replace(",", ""))
                res.append(item)
            row = {'Person': items[0].decode("unicode_escape"),
                   'TotalGross($)': res[0],
                   'Movies#': int(items[2]),
                   'MovieAverage($)': res[1],
                   '#1Picture': items[4].decode("unicode_escape"),
                   'Gross': res[2]}
            # print(row)
            collection.insert(row)

def update_genres():
    collection = db['genres']
    html = pq(url + 'genres/')
    html = html.find('table table:first tr')
    rows = html.items()
    rows.next()
    for tr in rows:
        items = (tr.text().encode('raw_unicode_escape')).split('\n')
        if items[3].find('k') != -1:
            items[3] = items[3].strip('$ | k').replace(",", "")
            items[3] = float('%.4f' % (float(items[3]) / 1000))
        else:
            items[3] = float(items[3].strip('$').replace(",", ""))
        row = {'Genre': items[0],
               'Movies#': int(items[1]),
               '#1Picture': items[2],
               'Gross': items[3]}
        # print(row)
        collection.insert(row)

def update_genre_details():
    collection = db['genre_details']
    html = pq(url + 'genres/')
    html = html.find('table table:first tr')
    rows = html.items()
    rows.next()
    for a in rows:
        addurl = a.find('td:first a').attr('href').replace("./", "")
        print(addurl)
        count = int(a.find('td:nth-child(2)').text())
        print(count)
        genre = (a.find('td:first-child a').text().encode('raw_unicode_escape'))
        try:
            html2 = pq(url + 'genres/' + addurl)
        except:
            html2 = ""
            continue

        if(html2 != ""):
            html2 = html2.find('table table:first tr')
            rows2 = html2.items()
            rows2.next()
            i = 1
            for tr in rows2:
                items = (tr.text().encode('raw_unicode_escape')).split('\n')
                if(len(items) > 8):
                    del items[2]
                res = []
                for item in [items[3], items[4], items[5], items[6]]:
                    if (item == "n/a") | (item == "-"):
                        item = 0
                    else:
                        if item.find('k') != -1:
                            item = item.strip('$ | k').replace(",", "")
                            item = float('%.4f' % (float(items) / 1000))
                        else:
                            item = float(item.strip('$').replace(",", ""))
                    res.append(item)
                row = {'Genre': genre,
                       'Rank': int(items[0]),
                       'Title': items[1],
                       'Studio': items[2],
                       'LifetimeGross($)': res[0],
                       'Theaters': res[1],
                       'OpeningGross($)': res[2],
                       'OpeningTheaters': res[3],
                       'Date': items[7]}
                i += 1
                if i > min(100, count):
                    break
                print(row)
                collection.insert(row)

def update_franchises():
    collection = db['franchise']
    html = pq(url + 'franchises/?view=Franchise&p=.htm')
    html = html.find('table table:first tr')
    rows = html.items()
    rows.next()
    for tr in rows:
        items = (tr.text().encode('raw_unicode_escape')).split('\n')
        res = []
        for item in [items[1], items[3], items[5]]:
            if item.find('k') != -1:
                item = item.strip('$ | k').replace(",", "")
                item = float('%.4f' % (float(item) / 1000))
            else:
                item = float(item.strip('$').replace(",", ""))
            res.append(item)
        row = {'Franchise': items[0],
               'TotalGross($)': res[0],
               'Movies#': int(items[2]),
               'MoviesAvg($)': res[1],
               '#1Picture': items[4],
               'Gross($)': res[2]}
        collection.insert(row)

def update_competitors():
    collection = db['competitor']
    years = [2019, 2020, 2021]
    for y in years:
        html = pq(url + 'schedule/?view=bydate&release=theatrical&yr=' + str(y) + '&p=.htm')
        # print(html)
        html = html.find('table table table table font:nth-child(2) a:even')
        rows = html.items()
        for tr in rows:
            movieurl = tr.attr('href')
            moviename = tr.find('b').text()
            row = {'url': movieurl,
                   'Movie': moviename}
            print(row)
            collection.insert(row)

def update_competitor_datails():
    collection = db['competitor_detail']
    urlcol = db['competitor']
    for row in urlcol.find():
        html = pq(url + row['url'])
        html = html.find('table table table center table tr')
        trs = html.items()
        if len(html) > 3:
            trs.next()
        count = 1
        res = [row['Movie']]
        for b in trs:
            b = b.find('b')
            for txt in b.items():
                res.append(txt.text())
            count += 1
            if count > 3:
                break
        try:
            finalres = {'Movie': res[0],
                        'Distributor': res[1],
                        'ReleaseDate': res[2],
                        'Genre': res[3],
                        'Runtime': res[4],
                        'MPAARating': res[5],
                        'ProductionBudget': res[6]}
            print(finalres)
            collection.insert(finalres)
        except:
            continue

def collectBudget():
    col_bg = db['budget']
    html = pq('https://en.wikipedia.org/wiki/List_of_most_expensive_films')
    html = html.find('table .wikitable .sortable .plainrowheaders')
    print(html)


if __name__ == "__main__":
    # update_domestic_yearly()
    # update_seasonal()
    # update_quarterly()
    # update_monthly()
    # update_weekly()
    # update_weekend()
    # update_daily()
    # update_studio()
    # update_actor()
    # update_director()
    # update_genres()
    # update_genre_details()
    # update_franchises()
    # update_competitors()
    # update_competitor_datails()
    collectBudget()
