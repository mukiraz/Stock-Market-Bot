# -*- coding: utf-8 -*-
"""
Created on Sun May 22 17:32:52 2022

@author: Murat Ugur KIRAZ

"""

from Connection import BinanceConnection as BC
#from Indicators import Indicators as Ind
from Strategy import Strategy as ST


HCcandles = BC("","").get_candles("btcusdt","5m", 1200)

#from constant import Source

#source = Ind(HCcandles).source(Source.OHLC4)
#atrBands = Ind(HCcandles).getATRBands(atrPeriod=3, atrMultiplierUpper = 1.4, srcUpper = Source.OHLC4, atrMultiplierLower = 1.4, srcLower = Source.CLOSE)
#macd = Ind(HCcandles).getMACD()

candles = ST(HCcandles).MACDS_RSI_EMA_Strategy()