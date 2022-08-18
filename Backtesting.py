# -*- coding: utf-8 -*-
"""
Created on Tue Jun 21 09:39:18 2022

@author: Murat Ugur KIRAZ

This module contains Backtesting Classes

"""
import pandas as pd

class Backtesting():   
    
    def __init__(self, symbol, candles, tick_size, comission_rate:float = 0.0, daily_interest_rate:float = 0.0, interval:str = "5m", risk_percentage:float = 0.01, risk_reward_ratio: float = 1.2, start_cash = 1000):
        self.parameters = {
            "total_cash": 0,
            "interval": interval,
            "symbol":symbol,
            "cash":start_cash,
            "risk_percentage":0.01,
            "risk_reward_ratio":1.2,
            "operation_time":"",
            "has_coin":False,
            "has_cash":True,
            "position":"",
            "coin_amount":0,
            "comission_rate":comission_rate,
            "tick_size": tick_size,
            "daily_interest_rate":daily_interest_rate,
            "stop_price":0,
            "sell_price":0,
            "comission":0,
            "comission_fee":0,
            "before_comission_calculated_coin_amount":0,
            "after_comission_calculated_coin_amount":0,
            "buy_price":0
            }
        
        self.candles = candles
        
    def toggle_has(self):
        if self.parameters["has_cash"]:
            self.parameters["has_cash"] = False
            self.parameters["has_coin"] = True
        else:
            self.parameters["has_cash"] = True
            self.parameters["has_coin"] = False
            
    def calculate_risk_amount(self, cash:float, risk_percentage:float):
        return cash * risk_percentage
        
    def calculate_coin_amount(self, position:str, operation :str, symbol:str, buy_price:int, stop_price:int, cash:float, risk_percentage:float):
        risk_amount = self.calculate_risk_amount(cash, risk_percentage)
        
        if position == "Long":        
            delta = buy_price - stop_price        
        if position == "Short":
            delta = stop_price - buy_price
            
        coin_amount = risk_amount / delta
        coin_amount = self.normalize_coin(self.parameters["tick_size"], coin_amount, operation)
        cash_amount_buy_coin = coin_amount * buy_price
        if cash_amount_buy_coin >= cash:
            coin_amount = cash / buy_price
            coin_amount = self.normalize_coin(self.parameters["tick_size"], coin_amount, operation)
        return coin_amount
    
    def calculate_hour_for_interest(self, start_time, end_time):
        start_time =  pd.Timestamp(start_time)
        start_time = start_time - pd.DateOffset(minutes=start_time.minute)
        end_time =  pd.Timestamp(end_time)
        end_time = end_time - pd.DateOffset(minutes=end_time.minute)
        end_time = end_time + pd.DateOffset(minutes = 60)
        time_delta = end_time - start_time
        time_delta = time_delta.seconds//3600
        return time_delta
    
    def calculate_interest_hourly(self, borrowed_money, buy_time, sell_time):
        #https://www.binance.com/en/support/faq/360030157812
        hours = self.calculate_hour_for_interest(buy_time, sell_time)
        return  borrowed_money * (self.parameters["daily_interest_rate"] / 24) * int(hours)
    
    def calculate_sell_price(self, position, buy_price, stop_price, risk_reward_ratio):
        if position == "Long":
            delta = buy_price - stop_price
            return buy_price + delta * risk_reward_ratio
        if position == "Short":
            delta = stop_price - buy_price
            return buy_price - delta * risk_reward_ratio
        
    def calculate_comission(self, coin_amount):
        self.parameters["comission"] = coin_amount * self.parameters["comission_rate"]
        self.parameters["before_comission_calculated_coin_amount"] = coin_amount
        self.parameters["after_comission_calculated_coin_amount"] = coin_amount - self.parameters["comission"]
        self.parameters["coin_amount"] = self.parameters["after_comission_calculated_coin_amount"]
        
    def insert_transaction(self,operation_time,  operation_type, position, coin_amount, price, 
                           comission, comission_fee, after_comission_calculated_coin_amount, 
                           fee, stop_price, sell_price, total_cash, explanation = ""):
        
        data ={
                    "operation_time": operation_time ,
                    "symbol": self.parameters["symbol"], 
                    "operation_type" : operation_type,
                    "position": position,
                    "coin_amount" : coin_amount,
                    "price" : price,
                    "comission": comission,
                    "comission_fee":comission_fee,
                    "after_comission_calculated_coin_amount" : after_comission_calculated_coin_amount,
                    "fee" : fee ,                 
                    "stop_price":stop_price,
                    "sell_price":sell_price,
                    "total_cash": total_cash,
                    "explanation": explanation          
                    }
        return data
    
    def normalize_coin(self, tick_size, amount, operation): 
        operation = operation.lower()
        if float(tick_size)<1:
            for i in range(len(tick_size)):
                if tick_size[i]=="1":
                    precision =(-1,i-1)
                    break
        else:
            for i in range(len(tick_size)):
                if tick_size[i]=="1":
                    precision =(1,i+1)
                    break
        
        if operation == "buy":
            if precision[0]==-1:
                amt_str = "{:0.0{}f}".format(amount, precision[1])
            else:
                amt_str = str(amount)
        elif operation == "sell":
            if precision[0]==-1:
                amount = str(amount)
                dot = amount.index(".") + 1
                amt_str = amount[0:dot+precision[1]]
            else:
                amt_str = str(amount)
        
        return float(amt_str)
    
    def buy_coin(self, decision:str, candles, i):
        if decision == "Long":
            self.parameters["position"] = "Long"
            self.parameters["stop_price"] = candles["atrlower"][i]
        
        elif decision == "Short":
            self.parameters["position"] = "Short"
            self.parameters["stop_price"] = candles["atrupper"][i]
        
        self.parameters["operation"] = "Buy"    
        self.parameters["buy_price"] = candles["Close"][i]    
        self.parameters["coin_amount"] = self.calculate_coin_amount(self.parameters["position"], self.parameters["operation"], self.parameters["symbol"],  self.parameters["buy_price"], self.parameters["stop_price"], self.parameters["cash"], self.parameters["risk_percentage"])    
        self.parameters["sell_price"] = self.calculate_sell_price(self.parameters["position"], self.parameters["buy_price"], self.parameters["stop_price"], self.parameters["risk_reward_ratio"])
        self.parameters["sell_price"] = self.calculate_sell_price(self.parameters["position"], self.parameters["buy_price"], self.parameters["stop_price"], self.parameters["risk_reward_ratio"])
        self.calculate_comission(self.parameters["coin_amount"])
        self.parameters["comission_fee"] = self.parameters["buy_price"] * self.parameters["comission"]    
        fee = self.parameters["before_comission_calculated_coin_amount"] * self.parameters["buy_price"]
        self.parameters["cash"] -= fee        
        self.toggle_has()    
        self.parameters["total_cash"] = self.parameters["cash"] + self.parameters["coin_amount"] * self.parameters["buy_price"]
        self.parameters["operation_time"] = candles["Id"][i+1]
        if decision == "Long":
            print("Long bought",self.parameters["total_cash"])
        elif decision == "Short":
            print("Short bought",self.parameters["total_cash"])
        
        return self.insert_transaction(self.parameters["operation_time"], self.parameters["operation"], self.parameters["position"], 
                                   self.parameters["before_comission_calculated_coin_amount"], self.parameters["buy_price"],
                                   self.parameters["comission"], self.parameters["comission_fee"], self.parameters["after_comission_calculated_coin_amount"],
                                   fee, self.parameters["stop_price"], self.parameters["sell_price"], self.parameters["total_cash"]
                                   )
            
        
    
    def sell_long(self, candles, i):
        self.parameters["operation"] = "Sell"
        self.toggle_has()
        self.calculate_comission(self.parameters["coin_amount"])
        fee = 0.0
        price = 0.0
        if candles["High"][i] >= self.parameters["sell_price"]:
            self.parameters["comission_fee"] = self.parameters["sell_price"] * self.parameters["comission"]
            fee = self.parameters["sell_price"] * self.parameters["coin_amount"]
            price = self.parameters["sell_price"]
            explanation = "Profit!"            
            print("Long sold. Profit!", self.parameters["total_cash"])
        elif candles["Low"][i] <= self.parameters["stop_price"]:
            self.parameters["comission_fee"] = self.parameters["stop_price"] * self.parameters["comission"]
            fee = self.parameters["stop_price"] * self.parameters["coin_amount"]
            price = self.parameters["stop_price"]
            explanation = "Loss!"            
            print("Long sold. Loss!", self.parameters["total_cash"])
            
        self.parameters["cash"] += fee
        self.parameters["total_cash"] = self.parameters["cash"]
    
        
        
        return self.insert_transaction(candles["Id"][i], self.parameters["operation"], self.parameters["position"], 
                                   self.parameters["before_comission_calculated_coin_amount"], price,
                                   self.parameters["comission"], self.parameters["comission_fee"], self.parameters["after_comission_calculated_coin_amount"],
                                   fee, "-", "-",self.parameters["total_cash"], explanation
                                   )
        
    
    def sell_short(self, candles, i):
        self.parameters["operation"] = "Sell"
        self.toggle_has()
        self.calculate_comission(self.parameters["coin_amount"])
        margin_cost = self.calculate_interest_hourly(self.parameters["buy_price"],self.parameters["operation_time"], candles["Id"][i])
        price = 0.0
        explanation = 0.0
        if candles["High"][i] >= self.parameters["stop_price"]:
            self.parameters["comission_fee"] = self.parameters["stop_price"] * self.parameters["comission"]
            net_loss = (self.parameters["stop_price"] - self.parameters["buy_price"]) * self.parameters["coin_amount"] + margin_cost
            self.parameters["total_cash"] -= net_loss
            price = self.parameters["stop_price"]
            explanation = "Loss!"            
            print("Short sold. Loss!", self.parameters["total_cash"])
        elif candles["Low"][i] <= self.parameters["sell_price"]:
            self.parameters["comission_fee"] = self.parameters["sell_price"] * self.parameters["comission"]
            net_profit = (self.parameters["buy_price"] - self.parameters["sell_price"]) * self.parameters["coin_amount"] - margin_cost
            self.parameters["total_cash"] += net_profit
            price = self.parameters["sell_price"]
            explanation = "Profit!"            
            print("Short sold. Profit!", self.parameters["total_cash"])
        
        self.parameters["cash"] = self.parameters["total_cash"]
        fee = self.parameters["sell_price"] * self.parameters["coin_amount"]
        
       
        
        return self.insert_transaction(candles["Id"][i], self.parameters["operation"], self.parameters["position"], 
                       self.parameters["before_comission_calculated_coin_amount"], price,
                       self.parameters["comission"], self.parameters["comission_fee"], self.parameters["after_comission_calculated_coin_amount"],
                       fee, "-", "-", self.parameters["total_cash"], explanation
                       )
        

    
    
