# -*- coding: utf-8 -*-
import pymongo
from bson.son import SON

import dash
import dash_core_components as dcc
import dash_html_components as html

client = pymongo.MongoClient(host='127.0.0.1', port=27017)
db = client['movie_db']
col_cd = db['competitor_detail']

def groupbyDate():
    # groupby release date and count
    # sort by release date
    xaxis = []
    yaxis = []
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
        xaxis.append(record["_id"])
        yaxis.append(record["count"])
    resData = [xaxis, yaxis]
    return resData


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

res = groupbyDate()
app.layout = html.Div(children=[
    html.H1(children='Movie Data Visualization'),

    dcc.Graph(
        id='example-graph',
        figure={
            'data': [
                {'x': res[0], 'y': res[1], 'type': 'bar', 'name': 'SF'},
            ],
            'layout': {
                'title': 'Future Movie Release',
                'xaxis': {'title': 'Date'},
                'yaxis': {'title': 'Number of Movie Release'}
            }
        }
    ),
    html.Div(children='''
    Movie Data Visualization, Apr 2019
'''),
    html.Div(children='''
    Graduate Design by Chen Chen.
''')


])



if __name__ == '__main__':
    app.run_server(debug=True)