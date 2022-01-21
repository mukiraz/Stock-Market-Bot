# -*- coding: utf-8 -*-
"""
Created on Tue Jan 11 21:07:46 2022

@author: mukir
"""

from BinanceCommunication import BinanceCommunication as BC
from CandleShaping import CandleShaping as CS
import pandas as pd
import numpy as np
#from Calculations import Calculations as Calc
from DatabaseClass import DatabaseClass as DB
from Predicting import CoinPredictors as CP
from sklearn.metrics import mean_squared_error

#Parameters

currency = "AVAXUSDT"
interval = "1m"
start = "01 Jan 2022"
end = "05 Jan 2022"
number_of_rows = [2]
predict = 0
shot = 50
y_actual = []
y_predicted = []
results = dict()





client=BC(DB().get_parameter_by_name("pk"),DB().get_parameter_by_name("sk"))



candles = client.get_historic_candles(currency, interval, start , end)

candles = candles.drop("Open_time_str",axis=1)

candles = CS.convert_to_float(candles)


for j in number_of_rows:
    for i in range(shot):
        df500=candles.iloc[i:500+i].reset_index(drop=True)
        values = CP().predictWRandomForest(df500,currency,j)
        y_actual.append(values["last_price"])
        y_predicted.append(values["prediction"])
        xxx = df500.Close[-1:]
        if (((xxx[499] > values["last_price"]) and (values["prediction"] > values["last_price"])) or ((xxx[499] < values["last_price"]) and (values["prediction"] < values["last_price"]))):
            predict += 1
    rms = mean_squared_error(y_actual, y_predicted, squared=False)
    results[j] = [rms,predict/shot]
    y_actual = []
    y_predicted = []
    predict = 0
    
    


print(results)




