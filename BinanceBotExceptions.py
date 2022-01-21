# -*- coding: utf-8 -*-
"""
Created on Sat Nov 20 23:02:02 2021

This class logs and mails the exception.
E.(.eqo0lDH&
@author: mukir
"""

from Logging import Logging as Log
from BinanceBotMailer import BinanceBotMailer as BBM
from datetime import datetime
from DatabaseClass import DatabaseClass as DB
import time

class BinanceBotExceptions():
    
    # This method Logs and e-mails to Binance API Exceptions.         
    def BinanceAPIExceptionExc(function_name, code, message, parameters="No parameter"):
        user = DB().get_parameter_by_name("mail")
        current_time = str(datetime.now(tz=None))
        Log(message).logBinanceError(function_name, status_code = code, current_time = current_time)
        mail_message=f"""
        Time          : {current_time},
        Function Name : {function_name},
        Status Code   : {code},
        Message       : {message},
        User          : {user},
        Parameters    : {parameters}
        """
        receivers = ["binance_bot_exceptions@mukiraz.com", user]
        for receiver in receivers:
            BBM().send_mail(receiver,"Binance API Exception", mail_message)
        print("Binance API Exception Occured.","Code:",code, "Message:",message, "Function :",function_name, "Mail sent to user and administrator.")
    
    # This method Logs and e-mails to Binance Request Exceptions.
    def BinanceRequestExceptionExc(function_name, message, parameters="No parameter"):
        user = DB().get_parameter_by_name("mail")
        current_time = str(datetime.now(tz=None))
        Log(message).logBinanceError(function_name, current_time = current_time)
        mail_message=f"""
        Time          : {current_time},
        Function Name : {function_name},
        Message       : {message},
        User          : {user},
        Parameters    : {parameters}
        """
        receivers = ["binance_bot_exceptions@mukiraz.com", user]
        for receiver in receivers:
            BBM().send_mail(receiver,"Binance API Exception", mail_message)
        print("Binance Request Exception Occured.", "Message:",message, "Function :",function_name, "Mail sent to user and administrator.")
        
    # This method Logs Connection Exception.  
    def ConnectionErrorException(function_name, time_period=10, user=""):
        current_time = str(datetime.now(tz=None))
        message="No internet connection " + "Will try",str(time_period) + "seconds later."
        print(message)
        Log(message).logBinanceError(function_name, current_time = current_time)        
        time.sleep(time_period)