class BacktestWithRatio(Backtesting):
    
    def __init__(self, symbol, candles, tick_size, comission_rate:float = 0.0, daily_interest_rate:float = 0.0, interval:str = "5m", risk_percentage:float = 0.01, risk_reward_ratio: float = 1.2, start_cash = 1000):
        self.BT = Backtesting(symbol, candles, tick_size, comission_rate = comission_rate, daily_interest_rate = daily_interest_rate, interval = interval, risk_percentage = risk_percentage, risk_reward_ratio = risk_reward_ratio, start_cash = 1000)
        self.parameters = self.BT.parameters
        self.candles = candles
        
    def backtest(self):      
        
        df_transactions = pd.DataFrame(columns = [
            "operation_time", 
            "symbol", 
            "operation_type", 
            "position",
            "coin_amount", 
            "price", 
            "fee", 
            "comission",
            "comission_fee",
            "after_comission_calculated_coin_amount",
            "total_cash",
            "stop_price",
            "sell_price",
            "explanation"])
        for i in range(len(self.candles)):
            if  self.parameters["has_cash"]:
                if self.candles["Decision"][i] == "Long":
                    data = self.BT.buy_coin(self.candles["Decision"][i], self.candles, i)            
                    df_transactions = df_transactions.append(data, ignore_index = True)
                    continue
                elif self.candles["Decision"][i] == "Short":
                    data = self.BT.buy_coin(self.candles["Decision"][i], self.candles, i)            
                    df_transactions = df_transactions.append(data, ignore_index = True)
                    continue
                else:
                    continue
            if self.parameters["has_coin"]:
                if self.parameters["position"] == "Long":
                    if  self.candles["High"][i] >= self.parameters["sell_price"]:                
                        #profit
                        data = self.BT.sell_long(self.candles, i)                
                        df_transactions = df_transactions.append(data, ignore_index = True) 
                        continue
                    elif self.candles["Low"][i] <= self.parameters["stop_price"]:                
                        #loss
                        data = self.BT.sell_long(self.candles, i)                
                        df_transactions = df_transactions.append(data, ignore_index = True)                        
                        continue
                elif self.parameters["position"] == "Short":
                    if self.candles["High"][i] >= self.parameters["stop_price"]:                
                        #loss
                        data = self.BT.sell_short(self.candles, i)
                        df_transactions = df_transactions.append(data, ignore_index = True)                        
                        continue
                    elif self.candles["Low"][i] <= self.parameters["sell_price"]:                
                        #profit
                        data = self.BT.sell_short(self.candles, i)
                        df_transactions = df_transactions.append(data, ignore_index = True)
                        print("Short sold. Profit!", self.parameters["total_cash"])
                        continue
                    
        return df_transactions
    
