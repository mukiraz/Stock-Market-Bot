# -*- coding: utf-8 -*-
"""
Created on Sun May 22 17:32:52 2022

@author: Murat Ugur KIRAZ

"""

from Connection import BinanceConnection as BC
#from Indicators import Indicators as Ind
from Strategy import Strategy as ST
import pandas as pd

interval = "5m"
coin_name = "btcusdt"
start_cash = 1000
cash = start_cash
risk_percentage = 0.01
comission_rate = 0.001
risk_reward_ratio = 1.5
has_coin = False
has_cash = True
position = ""
coin_amount = 0


HCcandles = BC("","").get_candles("btcusdt",interval, 1200)

#from constant import Source

#source = Ind(HCcandles).source(Source.OHLC4)
#atrBands = Ind(HCcandles).getATRBands(atrPeriod=3, atrMultiplierUpper = 1.4, srcUpper = Source.OHLC4, atrMultiplierLower = 1.4, srcLower = Source.CLOSE)
#macd = Ind(HCcandles).getMACD()

candles = ST(HCcandles).MACDS_RSI_EMA_Strategy()

#variables


def calculate_risk_amount(cash:float, risk_percentage:float):
    return cash * risk_percentage

def calculate_coin_amount(position:str, buy_price:int, stop_price:int, cash:float, risk_percentage:float):
    if position == "Long":
        risk_amount = calculate_risk_amount(cash, risk_percentage)
        delta = buy_price - stop_price
        coin_amount = risk_amount / delta
        cash_amount_buy_coin = coin_amount * buy_price
        if cash_amount_buy_coin >= cash:
            coin_amount = cash / buy_price
        return coin_amount
    if position == "Short":
        pass

def calculate_sell_price(position:str, risk_reward_ratio:float, cash:float, risk_percentage:float, buy_price:float, coin_amount:float):
     if position == "Long":
         risk_amount = calculate_risk_amount(cash, risk_percentage)
         reward_price = risk_amount * risk_reward_ratio
         sell_price = (reward_price + (coin_amount * buy_price)) / coin_amount
         return sell_price
     if position == "Short":
         pass

df_transactions = pd.DataFrame(columns = [
    "operation_time", 
    "coin_name", 
    "operation_type", 
    "position",
    "coin_amount", 
    "price", 
    "fee", 
    "comission", 
    "comission_calculated",
    "total_cash", 
    "explanation"])

for i in range(len(candles)):
    if has_cash:
        if candles["Decision"][i] == "Long":
            position = "Long"
            buy_price = candles["Close"][i]
            stop_price = candles["atrlower"][i]
            coin_amount = calculate_coin_amount("Long", buy_price, stop_price, cash, risk_percentage)
            sell_price = calculate_sell_price("Long", risk_reward_ratio, cash, risk_percentage, buy_price, coin_amount)
            comission = coin_amount * comission_rate
            comission_calculated = coin_amount - comission
            fee = coin_amount * buy_price
            cash -= fee
            has_cash = False
            has_coin = True
            total_cash = cash + fee - comission * buy_price
            data ={
                "operation_time": candles["Id"][i+1] ,
                "coin_name": coin_name, 
                "operation_type" : "Buy",
                "position": "Long",
                "coin_amount" : coin_amount, 
                "price" : buy_price,
                "comission": comission,
                "comission_calculated" : comission_calculated,
                "fee" : fee ,                 
                "total_cash": total_cash, 
                "explanation": ""
                
                }
            
            df_transactions = df_transactions.append(data, ignore_index = True)
            break
        elif candles["Decision"][i] == "Short":
            position = "Short"
            pass
    if has_coin:
        if position == "Long":
            pass
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        