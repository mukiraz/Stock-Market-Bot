from Connection import BinanceConnection as BC
from Strategy import Strategy as ST
from Backtesting import BacktestWithBuySell as BTBS

params = {
    "symbol" : "btcusdt",
    "interval": "5m"
    
    }

Binance = BC("","")

ts = Binance.get_tick_size(params["symbol"])

CandleData = Binance.get_candles(params["symbol"], params["interval"], 1200)
print("Getting candlestick data. Please wait...")

#CandleData = Binance.get_historic_candles(params["symbol"], params["interval"], "20 Jul, 2022")

print("Candlestick data was taken.")

candles = ST(CandleData).Bollinger_Bands_Strategy()


df_transactions = BTBS(params["symbol"], candles, ts, comission_rate = Binance.CONST_COMISSION_RATE, daily_interest_rate = Binance.CONST_DAILY_INTEREST_RATE).backtest()






