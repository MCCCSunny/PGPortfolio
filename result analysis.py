import os
import pandas as pd
import quantstats as qs

from pymongo import MongoClient
client = MongoClient('localhost', 27017)
db = client["JointQuant"]

path='F:\\study\\ml\\code\\PGPortfolio\\train_package\\CNN_capsule_EIIE\\'
dir_ = os.listdir(path)

for onefile in dir_:
    if onefile.isnumeric():
        try:
            df0 = pd.DataFrame([[None, 1000000]], columns=['omega','total_capital'])
            df = pd.read_csv(path+onefile+'\\netfile_backtest_df.csv')
            df = df.set_index('date')
            df = df[['omega', 'total_capital']]
            df = pd.concat([df0, df])
            final_asset_value = df.iloc[-1]['total_capital']
            # 利润
            profit = final_asset_value - df.iloc[0]['total_capital']          
            # 夏普率
            SR = qs.stats.sharpe(df['total_capital'])
            # MDD
            max_return = max(df['total_capital'])
            allValueList = df['total_capital'].values
            index_ = list(allValueList).index(max_return)
            min_return = min(allValueList[index_:])
            MDD = (min_return-max_return)/max_return
            print ('file %s: the profit of %f, SR is %f, MDD is %f'%(onefile, profit, SR, MDD))
            
        except:
            pass
          
# 平均权重进行交易
cash=1000000
stockList = ["600036", "601166", "601398", "601328", "000001", "600000", "600016"]
#["600030", "600703", "600050", "600837", "600031"]
#["600000", "002032", "600498", "000768", "600221"]
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
    
    