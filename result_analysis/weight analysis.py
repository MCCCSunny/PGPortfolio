import numpy as np
import pandas as pd
from sklearn import preprocessing
import matplotlib.pyplot as plt
import matplotlib as mpl
import seaborn as sns
from pymongo import MongoClient
client = MongoClient('localhost', 27017)
db = client["JointQuant"]

stockDict = {'1':  ["600000", "002032", "600498", "000768", "600221"], 
             '11': ["600519", "000858", "000661", "001914", "000651"],
             '21': ["600030", "600703", "600050", "600837", "600031"]}
stockList = ["600000", "002032", "600498", "000768", "600221"]
start = '2019-01-04'
end = '2019-12-31'
df_all = pd.DataFrame(columns=stockList)
for oneStock in stockList:
    df = pd.DataFrame(list(db[oneStock].find().sort('date'))).set_index('date')[['close']].loc[start:end]
    df_all[oneStock] =  df['close']
# 填补缺失值
df_all1 = df_all.fillna(method='ffill').iloc[1:]
# 对数据进行正则化
df_scaled = preprocessing.scale(df_all1.values)
df_new = pd.DataFrame(columns = df_all1.keys().tolist(), index=df_all1.index.tolist())
for i in range(df_scaled.shape[1]):
    df_new[stockList[i]] = df_scaled[:,i]
df_new.to_excel('E:\\code\\portfolio\\PGPortfolio\\result_analysis\\'+'set1.xlsx')
'''
for i in range(df_scaled.shape[1]):
    plt.plot(df_scaled[:,i], label=stockList[i])
plt.legend(loc='best')
'''
w_names = ['w1', 'w2', 'w3', 'w4', 'w5', 'w6', 'w7', 'w8', 'w9', 'w10']
#path= 'E:\\code\\portfolio\\PGPortfolio\\train_package\\GRU_EIIE\\1\\'
path = 'E:\\code\\portfolio\\PGPortfolio_trend\\train_package\\LSTM_EIIE_loss_trend\\1\\'
df_w = pd.read_csv(path+'netfile_backtest_df.csv')
df_w = df_w.set_index('date')[['omega', 'total_capital']]
df_w_all = pd.DataFrame(index=df_w.index, columns=w_names[:len(stockList)+1])
for i in range(len(df_w)):
    w_str = df_w.iloc[i]['omega'][1:-1].split(' ')
    w_str1 = []
    for onew in w_str:
        try:
            w_i = float(onew)
            w_str1.append(w_i)
        except:
            pass
    df_w_all.iloc[i]=w_str1
df_w_all = df_w_all.iloc[:,:len(stockList)]
df_w_all.to_excel(path+"weight.xlsx")


path_loss_trend = 'E:\\code\\portfolio\\PGPortfolio_trend\\train_package\\LSTM_EIIE_loss_trend\\1\\'
#path_loss_trend = 'E:\\code\\portfolio\\PGPortfolio\\train_package\\LSTM_EIIE\\1\\'
df_w = pd.read_csv(path+'netfile_backtest_df.csv')
df_w = df_w.set_index('date')[['omega', 'total_capital']]
df_w_all = pd.DataFrame(index=df_w.index, columns=w_names[:len(stockList)+1])
for i in range(len(df_w)):
    w_str = df_w.iloc[i]['omega'][1:-1].split(' ')
    w_str1 = []
    for onew in w_str:
        try:
            w_i = float(onew)
            w_str1.append(w_i)
        except:
            pass
    df_w_all.iloc[i]=w_str1
df_w_all = df_w_all.iloc[:,:len(stockList)]
df_w_all.to_excel(path_loss_trend+"weight.xlsx")

'''
# cmap用matplotlib colormap    
x_label = list(df_w_all.index)
y_label = list(df_w_all.keys())
fig, ax = plt.subplots(figsize=(15, 6))
# 绘制热力图    cmap：从数字到色彩空间的映射
df_w_all = df_w_all.ix[:,:len(stockList)].astype(float)
sns.heatmap(data=df_w_all.T,cmap="YlGnBu")#, ax=ax, cmap='OrRd', robust=True)
'''
