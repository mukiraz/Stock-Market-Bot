# -*- coding: utf-8 -*-
"""
Created on Tue Jun  7 04:14:50 2022

@author: Murat Ugur KIRAZ
"""

import pandas as pd

class Candleshaping():
    """
    This class shapes the candles.
    """
    
    def make_candle_dataframe(self, Id, Open, Close, High, Low, Volume):
        """
        Parameters
        ----------
        Id : TYPE Array
             This is the time data, it is used for Id.
        Open : TYPE Array
             This is the Open value of the candlestick data. 
        Close : TYPE Array
            This is the Close value of the candlestick data. 
        High : TYPE Array
            This is the High value of the candlestick data. 
        Low : TYPE Array
            This is the Low value of the candlestick data. 
        Volume : TYPE Array
            his is the Volume value of the candlestick data.

        Returns
        -------
        TYPE Pandas dataframe.
           This method gets the candlestick data in array and returns a pandas dataframe.

        """
        
        #Here we are creating a dictionary for the DataFrame
        candles = {
            "Id" : Id,
            "Open" : Open,
            "Close" : Close,
            "High" :High,
            "Low" : Low,
            "Volume" : Volume
            }
        #Cconverting dictionary to dataframe
        candles = pd.DataFrame(candles, index=None)
        #Sorting dataframe.
        candles = candles.sort_values(by=['Id'])
        
                
        return self.convert_to_float(candles.reset_index(drop=True))
    
    def convert_to_float(self, candles):
        df = candles.astype({'Open':'float',
                             'Close':'float',
                             'High':'float',
                             'Low':'float',
                             'Volume':'float'})
        return df
    
    def to_dateTime(candles):
        candles.astype({'Id':'int'})
        candles["Id"] = pd.to_datetime(candles['Id'], unit='s')
        return candles