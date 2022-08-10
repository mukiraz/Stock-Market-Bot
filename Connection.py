# -*- coding: utf-8 -*-
"""
Created on Tue Jun  7 03:08:29 2022

This module connects with the crypto stock market,
GET and POST data. 

@author: Murat Ugur KIRAZ
"""

import abc
from binance.client import Client
from binance.exceptions import BinanceRequestException, BinanceAPIException
from requests.exceptions import ConnectionError
from Exceptions import BinanceBotExceptions as BBE
from Candleshaping import Candleshaping as CS

class IConnection(metaclass=abc.ABCMeta):
    """
    This is an interface. 
    This interface contains basic functions of the  connection with the stock market.
    The aim of this interface is creating standart methods for stock markets.
    """
    
    @classmethod
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, 'get_candles') and 
                callable(subclass.load_data_source) and
                NotImplemented)

    @abc.abstractmethod
    def get_candles(self, symbol:str, interval:str, limit:int):
        """
        get_candles method GETs the candlestick data for desired interval time.
        It returns last n candlestick.
        
        """
        raise NotImplementedError
        
        
class BinanceConnection(IConnection):
    """
    This class connects with the Binance crypto stock market.
    
    """
    CONST_COMISSION_RATE = 0.001
    CONST_DAILY_INTEREST_RATE = 0.0001
    CONST_YEARLY_INTEREST_RATE = 0.0365
    
    def __init__(self, api_key, secret_key):
        """
        

        Parameters
        ----------
        api_key : TYPE
            API key of the Binance Stock Market
        secret_key : TYPE
            Secret key of the Binance Stock Market

        Returns
        -------
        None.
        This constructor method takes API and Secret key and creates the client object of Binance.
        """
        function_name = "init"
        try:

            self.api_key = api_key
            self.secret_key = secret_key
            self.client = Client(api_key, secret_key)
            self.tick_size = ''
            self.symbol = ''
            print("Connected to Binance")
        except BinanceRequestException as e:
            BBE.BinanceRequestExceptionExc(function_name, e.message)
            self.__init__(self.api_key, self.secret_key)
        except BinanceAPIException as e:
            BBE.BinanceAPIExceptionExc(function_name, e.status_code, e.message)
        except ConnectionError:
            BBE.ConnectionErrorException(function_name)
            self.__init__(self.api_key, self.secret_key)
            
    def make_candlestick(self, candles):
        """ 
        Parameters
        ----------
        candles : TYPE
            This method takes Binance candlestick data as parameter with the columns below:
            Id,
            Open,
            High,
            Low,
            Close,
            Volume,
            Close_time,
            Quote_asset_volume,
            Number_of_trades,
            Taker_buy_base_asset_volume,
            Taker_buy_quote_asset_volume,
            Ignore.,

        Returns
        -------
        candles : TYPE
           This method returns candlestick data with that columns by converting the string values to float:
              Id,
              Open,
              Close,
              High,
              Low,
              Volume

        """
        import numpy as np
        import pandas as pd
        array = np.array(candles)
        candles = pd.DataFrame(array,columns=['Id','Open','High','Low','Close','Volume','Close_time','Quote_asset_volume','Number_of_trades','Taker_buy_base_asset_volume','Taker_buy_quote_asset_volume','Ignore.',])
        candles = candles.iloc[:, lambda df: [0, 1, 2, 3, 4, 5]]
        candles = candles[['Id','Open','Close','High','Low','Volume']]
        candles = CS().convert_to_float(candles)
        candles["Volume"] = candles["Volume"] * 10000
        candles['Id'] = candles['Id'].str.slice(0, 10)
        candles = candles.astype({'Id':'int'})
        return candles
        
        
        
    def get_candles(self, symbol :str, interval:str, limit:int = 500):
        """
        Parameters
        ----------
        symbol : str
            Symbol as btcusdt, ethusdt, avaxusdt...
        interval : str
            1m, 3m, 5m, 15m, 30m, 2h, 4h, 6h, 8h, 12h, 1d, 3d, 1w, 1M,
        limit : int, optional
            The default is 500.
            This is the row count of candlestick data

        Returns
        -------
        candles : TYPE
            This method returns candlestick data with that columns by converting the string values to float:
              Id,
              Open,
              Close,
              High,
              Low,
              Volume

        """
        function_name = "get_candels"
        parameters = {
            "symbol":symbol,
            "interval":interval
            }
        try:
            
            self.symbol = symbol.upper()        
            self.tick_size = self.get_tick_size(self.symbol)
            candles = self.client.get_klines(symbol = self.symbol, interval = interval, limit = limit) 
            candles = self.make_candlestick(candles)
            return candles
            
        except BinanceRequestException as e:
            BBE.BinanceRequestExceptionExc(function_name, e.message, parameters)
        except BinanceAPIException as e:
            BBE.BinanceAPIExceptionExc(function_name, e.status_code, e.message, parameters)
        except ConnectionError:
            BBE.ConnectionErrorException(function_name)
    
    def get_historic_candles(self, symbol:str, interval:str, start_date:str, end_date:str = None):
        """
        

        Parameters
        ----------
        symbol : str
            Symbol as btcusdt, ethusdt, avaxusdt...
        interval : str
            1m, 3m, 5m, 15m, 30m, 2h, 4h, 6h, 8h, 12h, 1d, 3d, 1w, 1M,
        start_date : str
            Start date as '1 Jan, 2022'
        end_date : str, optional
            The default is None.
            If the argument is not given, method returns the candlestick data from start date to now.
            If end date is given as as '15 Jan, 2022' the method returns the candlestick data from start date to end date.

        Returns
        -------
        candles : TYPE
            his method returns candlestick data with that columns by converting the string values to float:
              Id,
              Open,
              Close,
              High,
              Low,
              Volume

        """
        self.symbol = symbol.upper()        
        self.tick_size = self.get_tick_size(self.symbol)
        if end_date == None:
            candles = self.client.get_historical_klines(self.symbol, interval, start_date)
        else:
            candles = self.client.get_historical_klines(self.symbol, interval, start_date, end_date)
        candles = self.make_candlestick(candles)
        return candles
    
    def get_tick_size(self, symbol:str):
        """
        

        Parameters
        ----------
        symbol : str
            Symbol, btcusdt, avaxusdt, ethusdt...

        Returns
        -------
        tick_size : str
            This method returns the tick size.

        """
        symbol_info = self.client.get_symbol_info(symbol)
        tick_size = symbol_info["filters"][2]["stepSize"]
        return tick_size
            
    def normalize_coin(self, symbol:str, amount:float, operation:str):
        """
        

        Parameters
        ----------
        symbol : str
            Symbol, btcusdt, avaxusdt, ethusdt...
        amount : float
            DESCRIPTION.
        operation : str
            only 'buy' and 'sell'

        Returns
        -------
        TYPE
            When buying or selling coin, stock market needs  the exact coin amount.
            If the calculated amount is 0.000245698745 btc,
            it should be 0.00024.
            This method returns the exact coin amount.
            see https://python-binance.readthedocs.io/en/latest/account.html or
            https://sammchardy.github.io/binance-order-filters/
            for detailed information

        """
        if self.symbol == '':            
            tick_size = self.get_tick_size(self.symbol)
        else:
            tick_size = self.tick_size       
        
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

