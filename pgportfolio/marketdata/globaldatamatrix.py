from __future__ import division
from __future__ import absolute_import
from __future__ import print_function

from pymongo import MongoClient
client = MongoClient('localhost', 27017)

from pgportfolio.marketdata.coinlist import CoinList
import numpy as np
import pandas as pd
from pgportfolio.tools.data import panel_fillna
from pgportfolio.constants import *
from datetime import datetime
import logging
import pdb

class HistoryManager:
    # if offline ,the coin_list could be None
    # NOTE: return of the sqlite results is a list of tuples, each tuple is a row
    def __init__(self, dbName, stockList):
        self._dbName = dbName
        self.stockList = stockList        

    def get_global_data_matrix_from_mongodb(self, start, end, features):
        db = client[self._dbName]
        dateSet = set()
        for stockName in self.stockList:
            df = pd.DataFrame(list(db[stockName].find().sort('date')))
            df = df.set_index('date')
            dateSet = dateSet.union(list(df.index))
        dateSet = sorted(list(dateSet))
  
        panel = pd.Panel(items=features, major_axis=self.stockList, minor_axis=dateSet, dtype=np.float32)
        for row_number, stockName in enumerate(self.stockList):
            df = pd.DataFrame(list(db[stockName].find().sort('date')))[features+['date']]
            df = df.set_index('date')
            for feature in features:
                panel.loc[feature, stockName, df.index] = df[feature].squeeze()
                panel = panel_fillna(panel, 'both')
        return panel, dateSet


    

