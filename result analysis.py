import os
import pandas as pd

path='E:\\code\\portfolio\\PGPortfolio\\train_package\\'
dir_ = os.listdir(path)

for onefile in dir_:
    if onefile.isnumeric():
        try:
            df = pd.read_csv(path+onefile+'\\netfile_backtest_df.csv')
            final_asset_value = df.iloc[-1]['total_capital']
            profit = final_asset_value - 1e5
            print ('the profit of %s is %f'%(onefile, profit))
        except:
            pass