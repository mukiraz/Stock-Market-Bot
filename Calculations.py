# -*- coding: utf-8 -*-
"""
Created on Sun Nov  7 11:28:48 2021


@author: Murat Uğur KİRAZ mukiraz@mukiraz.com
"""

import datetime
from math import ceil


class Calculations():
    def __init__(self):
        periods={
                "1m":60000,
                "3m":180000,
                "5m":300000,
                "15m":900000,
                "30m":1800000,
                "1h":3600000,
                "2h":7200000,
                "4h":14400000,
                "6h":21600000,
                }
        self.periods=periods
        
    def wait_time(self,interval,server_time):        
        times = self.calculate_open_close_time(interval,server_time)
        delay=ceil((times["close_time"]-server_time)/1000)
        #print("Function Open time: ",datetime.datetime.fromtimestamp(int(times["open_time"]) / 1000.0),times["open_time"])
        #print("Function Close time: ",datetime.datetime.fromtimestamp(int(times["close_time"]) / 1000.0),times["close_time"])
        #print("Server Open time: ",datetime.datetime.fromtimestamp(int(server_time) / 1000.0),server_time)
        print("Will wait ", delay,"seconds","Close time :",datetime.datetime.fromtimestamp(int(times["close_time"]) / 1000.0))
        next_close_time = times["close_time"] + self.periods[interval]
        return {"next_close_time":next_close_time,
                "delay":delay
                }
    
    def calculate_open_close_time(self,interval,server_time):
        open_time = server_time - (server_time % self.periods[interval])
        close_time = open_time+self.periods[interval]
        return {"open_time": open_time,
                "close_time": close_time
                }
        
    def calculate_comission(cash_type,cash):
        if cash_type=="BNB":
            return cash*0.00075
        else:
            return cash*0.001
    
    def normalize_coin(info, coin, operation):
        step_size=info["filters"][2]["stepSize"]
        if float(step_size)<1:
            for i in range(len(step_size)):
                if step_size[i]=="1":
                    step=(-1,i-1)
        else:
            for i in range(len(step_size)):
                if step_size[i]=="1":
                    step=(1,i+1)
        if operation == "buy":
            if step[0]==-1:
                if step[1]==0:
                    return "{:.0f}".format(coin)
                elif step[1]==1:
                    return "{:.1f}".format(coin)
                elif step[1]==2:
                    return "{:.2f}".format(coin)
                elif step[1]==3:
                    return "{:.3f}".format(coin)
                elif step[1]==4:
                    return "{:.4f}".format(coin)
                elif step[1]==5:
                    return "{:.5f}".format(coin)
                elif step[1]==6:
                    return "{:.6f}".format(coin)
                elif step[1]==7:
                    return "{:.7f}".format(coin)
                elif step[1]==8:
                    return "{:.8f}".format(coin)
                elif step[1]==9:
                    return "{:.9f}".format(coin)
            else:
                return int(coin)
        elif operation == "sell":
            if step[0]==-1:
                coin = str(coin)
                dot = coin.index(".") + 1
                return coin[0:dot+1]
            else:
                return int(coin)
            
    
    def check_input_int_or_float(input):
        try:
            # Convert it into integer
            int(input)
            return True
        except ValueError:
            try:
                # Convert it into float
                float(input)
                return True
            except ValueError:
                return False
            
    def check_input_int(input):
        try:
            # Convert it into integer
            int(input)
            return True
        except ValueError:            
            return False
            
    def calculate_order(order):     
        fills=order["fills"]
        commission=0
        fee=0
        time=str(datetime.datetime.fromtimestamp(int(order["transactTime"]) / 1000.0))
        executedQty=float(order["executedQty"])
        for fill in fills:
            commission+=float(fill["commission"])
            fee+=float(fill["price"])*float(fill["qty"])
        average = fee/executedQty
        return {
            "comission":commission,
            "time":time,
            "executedQty":executedQty,
            "fee":fee,
            "average":average
            }
    
    def date_format(int_format):
        return datetime.datetime.fromtimestamp(int(int_format) / 1000.0)
    
        
        



       