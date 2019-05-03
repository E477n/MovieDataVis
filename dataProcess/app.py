# -*- coding: utf-8 -*-
import pymongo
from bson.son import SON
from datetime import datetime as dt

import dash
import dash_table
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

input = ["Avengers: Endgame", "2019-01-01", "2019-12-30", ["3D"], "Avengers", 200]

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

# A -> A^T
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
def getFinalTable(res0):
    i = 0
    modified_list = []
    for item in res0[0]:
        item.append(res0[1][i])
        i += 1
        modified_list.append(item)

    sorted_list = sorted(modified_list, key=lambda x: x[0], reverse=True)

    # list of dict
    f_res_table = []
    i = 0
    for record in sorted_list:
        i += 1
        row = {}
        row = {
            "Rank": i,
            "Date": record[6],
            "Final Grade": record[0],
            "History Box Office Receipts": record[1],
            "Competitors": record[2],
            "Performance of Same Genre Movies": record[3],
            "Franchise": record[4],
            "Budget": record[5]
        }
        f_res_table.append(row)
    return f_res_table



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
if input[4] == "":
    trace0 = go.Heatmap(
        z=res0[0],
        y=res0[1],
        x=["Final Grade", "History Box Office Receipts", "Competitors", "Performance of Same Genre Movies", "Budget"],
        colorscale='Viridis',
    )
elif input[4] == "" and input[5] < 200:
    trace0 = go.Heatmap(
        z=res0[0],
        y=res0[1],
        x=["Final Grade", "History Box Office Receipts", "Competitors", "Performance of Same Genre Movies"],
        colorscale='Viridis',
    )
elif input[4] != "" and input[5] < 200:
    trace0 = go.Heatmap(
        z=res0[0],
        y=res0[1],
        x=["Final Grade", "History Box Office Receipts", "Competitors", "Performance of Same Genre Movies", "Franchise"],
        colorscale='Viridis',
    )
else:
    trace0 = go.Heatmap(
        z=res0[0],
        y=res0[1],
        x=["Final Grade", "History Box Office Receipts", "Competitors", "Performance of Same Genre Movies", "Franchise", "Budget"],
        colorscale='Viridis',
)
data0.append(trace0)
table_data0 = getFinalTable(res0)

app.layout = html.Div(children=[
    html.Div(
        style={
            'width': '30%',
            'height': '500px',
            'display': 'inline-block',
        }
    ),

    html.Div([

        html.H5(children='Movie Release Date Decision',
                style={
                    'marginTop': '60px',
                }
                ),

        html.Div(children=[
            html.Label(children='Movie Name:'),
            dcc.Input(
                placeholder='Enter a movie name',
                type='text',
                value=''
            ),
        ],
            style={
                'marginTop': '30px',
            }
        ),
        html.Div([
            html.Label(children='Release Date Range:'),
            dcc.DatePickerRange(
                id='date-picker-range',
                start_date=dt(2019, 5, 4),
                end_date_placeholder_text='Select a date',
                style={
                    'width': '400px',
                }
            ),
        ],
            style={
                'marginTop': '30px',
            }
        ),
        html.Div([
            html.Label(children='Genres:'),
            dcc.Dropdown(
                options=[
                    {'label': '3D', 'value': '3D'},
                    {'label': 'Animation', 'value': 'Animation'},
                    {'label': 'Action', 'value': 'Action'}
                ],
                multi=True,
                value="Animation"
            ),
        ],
            style={
                'marginTop': '30px',
            }
        ),
        html.Div([
            html.Label(children='Franchise:'),
            dcc.Dropdown(
                options=[
                    {'label': 'Avengers', 'value': 'Avengers'},
                    {'label': 'Moana', 'value': 'Moana'},
                    {'label': 'Toy', 'value': 'Toy'}
                ],
                value='Avengers'
            ),
        ],
            style={
                'marginTop': '30px',
            }
        ),
        html.Div([
            html.Label(children='Production Budget (million):'),
            dcc.Slider(
                min=0,
                max=400,
                step=5,
                marks={
                   i: '{}'.format(i) for i in range(0, 400, 50)
                },
                value=200,
            )
        ],
            style={
                'marginTop': '30px',
            }
        ),
        html.Div([
            html.Button('Make Decisions', id='button',
                        style={
                            'color': 'white',
                            'backgroundColor': 'rgb(61, 153, 112)',
                        }
                        ),
        ],
            style={
                'marginTop': '60px',
                'textAlign': 'center'
            }
        ),

    ],
    style={
        'width': '40%',
        'height': '500px',
        'display': 'inline-block',
    }
    ),

    html.Div(
    style={
        'width': '29%',
        'height': '500px',
        'display': 'inline-block',
    }
    ),


    dcc.Tabs(id="tabs-styled-with-props", value='tab-0', children=[
        dcc.Tab(label='Result', value='tab-0'),
        dcc.Tab(label='Historical Box Office', value='tab-1'),
        dcc.Tab(label='Competitors', value='tab-2'),
        dcc.Tab(label='Same Genre Movies', value='tab-3'),
        dcc.Tab(label='Franchise', value='tab-4'),
        dcc.Tab(label='Budget', value='tab-5'),

    ],
    colors={
        "border": "white",
        "primary": "navy",
        "background": "#3c996526"
    },
    style={
        "height": '60px',
        'marginTop': '100px',
    }),
    html.Div(id='tabs-content-props'),

    html.Div(children='''Movie Data Visualization, Apr 2019'''),
    html.Div(children='''Graduate Design by Chen Chen.'''),
],
    style={
        "margin": '20px'
    }
)

@app.callback(Output('tabs-content-props', 'children'),
              [Input('tabs-styled-with-props', 'value')])
def render_content(tab):
    if tab == 'tab-0':
        return html.Div([
            html.Div([
                # heat map for the final results
                dcc.Graph(
                    style={
                        'height': 800,
                    },
                    id="finalHeatmap",
                    figure=go.Figure(
                        data=data0,
                        layout=go.Layout(
                            title="Grading Heat Map for Final Results",
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
            ],
                style={
                    'width': '60%',
                    'display': 'inline-block'
                   },
            ),
            html.Div([
                dash_table.DataTable(
                    id='finaltable',
                    columns=[{"name": i, "id": i} for i in
                             ["Rank", "Date", "Final Grade", "History Box Office Receipts", "Competitors",
                              "Performance of Same Genre Movies", "Franchise", "Budget"]],
                    data=table_data0,
                    n_fixed_rows=1,
                    style_cell={
                        'minWidth': '10px',
                        'maxWidth': '70px',
                        'whiteSpace': 'normal'
                    },
                    style_table={
                        'maxHeight': '600px',
                        'overflowY': 'scroll',
                        'maxWidth': '300',
                    },
                    style_data_conditional=[{
                        'if': {'column_id': 'Final Grade'},
                        'backgroundColor': '#3D9970',
                        'color': 'white',
                    }]
                )

            ],
                style={
                    'float': 'right',
                    'width': '35%',
                    'marginRight': '30px',
                    'marginTop': '100px',
                }
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
    app.run_server(debug=True)
