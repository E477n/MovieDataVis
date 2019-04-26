# -*- coding: utf-8 -*-
import pymongo
from bson.son import SON

import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly
import plotly.plotly as py
import plotly.graph_objs as go

plotly.tools.set_credentials_file(username='MerestNora', api_key='hIxgd4Os9A0YzkNYnfn9')

client = pymongo.MongoClient(host='127.0.0.1', port=27017)
db = client['movie_db']
col_cd = db['competitor_detail']
col_wl = db['weekly']

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

def get_cc():
    col_cc = db['competitor_count']
    # generate non repetitive genre set
    genre_set = []
    for record in col_cc.find():
        if record['Genre'] not in genre_set:
            genre_set.append(record['Genre'])

    res = []
    for genre in genre_set:
        x = []
        y = []
        for record in col_cc.find({'Genre': genre}):
            x.append(record['ReleaseDate'])
            y.append(record['Count'])
        row = [genre, x, y]
        res.append(row)
    return res

def weeklyGrossTrendByYear():
    years = ["2012", "2013", "2014", "2015", "2016", "2017", "2018"]
    res = []
    xaxis = []
    for i in range(1, 54):
        xaxis.append(i)
    for year in years:
        row = []
        for record in col_wl.find({"Year": year}):
            row.append(record["OverallGross($)"])
        res.append(row)
    return [xaxis, res]

def blockbusterBudget():
    col_bg = db['budget']
    xaxis = []
    yaxis = []
    size = []
    title = []
    for record in col_bg.find():
        xaxis.append(record["week#"])
        yaxis.append(record["budget"])
        size.append(record["budget"]/7)
        title.append(record["title"])
    return [xaxis, yaxis, size, title]



external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

res = groupbyDate()

res2 = get_cc()
data2 = []
for i in res2:
    trace = go.Bar(
        x=i[1],
        y=i[2],
        name=i[0]
    )
    data2.append(trace)

res3 = weeklyGrossTrendByYear()
data3 = []
d3year = 2012
for i in res3[1]:
    trace = go.Scatter(
        x=res3[0],
        y=i,
        name=d3year
    )
    d3year += 1
    data3.append(trace)

res4 = blockbusterBudget()
data4 = []
trace = go.Scatter(
    x=res4[0],
    y=res4[1],
    text=res4[3],
    mode='markers',
    marker=dict(
        size=res4[2],
    )
)
data4.append(trace)

app.layout = html.Div(children=[
    html.H1(children='Movie Data Visualization'),

    # Future Movie Release, group by date, count
    dcc.Graph(
        style={'height': 700},
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
'''),

    dcc.Graph(
        style={'height': 700},
        id='stackedgraph',
        figure=go.Figure(
            data=data2,
            layout=go.Layout(
                barmode='stack',
                title='Competitor Genre',
                showlegend=True,
                legend=go.layout.Legend(
                    x=0,
                    y=1.0
                ),
                margin=go.layout.Margin(l=40, r=0, t=40, b=30)
            )
        ),
    ),

    html.Div(children='''
    Movie Data Visualization, Apr 2019
'''),
    html.Div(children='''
    Graduate Design by Chen Chen.
'''),

    # factor5 history box office in weeks
    dcc.Graph(
        style={'height': 700},
        id='linechart',
        figure=go.Figure(
            data=data3,
            layout=go.Layout(
                title='Weekly Gross for Factor 5',
                showlegend=True,
                legend=go.layout.Legend(
                    x=0,
                    y=1.0
                ),
                margin=go.layout.Margin(l=40, r=0, t=40, b=30)
            )
        ),
    ),

    html.Div(children='''
    Movie Data Visualization, Apr 2019
'''),
    html.Div(children='''
    Graduate Design by Chen Chen.
'''),

    dcc.Graph(
        style={'height': 700},
        id='bubblechart',
        figure=go.Figure(
            data=data4,
            layout=go.Layout(
                title='movie budget and release date for factor 5',
                xaxis=dict(
                    title='week#'
                ),
                yaxis=dict(
                    title='Budget'
                ),
                showlegend=True,
                legend=go.layout.Legend(
                    x=0,
                    y=1.0
                ),
                margin=go.layout.Margin(l=100, r=100, t=40, b=30)
            )
        ),
    ),

    html.Div(children='''
    Movie Data Visualization, Apr 2019
'''),
    html.Div(children='''
    Graduate Design by Chen Chen.
''')




])

if __name__ == '__main__':
    get_cc()
    app.run_server(debug=True)
