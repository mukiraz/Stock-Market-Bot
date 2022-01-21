# -*- coding: utf-8 -*-
"""
Created on Fri Dec  3 21:24:57 2021

This python file calculates indicators.

@author: Murat Uğur KİRAZ
"""

import pandas as pd
import numpy as np

class Indicators():
    def __init__(self,candles):
    # In construction, all string expressions are converted to the floats.
        for i in range(1,len(candles.columns)):            
           candles.iloc[:,i]=candles.iloc[:,i].apply(pd.to_numeric, errors='coerce', downcast="float" )
        self.candles=candles
        
    #  This method calculates MACD 
    def calculateMACD(self,column="Close",short=12,long=26,signal_param=9):
        candles=self.candles[column]
        shortEMA=candles.ewm(span=short,adjust=False).mean()
        longEMA=candles.ewm(span=long,adjust=False).mean()
        MACD=shortEMA-longEMA
        macd_array=np.array(MACD)
        df1=pd.DataFrame(macd_array,columns=["MACD"])
        signal=MACD.ewm(span=signal_param,adjust=False).mean()
        signal_array=np.array(signal)
        df2=pd.DataFrame(signal_array,columns=["signal"])
        df=pd.concat([df1, df2], axis=1, join='inner')
        return df
    
    # This method calculates RSI
    def calculateRSI(self,column="Close",period=14):
        candles=self.candles[column]
        candles = candles.apply(pd.to_numeric, errors='coerce', downcast="float" )
        delta = candles.diff()
        up = delta.clip(lower=0)
        down = -1*delta.clip(upper=0)
        ema_up = up.ewm(com=(period-1), adjust=False).mean()
        ema_down = down.ewm(com=(period-1), adjust=False).mean()
        rs = ema_up/ema_down
        rsi_array=list()
        rs=rs.to_numpy()
        for i in rs:
            try:
                rsi_array.append(100-(100/(1+i)))
            except TypeError:
                rsi_array.append(0)

        rsi_array=np.array(rsi_array)
        df=pd.DataFrame(rsi_array,columns=["RSI"])
        
        return df
    # This method calculates Bollinger Bands.
    def calculateBollinger(self,column="Close",lenght=20,st_dev=2):
        candles=self.candles[column]
        sma = np.array(candles.rolling(window=lenght).mean())
        df_sma=pd.DataFrame(sma,columns=["sma"])
        rstd = np.array(candles.rolling(window=lenght).std())
        df_rstd=pd.DataFrame(rstd,columns=["rstd"])
        upper_band = np.array(sma + st_dev * rstd)
        df_upper_band=pd.DataFrame(upper_band,columns=["upper_band"])
        lower_band =  np.array(sma - st_dev * rstd)
        df_lower_band=pd.DataFrame(lower_band,columns=["lower_band"])
        df=pd.concat([df_sma, df_rstd,df_upper_band,df_lower_band], axis=1, join='inner')
        return df