# -*- coding: utf-8 -*-
"""
Created on Sun Jun 12 23:41:55 2022

@author: t.binen
"""

import pandas as pd
import numpy as np
from Indicators import Indicators as Ind
from constant import Source
from Candleshaping import Candleshaping as CS


class Strategy():
    
    def __init__(self, candles):
        self.candles = candles
    
    def crossOver(self, signal1, signal2):
        position = False
        decision = list()
        for i in range(len(signal1)):
            if signal1[i] > signal2[i]:
                if position == False :
                    decision.append("Long")
                    position = True
                else:
                    decision.append(np.nan)
            elif signal1[i] < signal2[i]:
                if position == True:
                    decision.append("Short")
                    position = False
                else:
                    decision.append(np.nan)
            else:
                decision.append(np.nan)
        decisionSignal = {"Decision":decision}
        return pd.DataFrame(decisionSignal)
        
    def MACDS_RSI_EMA_Strategy(self):
        MACD = Ind(self.candles).getMACD()
        atrBands = Ind(self.candles).getATRBands(atrPeriod=3, atrMultiplierUpper = 1.4, srcUpper = Source.CLOSE, atrMultiplierLower = 1.4, srcLower = Source.CLOSE)
        ema = Ind(self.candles).getEMA(length = 200)
        rsi = Ind(self.candles).getRSI(length = 14)
        candles = CS.to_dateTime(self.candles)
        decisionSignal = self.crossOver(MACD["MACD"], MACD["Signal"])
        cand = pd.concat([candles, MACD, atrBands, ema, rsi, decisionSignal], axis=1, join='inner')  
        """
        for i in range(len(cand)):
            if not (cand["Decision"][i] == "Long") and (candles["Close"][i] > ema["EMA"][i]) and (rsi["RSI"][i] > 50):
                print("Decision: {0}, 200EMA: {1} , RSI : {2}, Close: {3} ".format(cand["Decision"][i], cand["EMA"][i], cand["RSI"][i], cand["Close"][i]))
                
            if not (cand["Decision"][i] == "Short") and (candles["Close"][i] < ema["EMA"][i]) and (rsi["RSI"][i] < 50):
                print("Decision: {0}, 200EMA: {1} , RSI : {2}, Close: {3} ".format(cand["Decision"][i], cand["EMA"][i], cand["RSI"][i], cand["Close"][i]))
        """
        return cand
        