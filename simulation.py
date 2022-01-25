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
from scipy.stats import skew, kurtosis
import time

#Parameters

currency = "BTCUSDT"
intervals = ["1m","3m","5m","15m"]
histories = (["03 Jan, 2021", "15 Jan, 2021"], 
             ["11 Jan, 2021", "23 Jan, 2021"],
             ["20 Jan, 2021", "30 Jan, 2021"],
             ["03 Feb, 2021", "15 Feb, 2021"], 
             ["11 Feb, 2021", "23 Feb, 2021"],
             ["03 Mar, 2021", "15 Mar, 2021"], 
             ["11 Mar, 2021", "23 Mar, 2021"],
             ["20 Mar, 2021", "30 Mar, 2021"],
             ["03 Apr, 2021", "15 Apr, 2021"], 
             ["11 Apr, 2021", "23 Apr, 2021"],
             ["20 Apr, 2021", "30 Apr, 2021"],
             ["03 May, 2021", "15 May, 2021"], 
             ["11 May, 2021", "23 May, 2021"],
             ["20 May, 2021", "30 May, 2021"],
             ["03 Jun, 2021", "15 Jun, 2021"], 
             ["11 Jun, 2021", "23 Jun, 2021"],
             ["20 Jun, 2021", "30 Jun, 2021"],
             ["03 Jul, 2021", "15 Jul, 2021"], 
             ["11 Jul, 2021", "23 Jul, 2021"],
             ["20 Jul, 2021", "30 Jul, 2021"],
             ["03 Sep, 2021", "15 Sep, 2021"], 
             ["11 Sep, 2021", "23 Sep, 2021"],
             ["20 Sep, 2021", "30 Sep, 2021"],
             ["03 Oct, 2021", "15 Oct, 2021"], 
             ["11 Oct, 2021", "23 Oct, 2021"],
             ["20 Oct, 2021", "30 Oct, 2021"],
             ["03 Nov, 2021", "15 Nov, 2021"], 
             ["11 Nov, 2021", "23 Nov, 2021"],
             ["20 Nov, 2021", "30 Nov, 2021"],
             ["03 Dec, 2021", "15 Dec, 2021"], 
             ["11 Dec, 2021", "23 Dec, 2021"],
             ["20 Dec, 2021", "30 Dec, 2021"]             
             )
number_of_rows = range(2,15)
predict = 0
shot = 200
y_actual = np.array([])
y_predicted = np.array([])
y_pred_inc_rate =np.array([])
y_real_inc_rate =np.array([])
results = dict()

df = pd.DataFrame(columns=['interval', 
                           'row_number',
                           'rms', 
                           'pred/shot', 
                           'pred_inc_mean', 
                           'pred_inc_median', 
                           'pred_inc_max', 
                           'pred_inc_min', 
                           'pred_inc_std', 
                           'pred_inc_carp', 
                           'pred_inc_bas', 
                           'real_inc_mean', 
                           'real_inc_median', 
                           'real_inc_max', 
                           'real_inc_min', 
                           'real_inc_std', 
                           'real_inc_carp', 
                           'real_inc_bas', 
                           'mean', 
                           'median',
                           'max',
                           'min',
                           'std',
                           'carp',
                           'bas',
                           'time'])

df2 = pd.DataFrame(columns=[
                           'kline',
                           'interval', 
                           'row_number',
                           'X',
                           'rms', 
                           'pred/shot', 
                           'pred_inc_mean', 
                           'pred_inc_median', 
                           'pred_inc_max', 
                           'pred_inc_min', 
                           'pred_inc_std', 
                           'pred_inc_carp', 
                           'pred_inc_bas', 
                           'real_inc_mean', 
                           'real_inc_median', 
                           'real_inc_max', 
                           'real_inc_min', 
                           'real_inc_std', 
                           'real_inc_carp', 
                           'real_inc_bas', 
                           'mean', 
                           'median',
                           'max',
                           'min',
                           'std',
                           'carp',
                           'bas',
                           'time'])


def current_milli_time():
    return round(time.time() * 1000)



