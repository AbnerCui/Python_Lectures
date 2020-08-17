# -*- coding: utf-8 -*-
"""
Created on Thu Jul  2 11:47:16 2020

@author: a
"""

import pandas as pd
import numpy as np
from translate import Translator
import statsmodels.api as sm
import datetime
from numpy import mat, cov, mean, hstack, multiply,sqrt,diag, squeeze, ones, array, vstack, kron, zeros, eye, savez_compressed







#%%
#read daily macro data
'''
data_1 = pd.read_excel('E:/宏观因子_前瞻/日/宏观/人民币汇率(日).xls')
data_2 = pd.read_excel('E:/宏观因子_前瞻/日/宏观/交易所债券指数(日).xls')
data_3 = pd.read_excel('E:/宏观因子_前瞻/日/宏观/股票市场总体指标(日).xls')
'''
# 自变量数据处理
def merge_data(data1, data2, data3):
    data_concat = pd.merge(data1,data2, on=['指标名称'])
    data_concat = pd.merge(data_concat,data3, on=['指标名称'])
    
    data_del = data_concat.drop(index=(data_concat.loc[(data_concat['指标名称']=='数据来源: 中债估值中心')].index))
    data_del = data_del.drop(index=(data_del.loc[(data_del['指标名称']=='数据来源：Wind')].index))
    data_merge = data_del.fillna(method='bfill')
    return data_merge
#data_del = data_del.drop(columns=['活期存款利率' ,'定期存款利率:1年(整存整取)','人民银行对金融机构存款利率:法定准备金'])
#data_del_nan = data_del.dropna(axis=1,how='all') 
#data_del_nan = data_del_nan.dropna(axis=0,how='any')

#2014-02-07--2020-06-17的数据
#name_list = data_del.columns.values.tolist()
'''
start_date = datetime.datetime(2019, 6, 18, 0, 0, 0, 0)
end_date = datetime.datetime(2020, 6, 18, 00, 00, 00, 00)
'''
def data_cut(all_data, start_dat, end_dat, indicator):
    all_data = all_data[(all_data[indicator]>=start_dat)]
    all_data = all_data[(all_data[indicator]<=end_dat)]

    part_data = all_data.dropna(axis=1, how='any') 
    return part_data


'''
del_list = []
for i in range(1, len(name_list[0:])):
    if  np.isnan(data_del.iloc[0,i])  == True:
        del_list.append(name_list[i])
    
    else:
        continue
    
data_del = data_del.drop(columns=del_list)
'''
# calculate the return
def calculate_return_norm(part_data):
    
    for i in part_data.columns[1:]:
        part_data[i] = np.diff(part_data[i])/part_data[i].iloc[:-1]
    
    # del the last two line in data_del
    
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
    return p

#delete the weekly and monthly data
def del_weekly_monthly(p, number):
    week_monthdata = []
    for i in p.columns:
        if  (len(np.unique(p[i]))<int(number)) == True:
            week_monthdata.append(i)
        else:
            continue
    s = p.drop(columns=week_monthdata)
    return s

'''
#method2
for i in range(data_del.shape[1]-1):
    for j in range(data_del.shape[0]):
        if j < data_del.shape[0]-2:
            data_del.iloc[j, i+1] = data_del.iloc[j+1,i+1]-data_del.iloc[j,i+1]
        else:
            data_del.iloc[j, i+1] = data_del.iloc[j, i+1]
'''


def translate_indicator(p):
# translate the indicators
    translator = Translator(from_lang="chinese",to_lang="english")
    
    columns_list_c = p.columns.tolist()
    columns_list_eng = []
    for i in columns_list_c:
        columns_list_eng.append(translator.translate(i))
    
    columns_list = []
    for i in columns_list_eng:
        columns_list.append(i.replace(' ','_'))
    
    p.columns=columns_list
    p = p.rename(columns={'Indicators':'Date'})
    
    x = p
    return x
#%%
# 因变量数据处理
def read_Y_data(start_date, end_date):
    industry_list = pd.read_csv('E:/lists.csv')
    industry_list = list(industry_list['industry'])

    data_list = []
    for i in industry_list:
        ddt = pd.read_csv('E:/data/'+str(i)+'.csv')
        ddt = ddt.rename(columns={'close':str(i)+'close'})
        ddt = ddt.set_index('Date')
        ddt = ddt.loc[start_date:end_date][str(i)+'close']
        #ddt_df = {'Date':ddt.index, str(i)+'close':ddt.values}
        data_list.append(ddt)
    
    pd_close = pd.DataFrame(data_list).T
    pd_close = pd_close.fillna(method='bfill')
    return pd_close
# calculate the return
def calculate_return(y):
    for i in range(y.shape[1]):
        for j in range(y.shape[0]):
            if j < y.shape[0]-1:
                y.iloc[j, i] = y.iloc[j+1,i]-y.iloc[j,i]
            else:
                y.iloc[j, i] = y.iloc[j, i]
              
    Y = y.iloc[:-1,:] 
    return Y
def reset_index(Y):
    import datetime
    Y = Y.reset_index()
    Y.rename(columns={'index':'Date'}, inplace=True)
    list2 = Y['Date'].tolist()
    list3 = []
    for i in list2:
        list3.append(i+" "+"00:00:00")
    list4 = []
    for i in list3:
        list4.append(datetime.datetime.strptime(i, "%Y-%m-%d %H:%M:%S"))
    
    Y['Date'] = list4
    return Y


#%%
# Time series regressions

##############

def find_index(x,c):
    pval_03_index = []
    for i in range(len(c)):
        pval_03_index.append(list(x.pvalues).index(c[i]))
    return pval_03_index

