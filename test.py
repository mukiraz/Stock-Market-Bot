from Connection import BinanceConnection as BC
from Strategy import Strategy as ST



stockMarketBC = BC("","")


BinanceCandles = stockMarketBC.get_candles("btcusdt", "5m", limit = 1000)



cand = ST(BinanceCandles)

x = cand.MACDS_RSI_EMA_Strategy()

