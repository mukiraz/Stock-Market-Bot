# -*- coding: utf-8 -*-
"""
Created on Tue Jan 11 21:58:39 2022

@author: mukir
"""

from sklearn.ensemble import RandomForestRegressor
#from xgboost import XGBRegressor
from CandleShaping import CandleShaping as CS


class CoinPredictors:
    
    def prepare_for_learning(self,candles, number_of_rows):
        candles = candles.drop(['Close_time','Ignore.'], axis=1)        
        candles500=CS.add_rsi_macd_bollinger(candles)
        close=candles500.Close        
        if number_of_rows == 500:
            train_rows=candles500.iloc[0:(len(candles500)-1)]
            close_shifted=close.shift(-1).dropna().reset_index(drop=True)
        else:
            train_rows = candles500.iloc[(len(candles500)-1-number_of_rows):(len(candles500)-1)]
            close_shifted = close.shift(-1).dropna().reset_index(drop=True)
            close_shifted = close_shifted.iloc[(len(candles500)-1-number_of_rows):(len(candles500)-1)]
        prediction_row=candles500.iloc[-1:]
        X=train_rows.values
        Y=close_shifted.values
        prediction_row = prediction_row
        return {
              "X":X,
              "Y":Y,
              "prediction_row":prediction_row
            }

    def predictWRandomForest(self , candles , coin_name, number_of_rows = 500):
        train_set = self.prepare_for_learning(candles, number_of_rows)
        rf_reg = RandomForestRegressor(random_state=1,n_jobs=-1)
        rf_reg.fit(train_set["X"],train_set["Y"])
        prediction = rf_reg.predict(train_set["prediction_row"].values)
        prediction = prediction[0]        
        last_price = train_set["prediction_row"].Open.values
        last_price = last_price[0]
        open_time = train_set["prediction_row"].Open_time.values
        open_time = open_time[0]
        print("Estimating ", coin_name, "Last_price: ", last_price, "Prediction: ", prediction, "Estimated Profit: (%)", prediction/last_price)
        return {
                "last_price":last_price,
                "prediction":prediction,
                "open_time":open_time
            }