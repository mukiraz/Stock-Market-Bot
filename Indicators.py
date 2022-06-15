# -*- coding: utf-8 -*-
"""
Created on Sun May 29 19:16:44 2022

@author: Murat Ugur KIRAZ
"""
import pandas as pd
import pandas_ta as ta
from constant import Source

class Indicators():
    """
    The indicators are calculated by pandas_ta library. The documentation is below:
    
    https://github.com/twopirllc/pandas-ta
    
    In this class, the undefined indicators in pandas_ta are defined.
    
    """
    
    def __init__(self, candles):
        self.candles = candles
        
    def source(self, source:Source):
        """
        This method is used for source parameter of an indicator.

        Parameters
        ----------
        source : Source class from constant module
                OPEN, CLOSE, LOW, HIGH, HL2, HLC3, OHLC4, HLCC4
                HL2 = (High + Low) / 2
                HLC3 = (High + Low + Close) / 3
                OHLC4 = (Open + High + Low + Close) / 4
                HLCC4 = (High + Low + Close + Close) / 4
        Returns
        -------
        TYPE Series object of pandas.core.series
            It returns a pandas series with one column.

        """
        source = source.lower()
        if source == "close":
            return self.candles.Close
        elif source == "open":
            return self.candles.Open
        elif source == "high":
            return self.candles.High
        elif source == "low":
            return self.candles.Low
        elif source == "hl2":
            self.candles = (self.candles.High + self.candles.Low ) / 2
            return pd.Series(self.candles['hl2'])
        elif source == "hlc3":
            self.candles['hlc3'] = ( self.candles.High + self.candles.Close + self.candles.Low ) / 3 
            return pd.Series(self.candles['hlc3'])
        elif source == "ohlc4":
            self.candles['ohlc4'] = ( self.candles.Open + self.candles.High + self.candles.Close + self.candles.Low ) / 4
            return pd.Series(self.candles['ohlc4'])
        elif source == "hlcc4":
            self.candles['hlcc4'] = ( self.candles.Open + self.candles.High + self.candles.Close + self.candles.Low ) / 4
            return pd.Series(self.candles['hlcc4'])

    
    def insert_signal_to_df(self,*kwargs):
        """        

        Parameters
        ----------
        *kwargs : TYPE list
            DESCRIPTION
            List of the signals and candles 
            USAGE [candles,rsi,macd,bollinger]

        Returns
        -------
        df : TYPE pandas dataframe
            DESCRIPTION
            Returns the added signals.

        """
        return pd.concat(kwargs, axis=1, join='inner')
    
    def getATR(self, period):
        return self.candles.ta.atr(period)
    
    def getATRBands(self, atrPeriod : int =3, atrMultiplierUpper : float = 2.5, srcUpper : Source = Source.CLOSE, atrMultiplierLower : float = 2.5, srcLower : Source = Source.CLOSE):
        """
        

        Parameters
        ----------
        atrPeriod : int, optional
            DESCRIPTION. The default is 3.
        atrMultiplierUpper : float, optional
            DESCRIPTION. The default is 2.5.
        srcUpper : Source, optional
            DESCRIPTION. The default is Source.CLOSE.
        atrMultiplierLower : float, optional
            DESCRIPTION. The default is 2.5.
        srcLower : Source, optional
            DESCRIPTION. The default is Source.CLOSE.

        Returns
        -------
        df : TYPE
            DESCRIPTION.

        """
        atr = self.candles.ta.atr(atrPeriod)
        atrupper = self.source(srcUpper) + atr * atrMultiplierUpper
        atrlower = self.source(srcLower) - atr * atrMultiplierLower
        atrBands = {'atrupper':atrupper,
                    'atrlower':atrlower}
        df = pd.DataFrame(atrBands, index=None)
        return df
    
    def getMACD(self,  slow: int = 26, fast: int = 12, signal: int = 9, fillna: bool = False):
        signals = self.candles.ta.macd(slow, fast, signal, fillna)
        signals.columns.values[0] = "MACD"
        signals.columns.values[1] = "Histogram"
        signals.columns.values[2] = "Signal"
        return signals
    
    def getEMA(self, length: int = 14,  source : Source = Source.CLOSE):
        ema = self.candles.ta.ema(length = length)
        arr = ema.to_numpy() 
        return pd.DataFrame(arr, columns=["EMA"])

    
    def getRSI(self, length = 14):
        rsi = self.candles.ta.rsi(length = length)
        arr = rsi.to_numpy() 
        return pd.DataFrame(arr, columns=["RSI"])
    
    
    