def fisrt_del_bound(pvalue1,ts_res,X_value, merge_XY):
    list(ts_res.pvalues).sort(reverse=True)
    
    pval_03 = []
    for i in range(len(ts_res.pvalues)-1):
        if ts_res.pvalues[i+1]<=pvalue1:
            pval_03.append(ts_res.pvalues[i+1])
        else:
            continue
    pval_03.sort(reverse=True)
    
    pval_03_cal = pval_03[:]
    
    
    #if pval_03_cal[0]>0.05:
    #    del pval_03_cal[0]
            
    pval_03_index = find_index(ts_res, pval_03_cal)
            
    #for i in range(len(pval_03_index)):
    #    pval_03_index[i] = pval_03_index[i] + 1
            
    in_var = merge_XY.iloc[:,pval_03_index].values
    in_var = sm.add_constant(in_var)
    de_var = X_value
    cn_res = sm.OLS(de_var[:,1], in_var).fit()
    return cn_res

def del_each_one(cn_res,merge_XY,X_value):
    for i in range(len(cn_res.pvalues)-1):
    
        list1 = list(cn_res.pvalues[1:])
        list1.sort(reverse=True)
        if list1[0]>0.05:
            del list1[0]
        else:
            break
        
        '''
        a = a[9:]    
        pval_05_index = find_index(cn_res, a)
        for i in range(len(pval_05_index)):
            pval_05_index[i] = pval_05_index[i] + 1
        
        '''
        
        
        pval_05_index = find_index(cn_res, list1)
            
        #for i in range(len(pval_05_index)):
        #    pval_05_index[i] = pval_05_index[i] + 1
            
        in_var = merge_XY.iloc[:,pval_05_index].values
        in_var = sm.add_constant(in_var)
        de_var = X_value
        cn_res = sm.OLS(de_var[:,1], in_var).fit()
        i = i+1
    return cn_res


'''
less_005_index = find_index(pval_03_cal)
for i in range(len(less_005_index)):
    less_005_index[i] = less_005_index[i] + 1


pval03_all_index = find_index(pval_03)
res_pval_03 = []
for i in pval03_all_index:
    if i not in less_005_index:
        res_pval_03.append(i)
    else:
        continue


z=merge_XY.iloc[:,res_pval_03 and pval_03]


ts_res = sm.OLS(Y_value, X).fit()
alpha = ts_res.params[0]
beta = ts_res.params[1:]
avgExcessReturns = mean(Y_value, 0)

#%%
# Cross-section regression
cs_res = sm.OLS(avgExcessReturns.T, beta.T).fit()
riskPremia = cs_res.params
cs_res.summary()
'''
#%%




if __name__ =='__main__':
    # dayily data
    data_1 = pd.read_excel('人民币汇率(日).xls')
    data_2 = pd.read_excel('交易所债券指数(日).xls')
    data_3 = pd.read_excel('股票市场总体指标(日).xls')
    
    
    #data_4 = pd.read_csv('E:/宏观因子_前瞻/801001_features.csv')
    #part_data = data_cut(data_4, start_date_x, end_date_x, 'Date')
    
    
    
    # X数据整理
    data_all = merge_data(data_1, data_2, data_3)
    data_all = data_all.drop(index=(data_all.loc[(data_all['指标名称']=='频率')].index))
    start_date_x = datetime.datetime(2019, 6, 18, 0, 0, 0, 0)
    end_date_x = datetime.datetime(2020, 6, 18, 00, 00, 00, 00)
    part_data = data_cut(data_all, start_date_x, end_date_x, '指标名称')
    return_norm_data = calculate_return_norm(part_data)
    dayily_data = del_weekly_monthly(return_norm_data,230)
    independent_variable = translate_indicator(dayily_data)
    #independent_variable = independent_variable.reset_index(drop=True)
    independent_variable.set_index(['Date'], inplace=True)

    #Y数据整理
    start_date_y = '2019-06-18'
    end_date_y = '2020-06-18'
    data_y = read_Y_data(start_date_y, end_date_y)
    return_y = calculate_return(data_y)
    dependent_variable = reset_index(return_y)
    dependent_variable.set_index(['Date'], inplace=True)
    
    #查看两个列表中不同的行
    inde = [x for x in list(independent_variable.index) if x not in list(dependent_variable.index)]
    de = [y for y in list(dependent_variable.index) if y not in list(independent_variable.index)]
    independent_variable = independent_variable.drop(inde)
    dependent_variable = dependent_variable.drop(de)
    
    
    
    merge_XY = pd.merge(independent_variable,dependent_variable, on = 'Date')
    merge_XY.reset_index()
    
    #OLS
    X_value = merge_XY.iloc[:,1:114].values
    X = sm.add_constant(X_value)
    Y_value = merge_XY.iloc[:,114:].values
    ts_res = sm.OLS(Y_value[:,1], X).fit()
    cn_res = fisrt_del_bound(0.3,ts_res,X_value, merge_XY)
    list_res = del_each_one(cn_res,merge_XY,X_value)
    
    
    '''
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
    data_15 = pd.read_excel('E:/宏观因子_前瞻/月/宏观/外商直接投资(月).xls')
    # X数据整理
    data_all = merge_data(data_4, data_5, data_6)
    data_all = merge_data(data_all, data_6, data_7)
    start_date_x = datetime.datetime(2019, 6, 18, 0, 0, 0, 0)
    end_date_x = datetime.datetime(2020, 6, 18, 00, 00, 00, 00)
    part_data = data_cut(data_all, start_date_x, end_date_x)
    return_norm_data = calculate_return_norm(part_data)
    dayily_data = del_weekly_monthly(return_norm_data)
    independent_variable = translate_indicator(dayily_data)
    '''
    


