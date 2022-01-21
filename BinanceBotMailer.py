# -*- coding: utf-8 -*-
"""
Created on Sat Nov 20 23:58:27 2021

This python class sends mail to the users.

@author:Murat Ugur KIRAZ

"""

from smtplib import SMTP_SSL as SMTP
from smtplib import SMTPServerDisconnected, SMTPAuthenticationError
from email.mime.text import MIMEText
from DatabaseClass import DatabaseClass as DB

class BinanceBotMailer():
    def __init__(self):
        parameters = DB().get_parameters()
        __SMTPserver = parameters["SMTPserver"]
        self.sender = parameters["SMTPusername"]
        
        __USERNAME = parameters["SMTPusername"]
        __PASSWORD = parameters["SMTPpassword"]
        
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
        
    def send_mail(self, destination, subject, message):
        try:
            text_subtype = 'plain'
            
            msg = MIMEText(message, text_subtype)
            msg['Subject']=       subject
            msg['From']   = self.sender # some SMTP servers will do this automatically, not all
            
            self.__conn.sendmail(self.sender, destination, msg.as_string())
        except:
            self.__conn.quit()
            
    def check_server_connection(self):
        return self.connectionStatus
        
    
    def __del__(self):
        if self.connectionStatus:
            self.__conn.quit()
        