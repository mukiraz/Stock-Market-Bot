# -*- coding: utf-8 -*-
"""
Created on Sat Nov 20 22:56:37 2021

@author: Murat Uğur KİRAZ
"""

from binance.client import Client
from binance.exceptions import BinanceRequestException,BinanceAPIException
from requests.exceptions import ConnectionError
from BinanceBotExceptions import BinanceBotExceptions as BBE
from CandleShaping import CandleShaping as CS
import requests


class BinanceCommunication():
    def __init__(self,api_key,secret_key):
        function_name="init"
        try:
            self.api_key = api_key
            self.secret_key = secret_key
            self.client=Client(api_key, secret_key)
            print("Connected to Binance")
        except BinanceRequestException as e:
            BBE.BinanceRequestExceptionExc(function_name, e.message)
            self.__init__(self.api_key, self.secret_key)
        except BinanceAPIException as e:
            BBE.BinanceAPIExceptionExc(function_name, e.status_code, e.message)
        except ConnectionError:
            BBE.ConnectionErrorException(function_name)
            self.__init__(self.api_key, self.secret_key)

    def createintervals(self):
        self.intervals={
            "1m":self.client.KLINE_INTERVAL_1MINUTE,
            "3m":self.client.KLINE_INTERVAL_3MINUTE,
            "5m":self.client.KLINE_INTERVAL_5MINUTE,
            "15m":self.client.KLINE_INTERVAL_15MINUTE,
            "30m":self.client.KLINE_INTERVAL_30MINUTE,
            "1h":self.client.KLINE_INTERVAL_1HOUR,
            "2h":self.client.KLINE_INTERVAL_2HOUR,
            "4h":self.client.KLINE_INTERVAL_4HOUR,
            "6h":self.client.KLINE_INTERVAL_6HOUR            
            }
        return self.intervals
                        
    def get_system_status(self):
        function_name="get_system_status"
        try:
            response = requests.get("https://api1.binance.com/sapi/v1/system/status").json()
            if response["status"] == 0:
                return True
            else:
                return False
        except ConnectionError:
            BBE.ConnectionErrorException(function_name)
    
    def get_account_api_trading_status(self):
        function_name="get_account_api_trading_status"
        try:
            return self.client.get_account_api_trading_status()
        except BinanceRequestException as e:
            BBE.BinanceRequestExceptionExc(function_name, e.message)
        except BinanceAPIException as e:
            BBE.BinanceAPIExceptionExc(function_name, e.status_code, e.message)
        except ConnectionError:
            BBE.ConnectionErrorException(function_name)
       
    def get_asset_details(self):
        function_name="get_asset_details"
        try:
            return self.client.get_asset_details()
        except BinanceRequestException as e:
            BBE.BinanceRequestExceptionExc(function_name, e.message)
        except BinanceAPIException as e:
            BBE.BinanceAPIExceptionExc(function_name, e.status_code, e.message)
        except ConnectionError:
            BBE.ConnectionErrorException(function_name)
            
            
    def get_my_trades(self,symbol):
        function_name="get_my_trades"
        parameters = {
            "symbol": symbol
            }
        try:
            return self.client.get_my_trades(symbol= symbol)
        except BinanceRequestException as e:
            BBE.BinanceRequestExceptionExc(function_name, e.message, parameters)
        except BinanceAPIException as e:
            BBE.BinanceAPIExceptionExc(function_name, e.status_code, e.message, parameters)
        except ConnectionError:
            BBE.ConnectionErrorException(function_name)
            
    def get_asset_balance(self,asset):
        function_name="get_asset_balance"
        parameters = {
            "asset": asset
            }
        try:
            return self.client.get_asset_balance(asset=asset)            
        except BinanceRequestException as e:
            BBE.BinanceRequestExceptionExc(function_name, e.message, parameters)
        except BinanceAPIException as e:
            BBE.BinanceAPIExceptionExc(function_name, e.status_code, e.message, parameters)
        except ConnectionError:
            BBE.ConnectionErrorException(function_name)
    
    def is_full_connection_ok(self,asset):
        try:
            self.client.get_asset_balance(asset=asset)
            return True
        except BinanceAPIException:
            return False
        
            
    def get_account(self):
         function_name="get_account"
         try:
             return self.client.get_account()       
         except BinanceRequestException as e:
            BBE.BinanceRequestExceptionExc(function_name, e.message)
         except BinanceAPIException as e:
            BBE.BinanceAPIExceptionExc(function_name, e.status_code, e.message)
         except ConnectionError:
            BBE.ConnectionErrorException(function_name)
            
    def get_exchange_info(self):
        function_name="get_exchange_info"
        try:
            return self.client.get_exchange_info()
        except BinanceRequestException as e:
            BBE.BinanceRequestExceptionExc(function_name, e.message)
        except BinanceAPIException as e:
            BBE.BinanceAPIExceptionExc(function_name, e.status_code, e.message)
        except ConnectionError:
            BBE.ConnectionErrorException(function_name)
    
    def get_server_time(self):
        function_name="get_server_time"
        try:
            server_time= self.client.get_server_time()
            return server_time["serverTime"]
        except BinanceRequestException as e:
            BBE.BinanceRequestExceptionExc(function_name, e.message)
        except BinanceAPIException as e:
            BBE.BinanceAPIExceptionExc(function_name, e.status_code, e.message)
        except ConnectionError:
            BBE.ConnectionErrorException(function_name)
            
    def get_candels(self, symbol, interval, insert_open_time_str = False, *defreturn):
        function_name="get_candels"
        parameters = {
            "symbol":symbol,
            "interval":interval
            }
        try:
            intervals = self.createintervals()
            interval = intervals[interval]
            klines = self.client.get_klines(symbol=symbol, interval=interval)
            klines = CS.get_candle_dataframe(klines)
            if insert_open_time_str:
                klines['Open_time_str'] = CS.to_dateTime(klines)
            if len(defreturn)==0:
                return klines
            else:
                return klines.loc[:,defreturn]            
        except BinanceRequestException as e:
            BBE.BinanceRequestExceptionExc(function_name, e.message, parameters)
        except BinanceAPIException as e:
            BBE.BinanceAPIExceptionExc(function_name, e.status_code, e.message, parameters)
        except ConnectionError:
            BBE.ConnectionErrorException(function_name)

    def get_historic_candles(self, symbol, interval, start, end, insert_open_time_str = False, *defreturn):
        function_name="get_historic_candles"
        parameters ={
            "symbol":symbol,
            "interval":interval,
            "start":start,
            "end":end
            }
        try:
            intervals = self.createintervals()
            interval=intervals[interval]
            klines = self.client.get_historical_klines(symbol, interval, start, end)
            klines = CS.get_candle_dataframe(klines)
            if insert_open_time_str:
                klines['Open_time_str'] = CS.to_dateTime(klines)
            if len(defreturn)==0:
                return klines
            else:
                return klines.loc[:,defreturn]
        except BinanceRequestException as e:
            BBE.BinanceRequestExceptionExc(function_name, e.message, parameters)
        except BinanceAPIException as e:
            BBE.BinanceAPIExceptionExc(function_name, e.status_code, e.message, parameters)
        except ConnectionError:
            BBE.ConnectionErrorException(function_name)
            
    def get_recent_trades(self,symbol):
        function_name="get_recent_trades"
        parameters = {
            "symbol":symbol
            }
        try:
            return self.client.get_recent_trades(symbol=symbol)
        except BinanceRequestException as e:
            BBE.BinanceRequestExceptionExc(function_name, e.message, parameters)
        except BinanceAPIException as e:
            BBE.BinanceAPIExceptionExc(function_name, e.status_code, e.message, parameters)
        except ConnectionError:
            BBE.ConnectionErrorException(function_name)
            
    def get_avg_price(self,symbol):
        function_name="get_avg_price"
        parameters = {
            "symbol":symbol
            }
        try:
            return self.client.get_avg_price(symbol=symbol)
        except BinanceRequestException as e:
            BBE.BinanceRequestExceptionExc(function_name, e.message, parameters)
        except BinanceAPIException as e:
            BBE.BinanceAPIExceptionExc(function_name, e.status_code, e.message, parameters)
        except ConnectionError:
            BBE.ConnectionErrorException(function_name)
            
    def order_limit_buy(self,symbol,quantity,price):
        function_name="order_limit_buy"
        parameters ={
            "symbol":symbol,
            "quantity":quantity,
            "price":price
            }
        try:
            return self.client.order_limit_buy(
                symbol = symbol, 
                quantity = quantity, 
                price = str(price))
        except BinanceRequestException as e:
            BBE.BinanceRequestExceptionExc(function_name, e.message, parameters)
        except BinanceAPIException as e:
            BBE.BinanceAPIExceptionExc(function_name, e.status_code, e.message, parameters)
        except ConnectionError:
            BBE.ConnectionErrorException(function_name)

    def order_limit_sell(self,symbol,quantity,price):
       function_name="order_limit_sell"
       parameters ={
            "symbol":symbol,
            "quantity":quantity,
            "price":price
            }
       try:
           return self.client.order_limit_sell(
            symbol=symbol,
            quantity=quantity,
            price=str(price))
       except BinanceRequestException as e:
            BBE.BinanceRequestExceptionExc(function_name, e.message, parameters)
       except BinanceAPIException as e:
            BBE.BinanceAPIExceptionExc(function_name, e.status_code, e.message, parameters)
       except ConnectionError:
            BBE.ConnectionErrorException(function_name)
            
    def order_market_buy(self,symbol,quantity):
        function_name="order_market_buy"
        parameters ={
            "symbol":symbol,
            "quantity":quantity
            }
        try:
            return self.client.order_market_buy(
                    symbol=symbol,
                    quantity=quantity)
        except BinanceRequestException as e:
            BBE.BinanceRequestExceptionExc(function_name, e.message, parameters)
        except BinanceAPIException as e:
            BBE.BinanceAPIExceptionExc(function_name, e.status_code, e.message, parameters)
        except ConnectionError:
            BBE.ConnectionErrorException(function_name)
            
    def order_market_sell(self,symbol,quantity):
        parameters = { "symbol":symbol,
                       "quantity":quantity            
            }
        function_name="order_market_sell"
        try:
            return self.client.order_market_sell(
                    symbol=symbol,
                    quantity=quantity)
        except BinanceRequestException as e:
            BBE.BinanceRequestExceptionExc(function_name, e.message)
        except BinanceAPIException as e:
            BBE.BinanceAPIExceptionExc(function_name, e.status_code, e.message, parameters)
        except ConnectionError:
            BBE.ConnectionErrorException(function_name)
            
    def get_symbol_info(self,symbol):
        function_name="get_symbol_info"
        parameters = {
            "symbol":symbol
            }
        try:
            return self.client.get_symbol_info(symbol)
        except BinanceRequestException as e:
            BBE.BinanceRequestExceptionExc(function_name, e.message, parameters)
        except BinanceAPIException as e:
            BBE.BinanceAPIExceptionExc(function_name, e.status_code, e.message, parameters)
        except ConnectionError:
            BBE.ConnectionErrorException(function_name)
            

    def get_ticker(self):
        function_name="get_ticker"
        try:
            return self.client.get_ticker()
        except BinanceRequestException as e:
            BBE.BinanceRequestExceptionExc(function_name, e.message)
        except BinanceAPIException as e:
            BBE.BinanceAPIExceptionExc(function_name, e.status_code, e.message)
        except ConnectionError:
            BBE.ConnectionErrorException(function_name)
            
    def first_n_markets(self,n,cash_type):
        function_name="first_n_markets"
        parameters = {
            "n":n,
            "cash_type":cash_type
            }
        try:
            tickers=self.get_ticker()
            server_time=self.get_server_time()
            return CS.first_n_markets(n, tickers,cash_type,server_time)
        except BinanceRequestException as e:
            BBE.BinanceRequestExceptionExc(function_name, e.message, parameters)
        except BinanceAPIException as e:
            BBE.BinanceAPIExceptionExc(function_name, e.status_code, e.message, parameters)
        except ConnectionError:
            BBE.ConnectionErrorException(function_name)    
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            

    
    
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
       
        
       
        
       
        
       
        
       
        
       
        