# -*- coding: utf-8 -*-
"""
Created on Tue Nov 23 13:55:33 2021

@author: mukir
"""

from BinanceCommunication import BinanceCommunication as BC
from DatabaseClass import DatabaseClass as DB
from Calculations import Calculations as Calc
from CandleShaping import CandleShaping as CS
from Predicting import CoinPredictors as CP
import pandas as pd
from time import sleep


symbol = "AVAXUSDT"
start = "03 Jan, 2021"
end = "15 Jan, 2021"
interval = "15m"

client=BC(DB().get_parameter_by_name("pk"),DB().get_parameter_by_name("sk"))

candles = client.get_historic_candles(symbol, interval, start, end)

"""
currency = "AVAXUSDT"
start = "03 Jan, 2021"
end = "15 Jan, 2021"
interval = "15m"
number_of_rows = range(2,15)
shot = 100

client=BC(DB().get_parameter_by_name("pk"),DB().get_parameter_by_name("sk"))
candles = client.get_historic_candles(currency, interval, start , end)
candles = candles.drop("Open_time_str",axis=1)
candles = CS.convert_to_float(candles)

for j in number_of_rows:
    for i in range(shot):
        df500=candles.iloc[i:500+i].reset_index(drop=True)
        values = CP().predictWSVM(df500,currency,j)
        break
    break

"""

"""
client=BC(DB().get_parameter_by_name("pk"),DB().get_parameter_by_name("sk"))

markets = client.first_n_markets(20, "USDT")
cash = 20

df = pd.DataFrame(columns=["coin_name","coin_price","coin_amount", "norm_coin_amount_buy", "norm_coin_amount_sell"])




for market in markets:
    print(market)
    avg = float(client.get_avg_price(market)["price"])
    coin_amount = cash/avg
    norm_coin_amount_buy = Calc.normalize_coin(client.get_symbol_info(market), coin_amount, "buy")
    norm_coin_amount_sell = Calc.normalize_coin(client.get_symbol_info(market), coin_amount, "sell")
    df = df.append({'coin_name':market,
                    'coin_price': avg,
                    'coin_amount':coin_amount,
                    'norm_coin_amount_buy':norm_coin_amount_buy,
                    'norm_coin_amount_sell':norm_coin_amount_sell
                    }, ignore_index=True)
    
"""
    




"""
parameters = DB().get_parameters()

coin_name = "BNBUSDT"
coin_name_non = coin_name.replace(parameters["cash_type"], '')
asset_balance = 0.057

coin = Calc.normalize_coin(client.get_symbol_info(coin_name), asset_balance, "buy")





import websocket, json
from BinanceCommunication import BinanceCommunication as BC
from DatabaseClass import DatabaseClass as DB
client=BC(DB().get_parameter_by_name("pk"),DB().get_parameter_by_name("sk"))

symbol = "dogeusdt"

SOCKET = f"wss://stream.binance.com:9443/ws/{symbol}@kline_1m"

def on_open(ws):
    print('opened connection')


def on_close(ws):
    print('closed connection')


def on_message(ws, message):
    json_message = json.loads(message)
    print(json_message["k"]["c"])
    print(client.get_avg_price(symbol = "DOGEUSDT"))
ws = websocket.WebSocketApp(SOCKET, on_open=on_open, on_close=on_close, on_message=on_message)
ws.run_forever()

"""



    














"""


import websocket, json

interval = '1m'

cc = 'BTCUSDT'


socket = f'wss://stream.binance.com:9443/ws/{cc}@kline_{interval}'


def on_message(ws, message):
    print(message)


def on_close(ws, close_status_code, close_msg):
    print("### closed ###")

ws = websocket.WebSocketApp(socket, on_message=on_message, on_close = on_close)


ws.run_forever()









from BinanceCommunication import BinanceCommunication as BC
#from Predicting import CoinPredictors as CP
#import pandas as pd
#import numpy as np
from Calculations import Calculations as Calc
from DatabaseClass import DatabaseClass as DB



client=BC(DB().get_parameter_by_name("pk"),DB().get_parameter_by_name("sk"))

response = client.get_server_time()








from binance.enums import *
from binance.client import Client
from DatabaseClass import DatabaseClass as DB

client = Client(DB().get_parameter_by_name("pk"), DB().get_parameter_by_name("sk"))

client.get_server_time()

"""

    