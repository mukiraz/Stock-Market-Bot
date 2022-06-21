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
        
    def MACDS_RSI_EMA_Strategy(self, EMAlength:int = 200, RSIlength:int = 14):
        try:
            MACD = Ind(self.candles).getMACD()
            atrBands = Ind(self.candles).getATRBands(atrPeriod=14, atrMultiplierUpper = 1.4, srcUpper = Source.CLOSE, atrMultiplierLower = 1.4, srcLower = Source.CLOSE)
            ema = Ind(self.candles).getEMA(length = EMAlength)
            rsi = Ind(self.candles).getRSI(length = RSIlength)
            candles = CS.to_dateTime(self.candles)
            decisionSignal = self.crossOver(MACD["MACD"], MACD["Signal"])
            cand = pd.concat([candles, MACD, atrBands, ema, rsi, decisionSignal], axis=1, join='inner')  
            
            for i in range(len(cand)):
                """
                if (cand["Decision"][i] == "Long") and (candles["Close"][i] > ema["EMA"][i]) and (rsi["RSI"][i] > 50):
                    cand.at[i, 'Decision'] = "Long"
                elif (cand["Decision"][i] == "Short") and (candles["Close"][i] < ema["EMA"][i]) and (rsi["RSI"][i] < 50):
                    cand.at[i, 'Decision'] = "Short"
                else:                
                    cand.at[i, 'Decision'] = np.nan
                """
                if (cand["Decision"][i] == "Long") and (cand["MACD"][i] < 0):
                    cand.at[i, 'Decision'] = "Long"
                elif (cand["Decision"][i] == "Short") and (cand["MACD"][i] > 0):
                    cand.at[i, 'Decision'] = "Short"
                else:                
                    cand.at[i, 'Decision'] = np.nan
                    
            return cand
        except ValueError:
            print("Your candle stick rows should be more than {}".format(EMAlength))

        