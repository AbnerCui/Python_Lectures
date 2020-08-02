#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 30 23:22:12 2020

@author: abner
"""

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


## 使用ployly需要在官网注册，注册之后或得秘钥方可运行

'''
Data source: Johns Hopkins University (CSSEGISandData) [Keeps updating everyday]
https://github.com/CSSEGISandData/COVID-19/tree/master/csse_covid_19_data/csse_covid_19_time_series
'''

confirmed = 'data/time_series_covid19_confirmed_global.csv'
death = 'data/time_series_covid19_deaths_global.csv'


world_data_confirmed = pd.read_csv(confirmed)
world_data_death = pd.read_csv(death)
def get_country_new_report(country):
    if (country != 'World'):
        nation_df = world_data_confirmed.groupby('Country/Region').sum().loc[country].to_frame().iloc[2:].T
    elif (country=='World'):
        nation_df = world_data_confirmed.groupby('Country/Region').sum().sum(axis = 0, skipna = True).to_frame().iloc[2:].T.rename(index={0: 'World'})
    

    li = []
    for each in range(0,len(nation_df.columns.values)-1):
        x = int(nation_df[[str(nation_df.columns.values[each+1])]].iloc[0]) - int(nation_df[[str(nation_df.columns.values[each])]].iloc[0])
        li.append(x)
    data = {str(country):li} 
    df = pd.DataFrame(data, index =nation_df.columns.values[1:])
    return df.T

def plot_new_day_cases(country):
    date=get_country_new_report(country).columns.values
    fig = go.Figure([go.Bar(x=date, y=get_country_new_report(country).loc[country].to_list())])
    fig.update_layout(
        title='New reports everyday <b>(' + country+')</b>',
        yaxis=dict(
        title='Infected patients',
        titlefont_size=16,
        tickfont_size=14)
    )
    fig.show()
    
get_country_new_report('India')
    

    
    
india_pd = get_country_new_report('India')
india_cumulative_pd = world_data_confirmed.groupby(['Country/Region']).sum().loc[ 'India' , : ].to_frame().T
    
fig = px.line(india_pd, 
              x=india_cumulative_pd.columns.values[2:], 
              y=india_cumulative_pd.iloc[0].values[2:] )
fig.update_layout(
    title="Total Confirmed Cases in <b>India</b>",
    xaxis_title="Days",
    yaxis_title="People Infected",
    font=dict(
        family="Arial",
        size=13,
        color="#7f7f7f"
    )
)
fig.show()

fig = go.Figure()
x = []

fig.add_trace(go.Scatter(x=india_cumulative_pd.columns.values[2:],
                         y=india_cumulative_pd.iloc[0].values[2:] ,
                         mode='lines+markers',
                         name='Total Confirmed'))
fig.add_trace(go.Scatter(x=india_pd.columns.values,
                         y=india_pd.iloc[0].values,
                         mode='lines+markers',
                         name='Daily Confirmed'))

fig.update_layout(
        title='Total Confirmed Cases vs Daily Confirmed <b>(India)</b>',
        yaxis=dict(
        title='Infected population',
        titlefont_size=16,
        tickfont_size=14)
    )

fig.show()


def sum_column(df):
    if df.iloc[:,-1].isnull().values.any():
        df = df.iloc[:, :-1]
    sum = df.sum(axis=0)
    return sum[world_data_confirmed.columns[4:]].to_frame()

def after_hundred(country):
    li = world_data_confirmed.groupby(['Country/Region']).sum().loc[ country , : ].to_frame().T.values.tolist()[0][2:]
    x = []
    for each in range(0,len(li)):
        if li[each]>=100:
            x.append(li[each])
    return x
x_val = [ x for x in range(70)]
n = []
for each in range(0, len(x_val)):
    n.append(1000000)
npa = np.asarray(n, dtype=np.float32)
fig = go.Figure()

df_to_plot_world_confirm = sum_column(world_data_confirmed)

fig.add_trace(go.Scatter(
    x=x_val,
    y=npa,
    mode='lines',
    name='1 Million Mark'
))

fig.add_trace(go.Scatter(
    x=x_val,
    y=after_hundred('US'),
    mode='lines',
    name='US'
))


fig.add_trace(go.Scatter(
    x=x_val,
    y=after_hundred('Italy'),
    mode='lines',
    name='Italy'
))
fig.add_trace(go.Scatter(
    x=x_val,
    y=after_hundred('Spain'),
    mode='lines',
    name='Spain'
))
fig.add_trace(go.Scatter(
    x=x_val,
    y=after_hundred('India'),
    mode='lines',
    name='India'
))
fig.add_trace(go.Scatter(
    x=x_val,
    y=after_hundred('Japan'),
    mode='lines',
    name='Japan'
))
fig.add_trace(go.Scatter(
    x=x_val,
    y=after_hundred('Singapore'),
    mode='lines',
    name='Singapore'
))




fig.update_layout(yaxis_type="log")
fig.update_layout(
        title='How is India Doing Compared to <b> US, Spain, Italy, and others?</b>',
        yaxis=dict(
        title='Infected people',
        titlefont_size=16,
        tickfont_size=14),
    xaxis=dict(
        title='Days after 100 infection',
        titlefont_size=16,
        tickfont_size=14)
    )
fig.show()


def sum_column(df):
    if df.iloc[:,-1].isnull().values.any():
        df = df.iloc[:, :-1]
    sum = df.sum(axis=0)
    return sum[world_data_confirmed.columns[4:]].to_frame()

def after_hundred(country):
    li = world_data_death.groupby(['Country/Region']).sum().loc[ country , : ].to_frame().T.values.tolist()[0][2:]
    x = []
    for each in range(0,len(li)):
        if li[each]>=5:
            x.append(li[each])
    return x
x_val = [ x for x in range(70)]
n = []
for each in range(0, len(x_val)):
    n.append(100000)
npa = np.asarray(n, dtype=np.float32)
fig = go.Figure()

df_to_plot_world_confirm = sum_column(world_data_confirmed)

fig.add_trace(go.Scatter(
    x=x_val,
    y=npa,
    mode='lines',
    name='100000 Mark'
))





fig.add_trace(go.Scatter(
    x=x_val,
    y=after_hundred('Spain'),
    mode='lines',
    name='Spain'
))
fig.add_trace(go.Scatter(
    x=x_val,
    y=after_hundred('Italy'),
    mode='lines',
    name='Italy'
))
fig.add_trace(go.Scatter(
    x=x_val,
    y=after_hundred('US'),
    mode='lines',
    name='US'
))
fig.add_trace(go.Scatter(
    x=x_val,
    y=after_hundred('India'),
    mode='lines',
    name='India'
))




fig.update_layout(yaxis_type="log")
fig.update_layout(
        title='How is India Doing Compared to <b> US, Spain, Italy, and others?</b>',
        yaxis=dict(
        title='Deaths',
        titlefont_size=16,
        tickfont_size=14),
    xaxis=dict(
        title='Days',
        titlefont_size=16,
        tickfont_size=14)
    )
fig.show()
    
    
    
    
    
    