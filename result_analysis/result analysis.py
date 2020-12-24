import os
import pandas as pd
import quantstats as qs

from pymongo import MongoClient
client = MongoClient('localhost', 27017)
db = client["JointQuant"]


path='E:\\code\\portfolio\\PGPortfolio\\train_package\\APG\\'
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
          


    