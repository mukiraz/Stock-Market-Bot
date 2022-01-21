# -*- coding: utf-8 -*-
"""
Created on Tue Jan 11 21:35:35 2022

@author: mukir
"""

from BinanceCommunication import BinanceCommunication as BC
#from Predicting import CoinPredictors as CP
import pandas as pd
import numpy as np
#from Calculations import Calculations as Calc
from DatabaseClass import DatabaseClass as DB

#Parameters

currency = "BTCUSDT"
interval = "3m"
start = "01 Jan 2022"
end = "05 Jan 2022"


client=BC(DB().get_parameter_by_name("pk"),DB().get_parameter_by_name("sk"))



klines = client.get_historic_candles(currency, interval, start , end)

"""
array=np.array(klines)
candles = pd.DataFrame(array,columns=['Open time','Open','High','Low','Close','Volume','Close time','Quote asset volume','Number of trades','Taker buy base asset volume','Taker buy quote asset volume','Ignore.',])
candles = pd.DataFrame(candles)
"""