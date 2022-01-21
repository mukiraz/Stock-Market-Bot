# -*- coding: utf-8 -*-
"""
Created on Tue Nov 23 13:55:33 2021

@author: mukir
"""

from BinanceCommunication import BinanceCommunication as BC
from DatabaseClass import DatabaseClass as DB
from Calculations import Calculations as Calc

client=BC(DB().get_parameter_by_name("pk"),DB().get_parameter_by_name("sk"))

parameters = DB().get_parameters()

coin_name = "ADAUSDT"
coin_name_non = coin_name.replace(parameters["cash_type"], '')
asset_balance = 12.3932

if asset_balance < 12.4:
    coin = Calc.normalize_coin(client.get_symbol_info(coin_name), asset_balance, "sell")



"""

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

    