# -*- coding: utf-8 -*-
"""
Created on Tue May  1 19:14:04 2018

@author: P20133
"""

import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go
import json
from operator import itemgetter
from datetime import datetime as dt
from scipy.stats.stats import pearsonr

personen_de = json.load(open("personenliste_de_clean.json"))
personen = json.load(open("personenliste_en_clean.json"))
datumkompakt = json.load(open("datumliste_en_clean.json"))
datumkompakt_de = json.load(open("datumliste_de_clean.json"))

dict1 = personen
personenliste = sorted(dict1.items(), key=itemgetter(1),reverse=True)
names = list(zip(*personenliste))[0]


app = dash.Dash(__name__, static_folder='static')
server = app.server
app.title='Who is in the News!'
app.css.append_css({"external_url": "https://stackpath.bootstrapcdn.com/bootstrap/4.1.1/css/bootstrap.min.css"})

app.layout = html.Div([
    html.H1(children='Who is in the News!'),
    #, style={'text-align': 'center'}
    #html.Div([
            #html.Img(src='./static/newspic.jpg')
            #]),


    html.Div([
            dcc.Markdown('''This site gives you some **statistics and plots** of the appearence of persons in written news articles. You can use them for research
                         or journalistic purposes about how often public persons are mentioned in news articles and how these persons are related to each other.
                         ''' ),
    ],
      ),


html.Div([

    html.Div([
            dcc.Markdown('''
### The Data

The text-data comes from articles published by *Reuters* agency on their website [www.reuters.com](https://www.reuters.com/).
At the moment about 70.000 - 80.000 news articles in English and German are indexed. German news are from 2015 until now, English from 2016
until now.'''),
    ], className='col-lg-4'),

    html.Div([

        dcc.Markdown('''
### The Analysis

For each article a Named Entity Extraction (NER) is conducted with a **machine learning algorithm** to detect the mentions of the persons
in the texts. This algorithm uses a model which was **pretrained on a corpus** of Google news articles for English and German. The lists of
persons in the articles are used to calculate the counts and are stored in a database.'''
        ),
    ], className='col-lg-4'),

   html.Div([
          dcc.Markdown('''
### The Plots

We show a **barchart** of the counts for the most often mentioned persons. For up to four of this persons you can plot the
**timeseries** of the counts at the same time for a time period you select. For two persons you can calculate their **relation / correlation**
as a funcion of time.'''
        ),
        ], className='col-lg-4'),

],
className='row'),

    html.Div([
            html.Div([
                    html.H2(children='''Top Persons'''),
                    html.Div([
                        html.P(children='''Choose the number of persons:'''),
                        dcc.Dropdown(
                            id='histnum',
                            options=[{'label': i, 'value': i} for i in [10,15,20,25,30,35,40]],
                            value=20
                        )
                    ], className='form-control'),

                    html.Div([
                        html.P(children='''Choose the language:'''),
                        dcc.RadioItems(
                            id='sprache',
                            options=[{'label': i, 'value': i} for i in ['English', 'German']],
                            value='English'
                            )
                    ],className='form-control')
                ],
            className='col-lg-4 form-group' ),

            html.Div([
                    dcc.Graph(id='barchart')
                ],
            className='col-lg-8')
        ],
    className='row'),



    html.H2(children='''Variation over time'''),

    html.Div([


    html.Div([
            html.P(children='''Choose the timespan: '''),
            dcc.DatePickerRange(
                    id='datumrange',
                    min_date_allowed=dt(2015, 1, 1),
                    max_date_allowed=dt(2018, 7, 23),
                    initial_visible_month=dt(2018, 6, 1),
                    start_date=dt(2018, 4, 1),
                    end_date=dt(2018, 6, 30)
                    ),
            ],
    className='col-lg-4  form-group form-control'),


    html.Div([
            html.P(children='''Choose the persons: '''),
            html.Div([
                    #html.P(children='''Person 1'''),
                    dcc.Dropdown(
                            id='name1',
                            options=[{'label': i, 'value': i} for i in []],
                            value=names[0]
                            )
                    ],
            style={'width': '24%', 'float': 'left'}),
            html.Div([

                    dcc.Dropdown(
                            id='name2',
                            options=[{'label': i, 'value': i} for i in []],
                            value=names[1]
                            )
                    ],
            style={'width': '24%', 'float': 'left'}),
            html.Div([

                    dcc.Dropdown(
                            id='name3',
                            options=[{'label': i, 'value': i} for i in []],
                            value=names[2]
                            )
                    ],
            style={'width': '24%', 'float': 'left'}),
            html.Div([

                    dcc.Dropdown(
                            id='name4',
                            options=[{'label': i, 'value': i} for i in []],
                            value=names[3]
                            )
                ],
            style={'width': '24%', 'float': 'left'}),
        ],
        className='col-lg-8 form-group form-control')


    ],
    className='row'),



    html.Div([
            dcc.Graph(id='zeitplot')
        ],
    ),




    html.H2(children='Relation of Persons'),
    html.Div([
            dcc.Dropdown(
                    id='name5',
                    options=[{'label': i, 'value': i} for i in []],
                    value=names[0]
                    )
            ],
    style={'width': '20%', 'float': 'center', 'display': 'inline-block'}),
    html.Div([
            dcc.Dropdown(
                    id='name6',
                    options=[{'label': i, 'value': i} for i in []],
                    value=names[1]
                    )
            ],
    style={'width': '20%', 'float': 'center', 'display': 'inline-block'}),

    html.Div([
            dcc.Markdown('''Related Persons measures how **correlated** two persons are, in the sense that they are mentioned
in the news at the same day. On one hand if they have the same counts every day the correlation is 1, on the
other hand if a person appears always on days the second one does not, they are negative correlated near -1.
If there is no correlation the value is near zero.

This measure varies over time as the correlation changes in the same way the relationship of the persons may change.
We calculate the correlations over **a sliding time window of 30 days** and plot this values as a function of time.''', ),
                         ],
       ),
    dcc.Graph(id='relationplot'),








    dcc.Markdown('''**Imprint:**  [Dr. Andreas Stöckl](http://www.stoeckl.ai/impressum/)''')
],  className='container')
#style ={'padding' : '40px', 'width' : '1200px', 'backgroundColor':'#f4f7fc'},

