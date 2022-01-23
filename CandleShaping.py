# -*- coding: utf-8 -*-
"""
Created on Fri Dec  3 21:49:49 2021

This class shapes the candles.

@author: mukir
"""

from Indicators import Indicators
import pandas as pd
import numpy as np

class CandleShaping():
    
    # This method converts candles to pandas dataframe.
    def get_candle_dataframe(candles):
        array=np.array(candles)
        candles=pd.DataFrame(array,columns=['Open_time','Open','High','Low','Close','Volume','Close_time','Quote_asset_volume','Number_of_trades','Taker_buy_base_asset_volume','Taker_buy_quote_asset_volume','Ignore.',])
        return candles
    
    # Thşs method inserts indicator values to dataframe.    
    def insert_signal_df(*liste):
        df=pd.concat(liste,axis=1, join='inner')
        return df
    
    # This method converts string values of candle values to float.
    def convert_to_float(candles):
        for i in range(1,len(candles.columns)):            
           candles.iloc[:,i]=candles.iloc[:,i].apply(pd.to_numeric, errors='coerce', downcast="float" )
        return candles
    
    # This method converts open time integer values to day, month, year, hour, minute, seconds format
    def to_dateTime(dataframe):
        return pd.to_datetime(dataframe['Open_time'], unit='ms')
    
    # This method selects the highest counts of the coins.
    def first_n_markets(n,tickers,cash_type,server_time):
        tickers=pd.DataFrame(tickers)        
        open_time = server_time - (1000*60*60*30)
        is_recent=tickers["openTime"]>open_time
        tickers=tickers[is_recent]
        rgx=cash_type+"$"
        tickers=tickers.set_index('symbol').filter(regex=rgx,axis=0)
        tickers=tickers.sort_values(by=["count"],ascending=False)
        tickers=tickers.index
        return np.array(tickers[0:n])
    
    # This method adds rsi, macd and bollinger band values to candle dataframe.
    def add_rsi_macd_bollinger(candles):
        ind = Indicators(candles)
        rsi = ind.calculateRSI()
        bollinger = ind.calculateBollinger()
        macd = ind.calculateMACD()
        candles500 = pd.concat([candles,rsi,macd,bollinger], axis=1, join='inner')
        return candles500.dropna().reset_index(drop=True)
    