class BacktestWithBuySell():
    def __init__(self, symbol, candles, tick_size, comission_rate:float = 0.0, daily_interest_rate:float = 0.0, interval:str = "5m", start_cash = 1000):
        self.parameters = {
            "total_cash": 0,
            "interval": interval,
            "symbol":symbol,
            "cash":start_cash,            
            "operation_time":"",
            "has_coin":False,
            "has_cash":True,
            "position":"",
            "coin_amount":0.0,
            "comission_rate":comission_rate,
            "tick_size": tick_size,
            "daily_interest_rate":daily_interest_rate,            
            "comission":0,
            "comission_fee":0,
            "before_comission_calculated_coin_amount":0,
            "after_comission_calculated_coin_amount":0,
            "buy_price":0
            }
        
        self.candles = candles
    
    def calculate_comission(self, coin_amount):
        self.parameters["comission"] = coin_amount * self.parameters["comission_rate"]
        self.parameters["before_comission_calculated_coin_amount"] = coin_amount
        self.parameters["after_comission_calculated_coin_amount"] = coin_amount - self.parameters["comission"]
        self.parameters["coin_amount"] = self.parameters["after_comission_calculated_coin_amount"]
    
    def normalize_coin(self, tick_size, amount, operation): 
        operation = operation.lower()
        if float(tick_size)<1:
            for i in range(len(tick_size)):
                if tick_size[i]=="1":
                    precision =(-1,i-1)
                    break
        else:
            for i in range(len(tick_size)):
                if tick_size[i]=="1":
                    precision =(1,i+1)
                    break
        
        if operation == "buy":
            if precision[0]==-1:
                amt_str = "{:0.0{}f}".format(amount, precision[1])
            else:
                amt_str = str(amount)
        elif operation == "sell":
            if precision[0]==-1:
                amount = str(amount)
                dot = amount.index(".") + 1
                amt_str = amount[0:dot+precision[1]]
            else:
                amt_str = str(amount)
        
        return float(amt_str)
        
    def calculate_coin_amount(self, operation, coin_price, cash):
        coin_amount = cash / coin_price
        return self.normalize_coin(self.parameters["tick_size"], coin_amount, operation)
    
    def buy_coin(self, decision:str, candles, i):
        if decision == "Long":
            self.parameters["position"] = "Long"
        elif decision == "Short":
            self.parameters["position"] = "Short"
        
        self.parameters["operation"] = "Buy"    
        self.parameters["buy_price"] = candles["Open"][i]
        self.parameters["coin_amount"] = self.calculate_coin_amount(self.parameters["operation"], self.parameters["buy_price"], self.parameters["cash"])
        self.calculate_comission(self.parameters["coin_amount"])
        self.parameters["comission_fee"] = self.parameters["buy_price"] * self.parameters["comission"]
        fee = self.parameters["before_comission_calculated_coin_amount"] * self.parameters["buy_price"]
        self.parameters["cash"] -= fee        
        self.toggle_has()
        self.parameters["total_cash"] = self.parameters["cash"] + self.parameters["coin_amount"] * self.parameters["buy_price"]
        self.parameters["operation_time"] = candles["Id"][i]
        if decision == "Long":
            print("Long bought",self.parameters["total_cash"])
        elif decision == "Short":
            print("Short bought",self.parameters["total_cash"])
        
        return self.insert_transaction(self.parameters["operation_time"], 
                                       self.parameters["operation"], 
                                       self.parameters["position"], 
                                       self.parameters["coin_amount"] ,
                                       self.parameters["buy_price"],
                                       self.parameters["comission"],
                                       self.parameters["comission_fee"],
                                       self.parameters["after_comission_calculated_coin_amount"],
                                       fee,
                                       self.parameters["total_cash"]
                                       )
    
    
    
    def insert_transaction(self,
                           operation_time,  
                           operation_type, 
                           position, 
                           coin_amount, 
                           price, 
                           comission, 
                           comission_fee, 
                           after_comission_calculated_coin_amount, 
                           fee, 
                           total_cash, 
                           explanation = ""):
        
        data ={
                    "symbol": self.parameters["symbol"],
                    "operation_time": operation_time,                     
                    "operation_type" : operation_type,
                    "position": position,
                    "coin_amount" : coin_amount,
                    "price" : price,
                    "comission": comission,
                    "comission_fee":comission_fee,
                    "after_comission_calculated_coin_amount" : after_comission_calculated_coin_amount,
                    "fee" : fee ,                    
                    "total_cash": total_cash,
                    "explanation": explanation          
                    }
        return data
    
    def toggle_has(self):
        if self.parameters["has_cash"]:
            self.parameters["has_cash"] = False
            self.parameters["has_coin"] = True
        else:
            self.parameters["has_cash"] = True
            self.parameters["has_coin"] = False
        
        
    def backtest(self):
        df_transactions = pd.DataFrame(columns = [
            "operation_time", 
            "symbol", 
            "operation_type", 
            "position",
            "coin_amount", 
            "price", 
            "fee", 
            "comission",
            "comission_fee",
            "after_comission_calculated_coin_amount",
            "total_cash",            
            "explanation"])
        for i in range(len(self.candles)):
            if  self.parameters["has_cash"]:
                #buy coin
                if (self.candles["Decision"][i] == "Long") or (self.candles["Decision"][i] == "Short"):
                    data = self.buy_coin(self.candles["Decision"][i], self.candles, i)            
                    df_transactions = df_transactions.append(data, ignore_index = True)                
                else:
                    continue
               
            if self.parameters["has_coin"]:
                #sell coin
                pass
        
        
        
