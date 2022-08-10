from Connection import BinanceConnection as BC
from Strategy import Strategy as ST
from Backtesting import BacktestWithRatio as BTR

params = {
    "symbol" : "btcusdt",
    "interval": "5m"
    
    }

Binance = BC("","")

ts = Binance.get_tick_size("btcusdt")

#CandleData = Binance.get_candles(params["symbol"], params["interval"], 1200)
print("Getting candlestick data. Please wait...")

CandleData = Binance.get_historic_candles(params["symbol"], params["interval"], "20 Jul, 2022")

print("Candlestick data was taken.")

candles = ST(CandleData).MACDS_RSI_EMA_Strategy()


df_transactions = BTR("btcusdt", candles, ts).backtest()