@app.callback(
    dash.dependencies.Output('zeitplot', 'figure'),
    [dash.dependencies.Input('datumrange', 'start_date'),
     dash.dependencies.Input('datumrange', 'end_date'),
     dash.dependencies.Input('sprache', 'value'),
     dash.dependencies.Input('name1', 'value'),
     dash.dependencies.Input('name2', 'value'),
     dash.dependencies.Input('name3', 'value'),
     dash.dependencies.Input('name4', 'value')
     ])
def update_figure_a(startdatum,enddatum,sprache,name1,name2,name3,name4):

    if sprache == 'English':
        dict1 = datumkompakt[name1]
        dict2 = datumkompakt[name2]
        dict3 = datumkompakt[name3]
        dict4 = datumkompakt[name4]
    else:
        dict1 = datumkompakt_de[name1]
        dict2 = datumkompakt_de[name2]
        dict3 = datumkompakt_de[name3]
        dict4 = datumkompakt_de[name4]

    datelist = pd.date_range(start=startdatum, end=enddatum).tolist()
    datelist = pd.to_datetime((datelist))

    y_name1 =[]
    y_name2 =[]
    y_name3 =[]
    y_name4 =[]
    for date in datelist:
        if str(date).split()[0] in dict1:
            y_name1.append(dict1[str(date).split()[0]])
        else:
            y_name1.append(0)
        if str(date).split()[0] in dict2:
            y_name2.append(dict2[str(date).split()[0]])
        else:
            y_name2.append(0)
        if str(date).split()[0] in dict3:
            y_name3.append(dict3[str(date).split()[0]])
        else:
            y_name3.append(0)
        if str(date).split()[0] in dict4:
            y_name4.append(dict4[str(date).split()[0]])
        else:
            y_name4.append(0)

    trace1 = go.Scatter(
    x = datelist,
    y = y_name1,
    mode = 'lines',
    name = name1
    )
    trace2 = go.Scatter(
    x = datelist,
    y = y_name2,
    mode = 'lines',
    name = name2
    )
    trace3 = go.Scatter(
    x = datelist,
    y = y_name3,
    mode = 'lines',
    name = name3
    )
    trace4 = go.Scatter(
    x = datelist,
    y = y_name4,
    mode = 'lines',
    name = name4
    )


    return {
        'data': [trace1,trace2,trace3,trace4],
        'layout': go.Layout(
            xaxis={'title': 'Date'},
            yaxis={'title': 'Counts'},
            legend={'x': 0, 'y': 1},
            height=700,
            title='Counts over time'
        )
    }

@app.callback(
    dash.dependencies.Output('barchart', 'figure'),
    [     dash.dependencies.Input('sprache', 'value'),
     dash.dependencies.Input('histnum', 'value')
     ])

def update_figure_b(sprache,histnum):
    if sprache == 'English':
        dict1 = personen
    else:
        dict1 = personen_de

    personenliste = sorted(dict1.items(), key=itemgetter(1),reverse=True)

    names = list(zip(*personenliste))[0][0:histnum]
    values = list(zip(*personenliste))[1][0:histnum]

    trace1 = go.Bar(
    y = names,
    x = values,
    orientation = 'h'
    )


    return {
        'data': [trace1],
        'layout': go.Layout(
            xaxis={'title': 'Counts'},
            yaxis={'autorange':'reversed'},
            height=25*histnum,
            title='Counts per person',
            margin=go.Margin(
                    l=150,
                    r=50,
                    b=50,
                    t=50,
                    pad=4
            ),

        )
    }


@app.callback(
    dash.dependencies.Output('name1', 'options'),
    [dash.dependencies.Input('sprache', 'value'),
     dash.dependencies.Input('histnum', 'value')])
