from Connection import BinanceConnection as BC
from Strategy import Strategy as ST
from BacktestingTest import BacktestWithRatio as BwR

params = {
    "symbol" : "btcusdt",
    "interval": "5m"
    
    }

Binance = BC("","")

print("Getting candlestick data. Please wait...")
CandleData = Binance.get_candles(params["symbol"], params["interval"], 1200)


print("Candlestick data was taken.")

candles = ST(CandleData).MACDS_RSI_EMA_Strategy()

df_transactions= BwR(params["symbol"], candles, Binance.tick_size, Binance.CONST_COMISSION_RATE, Binance.CONST_DAILY_INTEREST_RATE, interval=params["interval"]).backtest()