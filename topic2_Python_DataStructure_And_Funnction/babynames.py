# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pyecharts import Bar, Line, Overlap,WordCloud
from pylab import mpl

def read_data(dataname):
    data = pd.read_csv(dataname)
    return data

def popular_name(gender):
    data_decades = data[data['Year']>=1920]
    data_decades['decade'] = pd.cut(data_decades['Year'], [1920,1930,1940,1950,1960,1970,1980,1990,2000,2010,2018], 
                                    labels = ['20s','30s','40s', '50s','60s','70s','80s','90s','00s','10s'],right=False)
    
    decade = data_decades.groupby(['decade', 'Gender', 'Name']).Count.sum().groupby(level=[0,1]).nlargest(1)
    
    decade_boy_count = decade.iloc[decade.index.get_level_values(3)==gender].reset_index(level=[0,1,3], drop=True)
    decade_boy_total = data_decades[data_decades['Gender']==gender].groupby('decade').Count.sum()
    decade_boy_pct = (decade_boy_count/decade_boy_total*100).round(2)
    ax = decade_boy_pct.plot.barh(title='Popular'+gender+'name')
    ax.set_ylabel('')
    ax.set_xlabel('percentage')
    
    
def name_trend(name, data, gender=['M','F'], year=1920, dodge = 500):
    if isinstance(gender, str):
        name_data = data[(data['Name'] == name)&(data['Gender']==gender)&(data['Year']>=year)]
        attr = list(name_data['Year'].values)
        bar = Bar(name)
        bar.add("", attr, list(name_data['Count'].values), mark_line=["average"], mark_point=["max", "min"],
               legend_text_size=18,xaxis_label_textsize=18,yaxis_label_textsize=18)
        line = Line()
        line.add("", attr, list(name_data['Count'].values + dodge))
        
    else:
        name_data = data[(data['Name'] == name)&(data['Year']>=year)]
        attr = list(range(year, 2018))
        v1 = name_data[name_data['Gender']==gender[0]].Count.values
        v2 = name_data[name_data['Gender']==gender[1]].Count.values
        bar = Bar(name)
        bar.add("男", attr, list(v1), legend_text_size=18,xaxis_label_textsize=18,yaxis_label_textsize=18)
        bar.add("女", attr, list(v2), legend_text_size=18,xaxis_label_textsize=18,yaxis_label_textsize=18)
        line = Line()
        line.add("", attr, list(v1 + dodge))
        line.add("", attr, list(v2 + dodge))
    
    overlap = Overlap()
    overlap.add(bar)
    overlap.add(line)
    return overlap.render(str(name)+str(gender)+str(dodge)+'.html')

def popular_name(gener):
    top15_boy = data.loc[(data['Year'].isin(list(range(2010,2018)))) & (data['Gender'] == 'M'), :].groupby('Name').Count.sum().nlargest(15)
    boy_total = data.loc[(data['Year'].isin(list(range(2010,2018)))) & (data['Gender'] == 'M'), :].groupby('Name').Count.sum().sum()
    
    name = list(top15_boy.index)
    value = list(top15_boy.values)
    wordcloud = WordCloud(width=800, height=450,background_color='#f2eada')  # feeeed
    wordcloud.add("", name, value, word_size_range=[20, 100],shape='diamond')
    return wordcloud.render('popolar name'+str(gener)+'.html')

if __name__ == '__main__':
    
    data=read_data('NationalNames.csv')
    #popular_name('M')
    #name_trend('Jordan',data,gender='M',year=1960)
    popular_name('M')
        
    
    
    