def set_names_options_a(sprache,histnum):
    if sprache == 'English':
        dict1 = personen
    else:
        dict1 = personen_de

    personenliste = sorted(dict1.items(), key=itemgetter(1),reverse=True)

    names = list(zip(*personenliste))[0][0:histnum]
    return [{'label': i, 'value': i} for i in names]

@app.callback(
    dash.dependencies.Output('name2', 'options'),
    [dash.dependencies.Input('sprache', 'value'),
     dash.dependencies.Input('histnum', 'value')])
def set_names_options_b(sprache,histnum):
    if sprache == 'English':
        dict1 = personen
    else:
        dict1 = personen_de

    personenliste = sorted(dict1.items(), key=itemgetter(1),reverse=True)

    names = list(zip(*personenliste))[0][0:histnum]
    return [{'label': i, 'value': i} for i in names]

@app.callback(
    dash.dependencies.Output('name3', 'options'),
    [dash.dependencies.Input('sprache', 'value'),
     dash.dependencies.Input('histnum', 'value')])
def set_names_options_c(sprache,histnum):
    if sprache == 'English':
        dict1 = personen
    else:
        dict1 = personen_de

    personenliste = sorted(dict1.items(), key=itemgetter(1),reverse=True)

    names = list(zip(*personenliste))[0][0:histnum]
    return [{'label': i, 'value': i} for i in names]

@app.callback(
    dash.dependencies.Output('name4', 'options'),
    [dash.dependencies.Input('sprache', 'value'),
     dash.dependencies.Input('histnum', 'value')])
def set_names_options_d(sprache,histnum):
    if sprache == 'English':
        dict1 = personen
    else:
        dict1 = personen_de

    personenliste = sorted(dict1.items(), key=itemgetter(1),reverse=True)

    names = list(zip(*personenliste))[0][0:histnum]
    return [{'label': i, 'value': i} for i in names]

@app.callback(
    dash.dependencies.Output('name5', 'options'),
    [dash.dependencies.Input('sprache', 'value'),
     dash.dependencies.Input('histnum', 'value')])
def set_names_options_e(sprache,histnum):
    if sprache == 'English':
        dict1 = personen
    else:
        dict1 = personen_de

    personenliste = sorted(dict1.items(), key=itemgetter(1),reverse=True)

    names = list(zip(*personenliste))[0][0:histnum]
    return [{'label': i, 'value': i} for i in names]

@app.callback(
    dash.dependencies.Output('name6', 'options'),
    [dash.dependencies.Input('sprache', 'value'),
     dash.dependencies.Input('histnum', 'value')])
def set_names_options_f(sprache,histnum):
    if sprache == 'English':
        dict1 = personen
    else:
        dict1 = personen_de

    personenliste = sorted(dict1.items(), key=itemgetter(1),reverse=True)

    names = list(zip(*personenliste))[0][0:histnum]
    return [{'label': i, 'value': i} for i in names]

def zeitKorr(startsegment, endsegment, namea, nameb, sprache):
    datesegment = pd.date_range(start=startsegment, end=endsegment).tolist()
    datesegment = pd.to_datetime((datesegment))

    if sprache == 'English':
        dicti1 = datumkompakt[namea]
        dicti2 = datumkompakt[nameb]
    else:
        dicti1 = datumkompakt_de[namea]
        dicti2 = datumkompakt_de[nameb]

    y_werte1 =[]
    y_werte2 =[]

    for date in datesegment:
        if str(date).split()[0] in dicti1:
            y_werte1.append(dicti1[str(date).split()[0]])
        else:
            y_werte1.append(0)

    for date in datesegment:
        if str(date).split()[0] in dicti2:
            y_werte2.append(dicti2[str(date).split()[0]])
        else:
            y_werte2.append(0)

    return pearsonr(y_werte1,y_werte2)[0]

@app.callback(
    dash.dependencies.Output('relationplot', 'figure'),
    [dash.dependencies.Input('datumrange', 'start_date'),
     dash.dependencies.Input('datumrange', 'end_date'),
     dash.dependencies.Input('sprache', 'value'),
     dash.dependencies.Input('name5', 'value'),
     dash.dependencies.Input('name6', 'value')
     ])
def update_figure_c(startdatum,enddatum,sprache,name5,name6):

    datelist = pd.date_range(start=startdatum, end=enddatum).tolist()
    datelist = pd.to_datetime((datelist))

    corr_zeit = []
    for date in datelist[:]:
        corr_zeit.append(zeitKorr(date, date + pd.DateOffset(days=30),name5,name6,sprache))

    trace1 = go.Scatter(
    x = datelist,
    y = corr_zeit,
    mode = 'lines'
    )

    return {
        'data': [trace1],
        'layout': go.Layout(
            xaxis={'title': 'Date'},
            yaxis={'title': 'Correlation'},
            legend={'x': 0, 'y': 1},
            height=700,
            title='Correlation over time'
        )
    }



if __name__ == '__main__':
    app.run_server()