for history in histories:
    start = history[0]
    end = history[1]
    
    for interval in intervals:
        candle_time_begin = current_milli_time()
        client=BC(DB().get_parameter_by_name("pk"),DB().get_parameter_by_name("sk"))
        candles = client.get_historic_candles(currency, interval, start , end)
        candles = CS.convert_to_float(candles)
        candle_time_end = current_milli_time()
        candle_get_time = candle_time_end - candle_time_begin
        for j in number_of_rows:
            for i in range(shot):
                ml_time_begin = current_milli_time()
                df500=candles.iloc[i:500+i].reset_index(drop=True)
                values = CP().predictWSVM(df500,currency,j)
                y_actual = np.append(y_actual, values["last_price"])
                y_predicted = np.append(y_predicted, values["prediction"])
                xxx = df500.Close[-1:]
                if (((xxx[499] > values["last_price"]) and (values["prediction"] > values["last_price"])) or ((xxx[499] < values["last_price"]) and (values["prediction"] < values["last_price"]))):
                    predict += 1
                    if ((xxx[499] > values["last_price"]) and (values["prediction"] > values["last_price"])):
                        y_pred_inc_rate = np.append(y_pred_inc_rate, xxx[499]/values["last_price"])
                        y_real_inc_rate = np.append(y_real_inc_rate, values["prediction"]/values["last_price"])
                ml_time_end = current_milli_time()
            rms = mean_squared_error(y_actual, y_predicted, squared=False)
            results[j] = [rms , predict/shot]
            df = df.append({'interval':interval,
                            'row_number':j,
                            'rms' : rms, 
                            'pred/shot' : predict/shot, 
                            'pred_inc_mean' : y_pred_inc_rate.mean(), 
                            'pred_inc_median' : np.median(y_pred_inc_rate), 
                            'pred_inc_max' : y_pred_inc_rate.max(), 
                            'pred_inc_min' : y_pred_inc_rate.min(), 
                            'pred_inc_std' : y_pred_inc_rate.std(), 
                            'pred_inc_carp' : skew(y_pred_inc_rate), 
                            'pred_inc_bas' : kurtosis(y_pred_inc_rate, fisher = True), 
                            'real_inc_mean' : y_real_inc_rate.mean(), 
                            'real_inc_median' : np.median(y_real_inc_rate), 
                            'real_inc_max' : y_real_inc_rate.max(), 
                            'real_inc_min' : y_real_inc_rate.min(), 
                            'real_inc_std' : y_real_inc_rate.std(), 
                            'real_inc_carp' : skew(y_real_inc_rate), 
                            'real_inc_bas' : kurtosis(y_real_inc_rate, fisher = True),
                            'mean': y_pred_inc_rate.mean() - y_real_inc_rate.mean(),
                            'median': np.median(y_pred_inc_rate) - np.median(y_real_inc_rate),
                            'max' : y_pred_inc_rate.max()- y_real_inc_rate.max(),
                            'min' : y_pred_inc_rate.min()- y_real_inc_rate.min(),
                            'std' : y_pred_inc_rate.std()- y_real_inc_rate.std(),
                            'carp': skew(y_pred_inc_rate) - skew(y_real_inc_rate),
                            'bas': kurtosis(y_pred_inc_rate, fisher = True) - kurtosis(y_real_inc_rate, fisher = True),
                            'time' : ml_time_end-ml_time_begin
                            }, ignore_index=True)
            
            df2 = df2.append({
                            'kline': start,
                            'interval':interval,
                            'row_number':j,
                            'X': str(j) + '_' + start,
                            'rms' : rms, 
                            'pred/shot' : predict/shot, 
                            'pred_inc_mean' : y_pred_inc_rate.mean(), 
                            'pred_inc_median' : np.median(y_pred_inc_rate), 
                            'pred_inc_max' : y_pred_inc_rate.max(), 
                            'pred_inc_min' : y_pred_inc_rate.min(), 
                            'pred_inc_std' : y_pred_inc_rate.std(), 
                            'pred_inc_carp' : skew(y_pred_inc_rate), 
                            'pred_inc_bas' : kurtosis(y_pred_inc_rate, fisher = True), 
                            'real_inc_mean' : y_real_inc_rate.mean(), 
                            'real_inc_median' : np.median(y_real_inc_rate), 
                            'real_inc_max' : y_real_inc_rate.max(), 
                            'real_inc_min' : y_real_inc_rate.min(), 
                            'real_inc_std' : y_real_inc_rate.std(), 
                            'real_inc_carp' : skew(y_real_inc_rate), 
                            'real_inc_bas' : kurtosis(y_real_inc_rate, fisher = True),
                            'mean': y_pred_inc_rate.mean() - y_real_inc_rate.mean(),
                            'median': np.median(y_pred_inc_rate) - np.median(y_real_inc_rate),
                            'max' : y_pred_inc_rate.max()- y_real_inc_rate.max(),
                            'min' : y_pred_inc_rate.min()- y_real_inc_rate.min(),
                            'std' : y_pred_inc_rate.std()- y_real_inc_rate.std(),
                            'carp': skew(y_pred_inc_rate) - skew(y_real_inc_rate),
                            'bas': kurtosis(y_pred_inc_rate, fisher = True) - kurtosis(y_real_inc_rate, fisher = True),
                            'time' : ml_time_end-ml_time_begin
                            }, ignore_index=True)
            y_actual = np.array([])
            y_predicted = np.array([])
            y_pred_inc_rate =np.array([])
            y_real_inc_rate =np.array([])
            predict = 0    
    
    df.to_csv(currency + "_" + start  + "_" + str(shot) + ".csv",index=False, sep=";")
    df.drop(df.index, inplace=True)

df2.to_csv("all"  + currency + "_" + "_" + str(shot) + ".csv",index=False, sep=";")





