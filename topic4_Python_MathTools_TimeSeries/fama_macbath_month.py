# -*- coding: utf-8 -*-
"""
Created on Mon Jul 27 14:25:51 2020

@author: a
"""
import sys
import os
sys.path.append('E:/宏观因子_前瞻')

import pandas as pd
import numpy as np
from translate import Translator
import statsmodels.api as sm
import datetime
from numpy import mat, cov, mean, hstack, multiply,sqrt,diag, squeeze, ones, array, vstack, kron, zeros, eye, savez_compressed
#
from fama_macbath import *
from sklearn.decomposition import PCA

    #Monthly data
data_4 = pd.read_excel('E:/宏观因子_前瞻/月/宏观/CPI当月同比(月).xls')
data_5 = pd.read_excel('E:/宏观因子_前瞻/月/宏观/RPI当月同比(月).xls')
data_6 = pd.read_excel('E:/宏观因子_前瞻/月/宏观/固定资产投资完成额(月).xls')
data_7 = pd.read_excel('E:/宏观因子_前瞻/月/宏观/规模以上工业增加值当月(月).xls')
data_8 = pd.read_excel('E:/宏观因子_前瞻/月/宏观/国家财政收入(月).xls')
data_9 = pd.read_excel('E:/宏观因子_前瞻/月/宏观/宏观经济景气指数(月).xls')
data_10 = pd.read_excel('E:/宏观因子_前瞻/月/宏观/货币供应量(月).xls')
data_11 = pd.read_excel('E:/宏观因子_前瞻/月/宏观/进出口贸易(月).xls')
data_12 = pd.read_excel('E:/宏观因子_前瞻/月/宏观/克强指数(月).xls')
data_13 = pd.read_excel('E:/宏观因子_前瞻/月/宏观/人民币汇率(月).xls')
data_14 = pd.read_excel('E:/宏观因子_前瞻/月/宏观/社会消费品零售总额当月(月).xls')

    # X数据整理
data_all = merge_data(data_4, data_5, data_6)
data_all = merge_data(data_all, data_7, data_8)
data_all = merge_data(data_all, data_9, data_10)
data_all = merge_data(data_all, data_11, data_12)
data_all = merge_data(data_all, data_13, data_14)
data_all = data_all.drop(index=(data_all.loc[(data_all['指标名称']=='频率')].index))

start_date_x = datetime.datetime(2014, 2, 21, 0, 0, 0, 0)
end_date_x = datetime.datetime(2020, 3, 31, 00, 00, 00, 00)
part_data = data_cut(data_all, start_date_x, end_date_x, '指标名称')
cols=[x for i,x in enumerate(part_data.columns) if part_data.iat[0,i]=='月']

part_data=part_data.drop(cols,axis=1)

#return
part_data.reset_index(drop=True, inplace=True)
for i in part_data.columns[1:]:
    part_data[i] = pd.DataFrame(np.diff(part_data[i]))
X = part_data = part_data.iloc[:-2,:]  
    
    
#normalization
    
del_li = []
for i in range(1, len(X.iloc[-1,:])):
    if X.iloc[-1,i] == 0:
        del_li.append(X.columns[i])
    else:
        continue
X = X.drop(columns=del_li)
    
p = pd.DataFrame(X.iloc[:,0])
for i in range(1, X.shape[1]):  
    norm_list = []
    for j in range(X.shape[0]):         
        data_mean = X.iloc[:,i].mean()
        data_std = X.iloc[:,i].std()
        norm_list.append((X.iloc[j,i] - data_mean)/data_std)
    p[X.columns[i]] = norm_list
        
p = p.dropna(axis=1, how='any') 

dayily_data = del_weekly_monthly(p,60)
independent_variable = translate_indicator(dayily_data)
date1 = []
for i in range(len(independent_variable['Date'])):
    date1.append(independent_variable['Date'][i].strftime("%Y-%m-%d"))
independent_variable['Date'] = date1


start_date_y = '2014-02-21'
end_date_y = '2020-06-18'
data_y = read_Y_data(start_date_y, end_date_y)
return_y = calculate_return(data_y)
dependent_variable = reset_index(return_y)
date2 = []
for i in range(len(dependent_variable['Date'])):
    date2.append(dependent_variable['Date'][i].strftime("%Y-%m-%d"))
dependent_variable['Date'] = date2


dep_var_date = []
dependent_variable_date = dependent_variable['Date']
for i in independent_variable['Date']:
    if i in list(dependent_variable_date):
        dep_var_date.append(i)
    else:
        continue
    
dependent_variable.set_index(['Date'], inplace= True)
dependent_variable = dependent_variable.loc[dep_var_date]
dependent_variable = reset_index(dependent_variable)     
date3 = []
for i in range(len(dependent_variable['Date'])):
    date3.append(dependent_variable['Date'][i].strftime("%Y-%m-%d"))
dependent_variable['Date'] = date3  
    
    
merge_XY = pd.merge(independent_variable,dependent_variable)

x_del =  merge_XY.iloc[:,1:134]
df2 = merge_XY.iloc[:,1:134].corr(method = 'pearson')
def del_corr(p, df2, i):
    del_list = []

    for j in df2.index:
        if df2[i][j]>p and df2[i][j]<1:
            del_list.append(j)
        else:
            continue       
    for c in range(len(del_list)):
        df2 = df2.drop(del_list[c], axis=0)
        df2 = df2.drop(del_list[c], axis=1)
    df2 = x_del[df2.columns]
    df2= df2.corr(method = 'pearson')
    return df2

for i in range(42):
    df2= del_corr(0.5, df2, df2.index[i])
    


pca = PCA(n_components=0.99999999)
newX = pca.fit_transform(x_del.to_numpy())

asq = np.corrcoef(newX.T)
pca_0 = pd.DataFrame(newX)



#134
X_value = x_del[df2.columns].values
#X_value = merge_XY.iloc[:,1:20].values
X = sm.add_constant(X_value)
Y_value = merge_XY.iloc[:,20:].values
ts_res = sm.OLS(Y_value[:,5], X).fit()
cn_res = fisrt_del_bound(0.3,ts_res,X_value, merge_XY)
list_res = del_each_one(cn_res,merge_XY,X_value)

#pca
X = sm.add_constant(newX)
Y_value = merge_XY.iloc[:,20:].values
ts_res = sm.OLS(Y_value[:,12], newX).fit()
cn_res = fisrt_del_bound(0.3,ts_res,newX, pca_0)
list_res = del_each_one(cn_res,pca_0,newX)


