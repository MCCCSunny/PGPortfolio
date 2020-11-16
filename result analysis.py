import os
import pandas as pd
import quantstats as qs

from pymongo import MongoClient
client = MongoClient('localhost', 27017)
db = client["JointQuant"]

path='E:\\code\\portfolio\\PGPortfolio\\train_package\\LSTM_EIIE\\'
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
'''
cash=1000000
stockList = ["600036", "601166", "601398", "601328", "000001", "600000", "600016"]
#["600030", "600703", "600050", "600837", "600031"]
#["600000", "002032", "600498", "000768", "600221"]scipy.optimize._lsap_module, scipy.optimize._differentialevolution, scipy.optimize._shgo, scipy.optimize._shgo_lib, scipy.optimize._shgo_lib.sobol_seq, scipy.optimize._shgo_lib.triangulation, scipy.optimize._dual_annealing, scipy.integrate, scipy.integrate._quadrature, scipy.integrate.odepack, scipy.integrate._odepack, scipy.integrate.quadpack, scipy.integrate._quadpack, scipy.integrate._ode, scipy.integrate.vode, scipy.integrate._dop, scipy.integrate.lsoda, scipy.integrate._bvp, scipy.integrate._ivp, scipy.integrate._ivp.ivp, scipy.integrate._ivp.bdf, scipy.integrate._ivp.common, scipy.integrate._ivp.base, scipy.integrate._ivp.radau, scipy.integrate._ivp.rk, scipy.integrate._ivp.dop853_coefficients, scipy.integrate._ivp.lsoda, scipy.integrate._quad_vec, scipy.misc, scipy.misc.doccer, scipy.misc.common, scipy.stats._constants, scipy.stats._continuous_distns, scipy.interpolate, scipy.interpolate.interpolate, scipy.interpolate.fitpack, scipy.interpolate._fitpack_impl, scipy.interpolate._fitpack, scipy.interpolate.dfitpack, scipy.interpolate._bsplines, scipy.interpolate._bspl, scipy.interpolate.polyint, scipy.interpolate._ppoly, scipy.interpolate.fitpack2, scipy.interpolate.interpnd, scipy.interpolate.rbf, scipy.interpolate._cubic, scipy.interpolate.ndgriddata, scipy.interpolate._pade, scipy.stats._stats, scipy.special.cython_special, scipy.stats._rvs_sampling, scipy.stats._tukeylambda_stats, scipy.stats._ksstats, scipy.stats._discrete_distns, scipy.stats.mstats_basic, scipy.stats._stats_mstats_common, scipy.stats._hypotests, scipy.stats._wilcoxon_data, scipy.stats.morestats, scipy.stats.statlib, scipy.stats.contingency, scipy.stats._binned_statistic, scipy.stats.kde, scipy.stats.mvn, scipy.stats.mstats, scipy.stats.mstats_extras, scipy.stats._multivariate, quantstats.utils, yfinance, yfinance.ticker, requests, requests.exceptions, requests.__version__, requests.utils, requests.certs, requests._internal_utils, requests.compat, requests.cookies, requests.structures, requests.packages, requests.models, requests.hooks, requests.auth, requests.status_codes, requests.api, requests.sessions, requests.adapters, yfinance.base, yfinance.utils, yfinance.shared, yfinance.tickers, yfinance.multi, multitasking, quantstats.plots, quantstats._plotting, quantstats._plotting.wrappers, numpy.lib.recfunctions, numpy.ma.mrecords, scipy.cluster, scipy.cluster.vq, scipy.cluster._vq, scipy.cluster.hierarchy, scipy.cluster._hierarchy, scipy.cluster._optimal_leaf_ordering, quantstats._plotting.core, quantstats.reports, tabulate
file 31: the profit of 1303296.021209, SR is 3.222049, MDD is -0.078631
file 75: the profit of 818731.025129, SR is 2.600522, MDD is -0.043673

In [25]: 
startDate = '2018-12-06'
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
''' 
    