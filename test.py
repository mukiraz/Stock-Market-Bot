from Connection import BinanceConnection as BC
from Strategy import Strategy as ST
import pandas as pd



Binance = BC("","")

CandleData = Binance.get_candles("btcusdt","5m", 500)

candles = ST(CandleData).MACDS_RSI_EMA_Strategy()


x = Binance.normalize_coin("btcusdt", 0.4411312645145128,"buy")

