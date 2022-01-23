# -*- coding: utf-8 -*-
"""
Created on Sat Jan 15 23:26:58 2022

@author: mukir
"""

from BinanceCommunication import BinanceCommunication as BC
from DatabaseClass import DatabaseClass as DB
from Calculations import Calculations as Calc
from Predicting import CoinPredictors as CP
from Logging import Logging
from time import sleep

class Bot:
    def __init__(self):
        _pk = DB().get_parameter_by_name("pk")
        _sk = DB().get_parameter_by_name("sk")
        self.client = BC(_pk, _sk)
        self.coin = ""
        self.next_close_time = ""
        self.best_price_offer={}
        self.predictions={}
        self.last_prices={}
        self.average_bought = 0
        self.coin_name = ""
        
    def is_connection_ok(self):
        return self.client.is_full_connection_ok(asset="USDT")
    
    def get_asset_balance(self,asset):
        return self.client.get_asset_balance(asset=asset)
    
    def start_bot(self):
        parameters = DB().get_parameters()
        self.next_close_time = Calc().calculate_open_close_time(DB().get_parameter_by_name("interval"),self.client.get_server_time())["close_time"]
        coin_name=""
        DB().update_data("parameters", ["has_cash","has_coin"], [1,0])
        assets=self.client.get_asset_balance(asset=parameters["cash_type"])
        total_cash_start = float(assets["free"])
        cash_limit = total_cash_start - (parameters["cash_start"] - parameters["cash_limit"])
        while True:
                parameters = DB().get_parameters()
                assets=self.client.get_asset_balance(asset=parameters["cash_type"])
                total_cash=assets["free"]
                if parameters["has_cash"]==1:
                    if total_cash_start < cash_limit:
                        print("Because of the loss, the system stopped.")
                        break                    
                    coin_name = self.decide_best_coin(parameters)
                    if self.best_price_offer[coin_name] > 1:
                        self.coin = parameters["cash"] / self.last_prices[coin_name]
                        self.coin = Calc.normalize_coin(self.client.get_symbol_info(coin_name), self.coin, "buy")
                        print("Average price from binance", self.client.get_avg_price(symbol = coin_name)["price"])
                        self.average_bought = self.buy_coin(coin_name, parameters, self.last_prices, self.predictions,self.best_price_offer, total_cash)
                        self.sell_coin_exceeds_stop_loss(coin_name, parameters, self.last_prices[coin_name], self.best_price_offer[coin_name])
                        continue
                    else:
                        print("There is no coin to buy!")
                        self.wait_next_interval(parameters)
                        
                        continue
                if parameters["has_coin"]==1:
                    klines = self.get_correct_candles(coin_name, parameters, self.next_close_time)
                    values = CP().predictWSVM(klines,coin_name,number_of_rows = 2)
                    avg_price=self.client.get_avg_price(symbol=coin_name)
                    avg_price = float(avg_price["price"])
                    last_price=values["last_price"]
                    prediction=values["prediction"]
                    if prediction>last_price:
                        assets = self.client.get_asset_balance(asset=parameters["cash_type"])
                        total_cash = float(assets["free"])+parameters["coin"]*avg_price
                        print("total_cash:",total_cash)
                        Logging("total_cash: " + str(total_cash)).logEvent()
                        self.sell_coin_exceeds_stop_loss(coin_name, parameters, last_price, prediction)
                        continue
                    else:
                        self.sell_coin(coin_name, parameters, last_price, prediction)
                        self.wait_next_interval(parameters)
                        continue
    
    # This method sells coin
    def sell_coin(self, coin_name, parameters, last_price, prediction, explanation = "Bot Decided"):
        
        coin_name_non = coin_name.replace(parameters["cash_type"], '')
        asset_balance = float(self.client.get_asset_balance(coin_name_non)["free"])
        if asset_balance < float(self.coin):
            self.coin = Calc.normalize_coin(self.client.get_symbol_info(coin_name), asset_balance, "sell")
        order=self.client.order_market_sell(symbol=coin_name, quantity= self.coin)
        calculated_order=Calc.calculate_order(order)
        cash_sold=calculated_order["fee"]
        comission=calculated_order["comission"]
        cash_sold=cash_sold-comission
        cash=parameters["cash_start"]
        DB().update_data("parameters", ["cash"], [cash])
        assets=self.client.get_asset_balance(asset=parameters["cash_type"])
        total_cash=assets["free"]
        print("Coin sold:",coin_name)
        print("Coin price: ",calculated_order["average"])
        print("Fee :", calculated_order["fee"])
        print("Quantity :", calculated_order["executedQty"])
        print("Comission :", calculated_order["comission"]) 
        print("Total cash:",total_cash)
        Logging("coin sold, cash: "+str(cash_sold)).logEvent()
        Logging("total_cash: "+str(total_cash)).logEvent()
        self.coin=0
        DB().update_data("parameters", ["coin", "has_cash", "has_coin"], [self.coin,1,0])
        DB().insert_data("transactions",
                         (coin_name,
                          calculated_order["time"], 
                          order["side"],
                          float(last_price),
                          prediction, 
                          float(prediction)/float(last_price), 
                          calculated_order["average"], 
                          calculated_order["executedQty"],
                          calculated_order["fee"],
                          calculated_order["comission"],
                          total_cash,
                          explanation))
        
    
    def buy_coin(self,coin_name,parameters, last_prices, predictions,best_price_offer, total_cash):
        order = self.client.order_market_buy(symbol=coin_name, quantity=self.coin)
        calculated_order=Calc.calculate_order(order)
        quantity = calculated_order["executedQty"] * 0.999
        DB().update_data("parameters", ["coin"], [quantity])
        print("coin bought:",coin_name)
        print("coin price: ",calculated_order["average"])
        print("Fee :", calculated_order["fee"])
        print("Quantity :", calculated_order["executedQty"])
        print("Comission :", calculated_order["comission"]) 
        print("Total cash:",total_cash)
        Logging("coin bought: "+str(self.coin)).logEvent()
        Logging("total_cash: " + str(total_cash)).logEvent()
        cash=0
        DB().update_data("parameters", ["cash", "has_cash", "has_coin"], [cash, 0, 1])
        DB().insert_data("transactions",
                         (coin_name,
                          calculated_order["time"],
                          order["side"],
                          float(last_prices[coin_name]),
                          predictions[coin_name], 
                          best_price_offer[coin_name], 
                          calculated_order["average"],
                          calculated_order["executedQty"],
                          calculated_order["fee"],
                          calculated_order["comission"],
                          total_cash,
                          "Bot Decided"))
        return calculated_order["average"]
    
    def sell_coin_exceeds_stop_loss(self,coin_name, parameters, last_price, prediction):
        stop_price = self.average_bought * (1 + parameters["stop_loss_limit"])
        profit_price = self.average_bought * (1 + parameters["profit_limit"])
        while int(self.next_close_time) > self.client.get_server_time():
            average =float(self.client.get_avg_price(symbol = coin_name)["price"])
            if average < stop_price:
                print("Because of the stop loss coin will be sold. Average: ",average, "Stop price: ", stop_price, "Profit Price", profit_price, "coin: ", self.coin)
                self.sell_coin(coin_name, parameters, last_price, prediction, explanation = "Stop loss." )
                wait_parameters = Calc().wait_time(parameters["interval"],self.client.get_server_time())
                self.next_close_time = wait_parameters["next_close_time"]
                sleep(wait_parameters["delay"])
                break
            elif average >= profit_price:
                print("Because of average of the coin price exceeds profit limit coin will be sold. Average: ",average, "Stop price: ", stop_price, "Profit Price", profit_price, "coin: ", self.coin)
                self.sell_coin(coin_name, parameters, last_price, prediction, explanation = "Profit loss." )
                wait_parameters = Calc().wait_time(parameters["interval"],self.client.get_server_time())
                self.next_close_time = wait_parameters["next_close_time"]
                sleep(wait_parameters["delay"])
                break                
            else:
                print("Average is higer than stop price! Continue... Average: ",average, "Stop price: ", stop_price, "Profit Price", profit_price, "coin: ", self.coin)
            sleep(1)
        wait_parameters = Calc().wait_time(parameters["interval"],(self.client.get_server_time()-2500))
        self.next_close_time = wait_parameters["next_close_time"]
        
    def get_correct_candles(self, coin_name, parameters, next_close_time):
        klines =""
        while True:
            klines = self.client.get_candels(coin_name, parameters["interval"])
            if int(next_close_time) != (int(klines.iloc[-1].Close_time)+1):
                print("loop")
                sleep(0.1)
            else:
                break
        return klines
    
    def decide_best_coin(self, parameters):
        first_coins=self.client.first_n_markets(parameters["number_of_coin"], parameters["cash_type"])
        self.best_price_offer.clear()
        self.last_prices.clear()
        for first_coin in first_coins:
            klines = self.get_correct_candles(first_coin, parameters, self.next_close_time)                    
            values = CP().predictWSVM(klines,first_coin,number_of_rows = 2)
            self.best_price_offer[first_coin]=(values["prediction"]/values["last_price"])
            self.last_prices[first_coin]=values["last_price"]
            self.predictions[first_coin]=values["prediction"]       
        coin_name=max(self.best_price_offer, key = self.best_price_offer.get)
        print("Decided coin: ", coin_name, self.best_price_offer[coin_name])
        return coin_name
    
    def wait_next_interval(self, parameters):
        wait_parameters = Calc().wait_time(parameters["interval"],self.client.get_server_time())
        self.next_close_time = wait_parameters["next_close_time"]
        sleep(wait_parameters["delay"])
        
        
        
                        
        