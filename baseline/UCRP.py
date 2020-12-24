# uniform constant-rebalanced portfolio
# 每天进行调整，将资产平均分配在每一个股票上
import pandas as pd
import numpy as np
from pymongo import MongoClient
client = MongoClient('localhost', 27017)
db = client["JointQuant"]
allFund = 0
allCash = 1000000
stockList = ["600036", "601166", "601398", "601328", "000001", "600000", "600016"]

startDate = '2019-04-04'
endDate = '2019-12-31'
df_all = pd.DataFrame(columns=stockList)
for one in stockList:
    df = pd.DataFrame(list(db[one].find().sort('date'))).set_index('date')
    df = df.loc[startDate:endDate]['close']
    df_all[one] = df       

df_all['assetDF'] = None
assetDFList = []
numList = [0]*len(stockList)
for oneDay in df_all.index:
    stockPrice = df_all.loc[oneDay]
    allFund = np.dot(stockPrice.values[:len(stockList)], numList)
    numList = []  
    for stock_i in range(len(stockList)):
        num = int((allFund+allCash)/(len(stockList)*100*stockPrice[stock_i]))*100
        numList.append(num)
    allCash = allFund + allCash - np.dot(stockPrice.values[:len(stockList)], numList)
    allFund = np.dot(stockPrice.values[:len(stockList)], numList)
    assetDFList.append(allFund+allCash)
df_all['assetDF'] = assetDFList
    
    
    
        
        
        