class HuobiConnection(IConnection):
    """
    This class connects with the Huobi crypto stock market.
    """
    
    CONST_COMISSION_RATE = 0.001
    
    def __init__(self, api_key, secret_key):
        self.__api_key = api_key
        self.__secret_key = secret_key
        
    def get_candles(self, symbol, interval, limit = 500):
        """
        

        Parameters
        ----------
        symbol : TYPE string, The symbol that you get data. 'btcusdt', 'ethusdt'
        interval : TYPE string, Time serie interval. Must be "1m","5m","15m", "30m", "1h" "4h", "1d" or "1w"
        limit : TYPE integer, optional
            DESCRIPTION. The default is 500.

        Returns
        -------
        candles : TYPE pandas dataframe,
            This method gives candlestick data.

        """
        from huobi.client.market import MarketClient
        from huobi.constant.definition import CandlestickInterval as CI
        symbol = symbol.lower()
        interval_values = {
            "1m": CI.MIN1,
            "5m": CI.MIN5,
            "15m": CI.MIN15,
            "30m": CI.MIN30,
            "1h": CI.MIN60,
            "4h" : CI.HOUR4,
            "1d" : CI.DAY1,
            "1w" : CI.WEEK1
             }
        market_client = MarketClient(init_log=True)
        list_obj = market_client.get_candlestick(symbol, interval_values[interval], limit)
        Open = list()
        Close = list()
        Low = list()
        High = list()
        Volume = list()
        Id = list()
        for data in list_obj:
            Id.append(data.id)
            Open.append(data.open)
            Close.append(data.close)
            Low.append(data.low)
            High.append(data.high)
            Volume.append(data.vol)
                
        candles = CS().make_candle_dataframe(Id, Open, Close, High, Low, Volume)
        del(market_client)
        return candles 
    