# -*- coding: utf-8 -*-
"""
Created on Tue Jun  7 03:23:18 2022

This python class sends mail to the users.

@author:Murat Ugur KIRAZ

"""

from smtplib import SMTP_SSL as SMTP
from smtplib import SMTPServerDisconnected, SMTPAuthenticationError
from email.mime.text import MIMEText
from DatabaseClass import DatabaseClass as DB

class BinanceBotMailer():
    # This constructor method gets the SMTP parameters from database and login the SMTP mail address.
    def __init__(self):
        # Assigning parameter values from database to parameters veriable. 
        parameters = DB().get_parameters()
        __SMTPserver = parameters["SMTPserver"]
        self.sender = parameters["SMTPusername"]
        
        __USERNAME = parameters["SMTPusername"]
        __PASSWORD = parameters["SMTPpassword"]
        
        #This parameter is used for checking the connection status of SMTP login.
        self.connectionStatus = False
        try:
            self.__conn = SMTP(__SMTPserver)
            self.__conn.set_debuglevel(False)
            self.__conn.login(__USERNAME, __PASSWORD)
            self.connectionStatus = True
        except SMTPServerDisconnected:
            self.connectionStatus = False            
        except SMTPAuthenticationError:
            self.connectionStatus = False
            self.__conn.quit()
    
    # This method sends mail to the user.
    def send_mail(self, destination, subject, message):
        try:
            text_subtype = 'plain'
            
            msg = MIMEText(message, text_subtype)
            msg['Subject']=subject
            msg['From']   = self.sender # some SMTP servers will do this automatically, not all
            
            self.__conn.sendmail(self.sender, destination, msg.as_string())
        except:
            self.__conn.quit()
    
    #This method checks the connection. If login is successfull, it returns true, else false. 
    def check_server_connection(self):
        return self.connectionStatus
        
    #This destructor method is used for to logout from SMTP  mail adress.
    def __del__(self):
        if self.connectionStatus:
            self.__conn.quit()
        