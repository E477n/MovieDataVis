# -*- coding: utf-8 -*-
import pymongo
from bson.son import SON

import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly
import plotly.plotly as py
import plotly.graph_objs as go
from dash.dependencies import Input, Output

from dataProcess import factor3
from algoMerge import algoMerge

plotly.tools.set_credentials_file(username='MerestNora', api_key='hIxgd4Os9A0YzkNYnfn9')

client = pymongo.MongoClient(host='127.0.0.1', port=27017)
db = client['movie_db']
col_cd = db['competitor_detail']
col_wl = db['weekly']

input = ["Avengers: Endgame", "2019-04-01", "2019-09-30", ["3D"], "Avengers", 200]

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

def factor3chart():
    # bubble chart + time series for each genre, interactive
    col_g = db['genres']
    xaxis = []
    yaxis = []
    size = []
    name = []
    for record in col_g.find():
        xaxis.append(record['Genre'])
        yaxis.append(record['Movies#'])
        size.append(record['Gross']/20)
        name.append(record['#1Picture'])
    res = [xaxis, yaxis, size, name]
    return res


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

def create_time_series(dff, axis_type, title):
    return {
        'data': [go.Scatter(
            x=dff['Year'],
            y=dff['Value'],
            mode='lines+markers'
        )],
        'layout': {
            'height': 225,
            'margin': {'l': 20, 'b': 30, 'r': 10, 't': 10},
            'annotations': [{
                'x': 0, 'y': 0.85, 'xanchor': 'left', 'yanchor': 'bottom',
                'xref': 'paper', 'yref': 'paper', 'showarrow': False,
                'align': 'left', 'bgcolor': 'rgba(255, 255, 255, 0.5)',
                'text': title
            }],
            'yaxis': {'type': 'linear' if axis_type == 'Linear' else 'log'},
            'xaxis': {'showgrid': False}
        }
    }

def getFinalSet():
    res = algoMerge.merge(input)
    f_res = []
    for i in range(0, len(res[0][0])):
        row = []
        for j in range(0, len(res[0])):
            row.append(res[0][j][i])
        f_res.append(row)
    print(res[1])
    return [f_res, res[1]]



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

res5 = factor3chart()
data5 = []
trace = go.Scatter(
    x=res5[0],
    y=res5[1],
    text=res5[3],
    mode='markers',
    marker=dict(
        size=res5[2],
    )
)
data5.append(trace)

data0 = []
res0 = getFinalSet()
print(res0)
trace0 = go.Heatmap(
    # z=[[1, 20, 30, 50, 1], [20, 1, 60, 80, 30], [30, 60, 1, -10, 20]],
    # x=['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'],
    # y=['Morning', 'Afternoon', 'Evening']
    z=res0[0],
    y=res0[1],
    x=["Final Grade", "History Box Office Receipts", "Competitors", "Performance of Same Genre Movies", "Franchise", "Budget"],
    colorscale='Viridis',
)
data0.append(trace0)

app.layout = html.Div(children=[
    html.H3(children='Movie Data Visualization'),

    dcc.Tabs(id="tabs-styled-with-props", value='tab-0', children=[
        dcc.Tab(label='Result', value='tab-0'),
        dcc.Tab(label='Factor1 - Historical Box Office Receipts', value='tab-1'),
        dcc.Tab(label='Factor2 - Competitors', value='tab-2'),
        dcc.Tab(label='Factor3 - Same Genre Movies', value='tab-3'),
        dcc.Tab(label='Factor4 - Franchise', value='tab-4'),
        dcc.Tab(label='Factor5 - Budget', value='tab-5'),

    ],
    colors={
        "border": "white",
        "primary": "navy",
        "background": "lightblue"
    },
    style={
        "height": 80
    }),
    html.Div(id='tabs-content-props'),

    html.Div(children='''Movie Data Visualization, Apr 2019'''),
    html.Div(children='''Graduate Design by Chen Chen.'''),
])

@app.callback(Output('tabs-content-props', 'children'),
              [Input('tabs-styled-with-props', 'value')])
def render_content(tab):
    if tab == 'tab-0':
        return html.Div([
            # heat map for the final results
            dcc.Graph(
                style={'height': 700},
                id="finalHeatmap",
                figure=go.Figure(
                    data=data0,
                    layout=go.Layout(
                        title="Heat Map for Final Results",
                        xaxis=dict(
                            title='Factors',
                            ticks='',
                            nticks=10
                        ),
                        yaxis=dict(
                            title='Date',
                            ticks='',
                            nticks=12
                        ),
                        showlegend=True
                    ),
                )
            ),
        ])

    elif tab == 'tab-1':
        return html.Div([
            # Future Movie Release, group by date, count
            dcc.Graph(
                style={'height': 600},
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
        ])
    elif tab == 'tab-2':
        return html.Div([
            dcc.Graph(
                style={'height': 600},
                id='stackedgraph',
                figure=go.Figure(
                    data=data2,
                    layout=go.Layout(
                        barmode='stack',
                        title='Competitor Genre',
                        showlegend=True,
                    )
                ),
            ),
        ])
    elif tab == 'tab-3':
        return html.Div([
            html.Div([
                dcc.Graph(
                    style={'height': 700},
                    id='bubblechart3',
                    figure=go.Figure(
                        data=data5,
                        layout=go.Layout(
                            title='Genre & Time series',
                            xaxis=dict(
                                title='Gross'
                            ),
                            yaxis=dict(
                                title='Movies#'
                            ),
                            showlegend=True,
                            legend=go.layout.Legend(
                                x=0,
                                y=1.0
                            ),
                            margin=go.layout.Margin(t=100, b=180)
                        )
                    ),
                ),
            ],
            style={'width': '100%', 'display': 'inline-block'}),
            html.Div([
                dcc.Graph(
                    id='x-time-series',
                    # figure=go.Figure(
                    #     data=data3,
                    #     layout=go.Layout(
                    #         title='Gross Time Series for Single Genre',
                    #         showlegend=True,
                    #         legend=go.layout.Legend(
                    #             x=0,
                    #             y=1.0
                    #         ),
                    #         # margin=go.layout.Margin(l=40, r=0, t=40, b=30)
                    #     )
                    # ),
                )
            ], style={'display': 'inline-block', 'width': '70%', 'height': 700}),
        ])
    elif tab == 'tab-4':
        return html.Div([

        ])
    elif tab == 'tab-5':
        return html.Div([
            # factor5 history box office in weeks
            dcc.Graph(
                style={'height': 600},
                id='linechart',
                figure=go.Figure(
                    data=data3,
                    layout=go.Layout(
                        title='Weekly Gross for Factor 5',
                        xaxis=dict(
                            title='week#'
                        ),
                        yaxis=dict(
                            title='Weekly Total Gross'
                        ),
                        showlegend=True,
                        legend=go.layout.Legend(
                            x=0,
                            y=1.0
                        ),
                        # margin=go.layout.Margin(l=40, r=0, t=40, b=30)
                    )
                ),
            ),
            dcc.Graph(
                style={'height': 600},
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
                        hovermode='closest'
                        # margin=go.layout.Margin(l=100, r=100, t=40, b=30)
                    )
                ),
            ),
        ])


if __name__ == '__main__':
    get_cc()
    app.run_server(debug=True)
