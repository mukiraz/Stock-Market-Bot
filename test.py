# -*- coding: utf-8 -*-
"""
Created on Sun May 22 17:32:52 2022

@author: Murat Ugur KIRAZ

"""

#from constant import Source

#source = Ind(HCcandles).source(Source.OHLC4)
#atrBands = Ind(HCcandles).getATRBands(atrPeriod=3, atrMultiplierUpper = 1.4, srcUpper = Source.OHLC4, atrMultiplierLower = 1.4, srcLower = Source.CLOSE)
#macd = Ind(HCcandles).getMACD()

from Connection import BinanceConnection as BC
#from Indicators import Indicators as Ind
from Strategy import Strategy as ST
import pandas as pd

start_cash = 1000
parameters = {
    "interval":"5m",
    "coin_name":"btcusdt",
    "cash":start_cash,
    "risk_percentage":0.01,
    "risk_reward_ratio":1.5,
    "has_coin":False,
    "has_cash":True,
    "position":"",
    "coin_amount":0,
    "stop_price":0,
    "sell_price":0,
    "comission":0,
    "before_comission_calculated_coin_amount":0,
    "after_comission_calculated_coin_amount":0
    }

df_transactions = pd.DataFrame(columns = [
    "operation_time", 
    "coin_name", 
    "operation_type", 
    "position",
    "coin_amount", 
    "price", 
    "fee", 
    "comission",
    "after_comission_calculated_coin_amount",
    "total_cash",
    "stop_price",
    "sell_price",
    "explanation"])


Binance = BC("","")

CandleData = Binance.get_candles(parameters["coin_name"],parameters["interval"], 1200)

candles = ST(CandleData).MACDS_RSI_EMA_Strategy()

def toggle_has():
    if parameters["has_cash"]:
        parameters["has_cash"] = False
        parameters["has_coin"] = True
    else:
        parameters["has_cash"] = True
        parameters["has_coin"] = False
        
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

def calculate_sell_price(position, buy_price, stop_price, risk_reward_ratio):
     if position == "Long":
         delta = buy_price - stop_price
         return buy_price + delta * risk_reward_ratio
     if position == "Short":
         pass

def calculate_comission(coin_amount, comission_rate):
    parameters["comission"] = coin_amount * Binance.CONST_COMISSION_RATE
    parameters["before_comission_calculated_coin_amount"] = coin_amount
    parameters["after_comission_calculated_coin_amount"] = coin_amount - parameters["comission"]
    parameters["coin_amount"] = parameters["after_comission_calculated_coin_amount"]
    
def insert_transaction(operation_time,  operation_type, position, coin_amount, price, 
                       comission, after_comission_calculated_coin_amount, 
                       fee, total_cash, stop_price, sell_price, explanation = ""):
    
    data ={
                "operation_time": operation_time ,
                "coin_name": parameters["coin_name"], 
                "operation_type" : operation_type,
                "position": position,
                "coin_amount" : coin_amount,
                "price" : price,
                "comission": comission,
                "after_comission_calculated_coin_amount" : after_comission_calculated_coin_amount,
                "fee" : fee ,                 
                "total_cash": total_cash,
                "stop_price":stop_price,
                "sell_price":sell_price,
                "explanation": explanation          
                }
    return data
    

for i in range(len(candles)):
    if parameters["has_cash"]:
        if candles["Decision"][i] == "Long":
            parameters["position"] = "Long"
            buy_price = candles["Close"][i]
            parameters["stop_price"] = candles["atrlower"][i]
            parameters["coin_amount"] = calculate_coin_amount(parameters["position"], buy_price, parameters["stop_price"], parameters["cash"], parameters["risk_percentage"])
            parameters["sell_price"] = calculate_sell_price(parameters["position"], buy_price, parameters["stop_price"], parameters["risk_reward_ratio"])
            calculate_comission(parameters["coin_amount"], Binance.CONST_COMISSION_RATE)
            #comission = parameters["coin_amount"] * Binance.CONST_COMISSION_RATE
            #comission_calculated = parameters["coin_amount"] - comission
            fee = parameters["before_comission_calculated_coin_amount"] * buy_price
            parameters["cash"] -= fee
            toggle_has()
            total_cash = parameters["cash"] + fee - parameters["comission"] * buy_price
            data = insert_transaction(candles["Id"][i+1], "Buy", parameters["position"], 
                               parameters["before_comission_calculated_coin_amount"], buy_price,
                               parameters["comission"], parameters["after_comission_calculated_coin_amount"],
                               fee, total_cash, parameters["stop_price"], parameters["sell_price"]
                               )
            
            df_transactions = df_transactions.append(data, ignore_index = True)
            continue
        elif candles["Decision"][i] == "Short":
            position = "Short"
            continue
    if parameters["has_coin"]:
        if parameters["position"] == "Long":
            if  candles["High"][i] >= parameters["sell_price"]:
                toggle_has()
                calculate_comission(parameters["coin_amount"], Binance.CONST_COMISSION_RATE)
                fee = parameters["sell_price"] * parameters["coin_amount"]
                parameters["cash"] += fee
                total_cash = parameters["cash"] - parameters["comission"] * parameters["sell_price"]
                data = insert_transaction(candles["Id"][i], "Sell", parameters["position"], 
                               parameters["before_comission_calculated_coin_amount"], parameters["sell_price"],
                               parameters["comission"], parameters["after_comission_calculated_coin_amount"],
                               fee, total_cash, "-", "-", "Profit!"
                               )
                
                df_transactions = df_transactions.append(data, ignore_index = True)
                continue
            elif candles["Low"][i] <= parameters["stop_price"]:
                toggle_has()
                calculate_comission(parameters["coin_amount"], Binance.CONST_COMISSION_RATE)
                fee = parameters["stop_price"] * parameters["coin_amount"]
                parameters["cash"] += fee
                total_cash = parameters["cash"] - parameters["comission"] * parameters["stop_price"]
                data = insert_transaction(candles["Id"][i], "Sell", parameters["position"], 
                               parameters["before_comission_calculated_coin_amount"], parameters["sell_price"],
                               parameters["comission"], parameters["after_comission_calculated_coin_amount"],
                               fee, total_cash, "-", "-", "Loss!"
                               )
                df_transactions = df_transactions.append(data, ignore_index = True)
                continue
        elif parameters["position"] == "Short":
            continue
                
                
                
                
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        