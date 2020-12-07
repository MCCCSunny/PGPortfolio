# 平均权重进行交易
import pandas as pd

from pymongo import MongoClient
client = MongoClient('localhost', 27017)
db = client["JointQuant"]

cash = 1000000
stockList = ["600036", "601166", "601398", "601328", "000001", "600000", "600016"]

startDate = '2019-04-04'
endDate = '2019-12-31'
allProfit = 0
for one in stockList:
    df = pd.DataFrame(list(db[one].find().sort('date'))).set_index('date')
    lastPrice = df.loc[endDate]['close']
    startPrice = df.loc[startDate]['close']
    num_ = int(cash/(len(stockList)*startPrice*100)) *100
    profit = num_*(lastPrice-startPrice)
    allProfit += profit
print ("all profit is %f"%allProfit)