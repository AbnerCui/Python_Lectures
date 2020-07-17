import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib as mpl
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
sns.set_style({'font.sans-serif':['simhei','Arial']})

def price_comparation():

    shanghai = pd.read_csv('sh.csv')# 将已有数据导进来
    shanghai.dropna(inplace=True)
    df=shanghai.copy()
    house_desc=df['house_desc']
    df['layout']=df['house_desc'].map(lambda x:x.split('|')[0])
    df['area']=df['house_desc'].map(lambda x:x.split('|')[1])
    df['temp']=df['house_desc'].map(lambda x:x.split('|')[2])
    df['floor']=df['temp'].map(lambda x:x.split('/')[0])

    df['area']=df['area'].apply(lambda x:x.rstrip('平'))
    df['singel_price']=df['singel_price'].apply(lambda x:x.rstrip('元/平'))
    df['singel_price']=df['singel_price'].apply(lambda x:x.lstrip('单价'))
    df['district']=df['district'].apply(lambda x:x.rstrip('二手房'))
    df['house_time']=df['house_time'].apply(lambda x:str(x))
    df['house_time']=df['house_time'].apply(lambda x:x.rstrip('年建'))

    del df['house_img']
    del df['s_cate_href']
    del df['house_desc']
    del df['zone_href']
    del df['house_href']
    del df['temp']

    df['singel_price']=df['singel_price'].apply(lambda x:float(x))
    df['area']=df['area'].apply(lambda x:float(x))
    df['house_title']=df['house_title'].apply(lambda x:str(x))
    df['trafic']=df['house_title'].apply(lambda x:'交通便利' if x.find("交通便利")>=0 or x.find("地铁")>=0 else "交通不便"  )

    df_house_count = df.groupby('district')['house_price'].count().sort_values(ascending=False).to_frame().reset_index()
    df_house_mean = df.groupby('district')['singel_price'].mean().sort_values(ascending=False).to_frame().reset_index()

    f, [ax1,ax2,ax3] = plt.subplots(3,1,figsize=(20,15))
    sns.barplot(x='district', y='singel_price', palette="Reds_d", data=df_house_mean, ax=ax1)
    ax1.set_title('上海各大区二手房每平米单价对比',fontsize=15)
    ax1.set_xlabel('区域')
    ax1.set_ylabel('每平米单价')
    sns.countplot(df['district'], ax=ax2)
    sns.boxplot(x='district', y='house_price', data=df, ax=ax3)
    ax3.set_title('上海各大区二手房房屋总价',fontsize=15)
    ax3.set_xlabel('区域')
    ax3.set_ylabel('房屋总价')
    plt.show()



def price_prediction():
    shanghai = pd.read_csv('sh.csv')# 将已有数据导进来
    shanghai.dropna(inplace=True)
    df=shanghai.copy()
    house_desc=df['house_desc']
    df['layout']=df['house_desc'].map(lambda x:x.split('|')[0])
    df['area']=df['house_desc'].map(lambda x:x.split('|')[1])
    df['temp']=df['house_desc'].map(lambda x:x.split('|')[2])
    df['floor']=df['temp'].map(lambda x:x.split('/')[0])

    df['area']=df['area'].apply(lambda x:x.rstrip('平'))
    df['singel_price']=df['singel_price'].apply(lambda x:x.rstrip('元/平'))
    df['singel_price']=df['singel_price'].apply(lambda x:x.lstrip('单价'))
    df['district']=df['district'].apply(lambda x:x.rstrip('二手房'))
    df['house_time']=df['house_time'].apply(lambda x:str(x))
    df['house_time']=df['house_time'].apply(lambda x:x.rstrip('年建'))

    del df['house_img']
    del df['s_cate_href']
    del df['house_desc']
    del df['zone_href']
    del df['house_href']
    del df['temp']

    df['singel_price']=df['singel_price'].apply(lambda x:float(x))
    df['area']=df['area'].apply(lambda x:float(x))
    df['house_title']=df['house_title'].apply(lambda x:str(x))
    df['trafic']=df['house_title'].apply(lambda x:'交通便利' if x.find("交通便利")>=0 or x.find("地铁")>=0 else "交通不便"  )

    df_house_count = df.groupby('district')['house_price'].count().sort_values(ascending=False).to_frame().reset_index()
    df_house_mean = df.groupby('district')['singel_price'].mean().sort_values(ascending=False).to_frame().reset_index()

    df[['室', '厅']] = df['layout'].str.extract(r'(\d+)室(\d+)厅')
    df['室'] = df['室'].astype(float)
    df['厅'] = df['厅'].astype(float)
    del df['layout']
    df.dropna(inplace=True)
    del df['house_title']
    del df['house_detail']
    del df['s_cate']

    linear = LinearRegression()
    area = df['area']
    price = df['house_price']
    area = np.array(area).reshape(-1, 1)  # 这里需要注意新版的sklearn需要将数据转换为矩阵才能进行计算
    price = np.array(price).reshape(-1, 1)
    # 训练模型
    model = linear.fit(area, price)
    # 打印截距和回归系数

    print('prediction intercept:', model.intercept_, 'prediction slope:', model.coef_)

    linear_p = model.predict(area)
    plt.figure(figsize=(12, 6))
    plt.scatter(area, price)
    plt.plot(area, linear_p, 'red')
    plt.xlabel("area")
    plt.ylabel("price")
    plt.show()

if __name__ == '__main__':
    price_comparation()
    price_prediction()