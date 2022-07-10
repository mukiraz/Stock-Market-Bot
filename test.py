from Connection import BinanceConnection as BC


stockBC = BC('','')

candles = stockBC.get_candles("avaxusdt", "15m", limit = 1200)

print(stockBC.tick_size)
