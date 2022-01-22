# -*- coding: utf-8 -*-
"""
Created on Sat Jan 15 17:38:52 2022

@author: mukir
"""

from pyfiglet import Figlet
from termcolor import colored
from DatabaseClass import DatabaseClass as DB
from Bot import Bot
from Calculations import Calculations as Calc
from BinanceBotMailer import BinanceBotMailer as BBM
import re
import shutil
from requests import get

class Controller:
    
    @staticmethod
    def do_00():
        """0.  Print Menu"""
        Controller.generate_menu()

    @staticmethod
    def do_01():
        """1.  Terms and Conditions"""
        Controller.get_terms_conditions()
    
    @staticmethod   
    def do_02():
        """2.  Set Mail Address"""
        Controller.set_database_value("mail","Mail Address")

    @staticmethod
    def do_03():
        """3.  Set Binance API Key"""
        Controller.set_database_value("pk","API Key")

    @staticmethod
    def do_04():
        """4.  Set Binance Secret Key"""
        Controller.set_database_value("sk","Secret Key")

    @staticmethod
    def do_05():
        """5.  Check Binance Connection Status"""
        Controller.is_client_status_ok()

    @staticmethod
    def do_06():
        """6.  Set Interval Time"""
        Controller.set_database_value("interval","Interval")
        
    @staticmethod
    def do_07():
        """7.  Set Cash Type"""
        Controller.set_database_value("cash_type","Cash Type")
        
    @staticmethod
    def do_08():
        """8.  Set Cash Amount"""
        Controller.set_database_value("cash","Cash")
    
    @staticmethod
    def do_09():
        """9.  Set Cash Limit"""
        Controller.set_database_value("cash_limit","Cash Limit")
    
    @staticmethod
    def do_10():
        """10. Set Stop Loss Limit"""
        Controller.set_database_value("stop_loss_limit","Stop Loss Limit")    
            
    @staticmethod
    def do_11():
        """11. Set Number of Coin Will Be Predicted"""
        Controller.set_database_value("number_of_coin","Number of Coin")

    
    @staticmethod
    def do_12():
        """12. Set SMTP Server Name"""
        Controller.set_database_value("SMTPserver","SMTP Server Name")
        
    @staticmethod
    def do_13():
        """13. Set SMTP User Name"""
        Controller.set_database_value("SMTPusername","SMTP User Name")
        
    @staticmethod
    def do_14():
        """14. Set SMTP Password"""
        Controller.set_database_value("SMTPpassword","SMTP Password")
    
    @staticmethod
    def do_15():
        """15. Check SMTP Connection"""
        Controller.is_SMTP_mail_connection_ok()
    
    @staticmethod
    def do_16():
        """16. Reset Settings"""
        confirm = input("Your all parameters will be reset. Do yo want to proceed? Y/N \n")
        if confirm.upper() == "Y":
            DB().reset_parameters()
            shutil.rmtree('logs')
            print("All parameters erased.")
            

        
    @staticmethod
    def do_17():
        """17. Start Bot"""
        parameters=DB().get_parameters()
        binance_connection_status = Bot().is_connection_ok()
        smtp_connection_status = BBM().check_server_connection()
        if not parameters["mail"]:
            print(colored("Set Mail Address from menu 2\n", 'red'))
            Controller.set_database_value("mail","Mail Address")
        elif not parameters["pk"]:
            print(colored("Set Binance API Key from menu 3\n", 'red'))
            Controller.set_database_value("pk","API Key")
        elif not parameters["sk"]:
            print(colored("Set Binance Secret Key from menu 4\n", 'red'))
            Controller.set_database_value("sk","Secret Key")
        elif not binance_connection_status:
            print(colored("Check your binance communication from menu 5\n", 'red'))
            Controller.is_client_status_ok()
        elif not parameters["interval"]:
            print(colored("Set Interval from menu 6\n", 'red'))
            Controller.set_database_value("interval","Interval")
        elif not parameters["cash_type"]:
            print(colored("Set Cash Type from menu 7\n", 'red'))
            Controller.set_database_value("cash_type","Cash Type")
        elif not parameters["cash"]:
            print(colored("Set Cash Amount from menu 8\n", 'red'))
            Controller.set_database_value("cash","Cash")
        elif not parameters["cash_limit"]:
            print(colored("Set Cash Limit from menu 9\n", 'red'))
            Controller.set_database_value("cash_limit","Cash Limit")
        elif not parameters["stop_loss_limit"]:
            print(colored("Set Stop Loss Limit from menu 10\n", 'red'))
            Controller.set_database_value("stop_loss_limit","Stop Loss Limit")
        elif not parameters["number_of_coin"]:
            print(colored("Set Number of Coins from menu 11\n", 'red'))
            Controller.set_database_value("number_of_coin","Number of Coins")
        elif not parameters["SMTPserver"]:
            print(colored("Set SMTP Server Name from menu 12\n", 'red'))
            Controller.set_database_value("SMTPserver","SMTP Server Name")
        elif not parameters["SMTPusername"]:
            print(colored("Set SMTP User Name from menu 13\n", 'red'))
            Controller.set_database_value("SMTPusername","SMTP User Name")
        elif not parameters["SMTPpassword"]:
            print(colored("Set SMTP Password from menu 14\n", 'red'))
            Controller.set_database_value("SMTPpassword","SMTP Password")
        elif not smtp_connection_status:
            print(colored("Check your SMTP Mail communication from menu 15\n", 'red'))
            Controller.is_SMTP_mail_connection_ok()
        else:
            print("You are about to start the bot with parameters below:")
            print("Interval:",parameters["mail"])
            print("Interval:",parameters["interval"])
            print("Cash Type:",parameters["cash_type"])
            print("Cash:",parameters["cash"])
            print("Cash Limit:",parameters["cash_limit"])
            print("Stop Loss Ratio:",parameters["stop_loss_limit"])
            print("Number of Coins:",parameters["number_of_coin"])
            agreement=input("By typing 'Y' and pressing enter, you will admit the terms and conditions.\nWill you start the bot? Y/N\n")
            if agreement.upper() == "Y":
                Bot().start_bot()


            
    @staticmethod
    def do_18():
        """18. Quit."""
        print("Exiting...")


    @staticmethod
    def execute(user_input):
        controller_name = f"do_{user_input}"
        try:
            controller = getattr(Controller, controller_name)
        except AttributeError:
            print("Method not found")
        else:
            controller()
            
    @staticmethod
    def print_lines():
        print("===============================================================================")
    
    def get_terms_conditions():        
        Controller.print_lines()
        f = Figlet(font='slant')
        print(colored(f.renderText('Terms & Conditions'), 'magenta'))
        Controller.print_lines()
        print(
"""
Dear User,
This crypto bot program automatically predicts next period of each 15 coin and 
buy/sell one of this coins. The aim of this program is to maximize your profit.
By inserting your public key, private key and setting your IP adress on 
https://www.binance.com/en you will be accepted terms and conditions. As Murat
Ugur KİRAZ, I will not accept your money loss.
"""
            )
        
    @staticmethod
    def is_client_status_ok():
        print("Connecting to binance. Please wait...")
        status = Bot().is_connection_ok()
        if status:
            Controller.print_lines()
            f = Figlet(font='slant')
            print(colored(f.renderText('Connection Ok'), 'green'))
            Controller.print_lines()
            return True
        else:            
            ip = get('https://api.ipify.org').content.decode('utf8')
            print(colored("Please check your API keys and be sure to give permission to "+ ip + " address from https://www.binance.com/en",'red'))    
            return False
        
    @staticmethod
    def is_SMTP_mail_connection_ok():
        print("Connecting to mail server. Please wait...")
        status = BBM().check_server_connection()
        if status:
            Controller.print_lines()
            f = Figlet(font='slant')
            print(colored(f.renderText('SMTP Connection Ok'), 'green'))
            Controller.print_lines()
            return True
        else:
            print(colored("Please check your SMTP settings.",'red'))    
            return False
        
    @staticmethod
    def set_database_value(parameter_value, parameter_string):
        parameters=DB().get_parameters()
        Controller.print_lines()
        f = Figlet(font='slant')
        print(colored(f.renderText(parameter_string), 'magenta'))
        Controller.print_lines()
        if not parameters[parameter_value]:
            Controller.change_parameter(parameter_value, parameter_string)
        else:
            chg_parameter = input("Your " + parameter_string +" is:\n--->"+ str(parameters[parameter_value]) + "\n Do yo want to change it? Y/N \n")
            if chg_parameter.upper()=="Y":                
                Controller.change_parameter(parameter_value, parameter_string)
                
    @staticmethod
    def print_parameter_string(parameter_value, parameter_string):
        Controller.generate_menu_header()
        print("Your "+ parameter_string +" is set as\n--->" +colored(parameter_value, 'green'))
        Controller.print_lines()
    
        
    @staticmethod
    def get_input_for_parameter(parameter_value, parameter_string):
        if parameter_value == "pk":
            key = input("Please insert your "+ parameter_string +"\n")
            if key == "":
                print(colored("You should enter a " + parameter_string + "\n", 'red'))
                Controller.set_database_value(parameter_value, parameter_string)
            else:
                return key
        elif parameter_value == "sk":
            key = input("Please insert your "+ parameter_string +"\n")
            if key == "":
                print(colored("You should enter a " + parameter_string + "\n", 'red'))
                Controller.set_database_value("sk","Secret Key")
            else:
                return key
        elif parameter_value == "interval":
            set_interval = input("Type interval time as 1m, 3m, 5m, 15m, 30m, 1h, 2h, 4h or 6h\n")
            if not set_interval in ("1m", "3m", "5m", "15m", "30m", "1h", "2h", "4h", "6h"):
                print(colored("You tried to set wrong value! Type interval time as 1m, 3m, 5m, 15m, 30m, 1h, 2h, 4h or 6h\n", 'red'))
                Controller.set_database_value("interval","Interval")
            else:
                return set_interval
        elif parameter_value == "cash_type":
            set_cash_type = input("Type Cash Type USDT or BNB\n")
            set_cash_type = set_cash_type.upper()
            if not set_cash_type in ("BNB","USDT"):
                print(colored("You tried to set wrong value! Type Cash Type USDT or BNB\n", 'red'))
                Controller.set_database_value("cash_type","Cash Type")
            else:
                return set_cash_type
        elif parameter_value == "mail":
            mail = input("Please insert your "+ parameter_string +"\n")
            regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
            if mail == "":
                print(colored("You should enter a " + parameter_string + "\n", 'red'))
                Controller.set_database_value("mail","Mail Address")
            elif not (re.fullmatch(regex, mail)):
                print(colored("You should enter a valid mail address", 'red'))
                Controller.set_database_value("mail","Mail Address")
            else:
                return mail
        elif parameter_value == "cash":
            parameters=DB().get_parameters()
            if parameters["cash_type"] == "":
                print(colored("You did not set a cash type. Please set it from menu 7\n", "red"))
                Controller.set_database_value("cash_type","cash type")
            else:
                status = Controller.is_client_status_ok()
                if status:
                    parameters=DB().get_parameters()
                    print("Getting your cash amount. Please wait...")
                    assets=Bot().get_asset_balance(asset=parameters["cash_type"])
                    set_cash=input("You have {:.5f} {}. Please set value below this number.\n".format(float(assets['free']),parameters["cash_type"]))
                    if not Calc.check_input_int_or_float(set_cash):
                        print(colored("Please set a valid float or integer\n", 'red'))
                        Controller.set_database_value("cash","Cash")
                    else:
                        if float(set_cash)>float(assets['free']):
                            print(colored("You typed {}, it is a bigger credit than you have ({}) Check again!\n".format(set_cash,float(assets['free'])), 'red'))
                            Controller.set_database_value("cash","Cash")
                        else:
                            return float(set_cash)
        elif parameter_value == "cash_limit":
            parameters=DB().get_parameters()
            if parameters["cash"] == "":
                print(colored("You did not set cash. Please set it from menu 8\n", "red"))
                Controller.set_database_value("cash","Cash")
            else:
                cash_limit = input("Cash limit is the value of cash that you admit to lose. Below that amount the \nbot will satop automatically. It will be calculated with percentage- like %10.\nPlease insert your "+ parameter_string +" between 0-100 as percentage. The amount will be \ncalculated and set as cash.\n")
                if (cash_limit == ""):
                    Controller.generate_menu_header()
                    print(colored("You should enter a " + parameter_string + "\n", 'red'))
                    Controller.set_database_value("cash_limit","Cash Limit")
                elif not Calc.check_input_int_or_float(cash_limit):
                    print(colored("Please set a valid float or integer\n", 'red'))
                    Controller.set_database_value("cash_limit","Cash Limit")
                elif float(cash_limit)<=0 or float(cash_limit)>100:
                    print(colored("Please set a value between 0 and 100\n", 'red'))
                    Controller.set_database_value("cash_limit","Cash Limit")
                else:
                    parameters=DB().get_parameters()
                    cash = float(parameters["cash"])
                    cash_limit = float(cash_limit)
                    cash_limit = 100 - cash_limit
                    cash_limit = (cash * cash_limit) / 100
                    return cash_limit
                
        elif parameter_value == "stop_loss_limit":
            stop_loss_limit = input("After bot buying a coin, within 10 seconds it will check the average price of \nthe coin. If the loss is below that percentage, the coin will be sold automatically.\nIt will be set as percentage- like 0.001.\nPlease insert your "+ parameter_string +" between 0-1.\nDo not forget to set decimal value with dot(.) not with comma (,)\n")   
            if stop_loss_limit == "":
                print(colored("You should enter a " + parameter_string + "\n", 'red'))
                Controller.set_database_value(parameter_value, parameter_string)
            elif not Calc.check_input_int_or_float(stop_loss_limit):
                print(colored("Please set a valid float or integer\n", 'red'))
                Controller.set_database_value(parameter_value, parameter_string)
            elif float(stop_loss_limit)<=0 or float(stop_loss_limit)>1:
                print(colored("Please set a value between 0 and 1. \nDo not forget to set decimal value with dot(.) not with comma (,)\n", 'red'))
                Controller.set_database_value(parameter_value, parameter_string)
            else:
                return float(stop_loss_limit)        
            
        elif parameter_value == "number_of_coin":
            print("Bot will get a list of most traded coins among this number. Please enter a \nnumber between 1 and 10")
            number_of_coin = input("Please insert your "+ parameter_string +"\n")
            if number_of_coin == "":
                print(colored("You should enter a " + parameter_string + "\n", 'red'))
                Controller.set_database_value(parameter_value, parameter_string)
            elif not Calc.check_input_int(number_of_coin):
                print(colored("Please set a valid integer\n", 'red'))
                Controller.set_database_value(parameter_value, parameter_string)
            elif int(number_of_coin)<1 or int(number_of_coin)>10:
                print(colored("Please set a value between 0 and 10.", 'red'))
                Controller.set_database_value(parameter_value, parameter_string)
            else:
                return number_of_coin
            
        elif parameter_value == "SMTPserver":
            print("Bot will communicate with you via that server.")
            SMTPserver = input("Please insert your "+ parameter_string +"\n")
            if SMTPserver == "":
                print(colored("You should enter a " + parameter_string + "\n", 'red'))
                Controller.set_database_value(parameter_value, parameter_string)
            else:
                return SMTPserver
            
        elif parameter_value == "SMTPusername":
            print("Bot will communicate with you via that server.")
            SMTPusername = input("Please insert your "+ parameter_string +"\n")
            if SMTPusername == "":
                print(colored("You should enter a " + parameter_string + "\n", 'red'))
                Controller.set_database_value(parameter_value, parameter_string)
            else:
                return SMTPusername
            
        elif parameter_value == "SMTPpassword":
            print("Bot will communicate with you via that server.")
            SMTPpassword = input("Please insert your "+ parameter_string +"\n")
            if SMTPpassword == "":
                print(colored("You should enter a " + parameter_string + "\n", 'red'))
                Controller.set_database_value(parameter_value, parameter_string)
            else:
                return SMTPpassword
            
    @staticmethod
    def change_parameter(parameter_value, parameter_string):
        parameter = Controller.get_input_for_parameter(parameter_value, parameter_string)
        if not parameter is None:
            DB().update_data("parameters", [parameter_value], [parameter])
            if parameter_value == "cash_type":
                DB().update_data("parameters", ["cash"], [""])
                DB().update_data("parameters", ["cash_start"], [""])
                DB().update_data("parameters", ["cash_limit"], [""])
            elif parameter_value == "cash":
                DB().update_data("parameters", ["cash_start"], [parameter])
                DB().update_data("parameters", ["cash_limit"], [""])
                DB().update_data("parameters", ["has_cash"], [1])
            Controller.print_parameter_string(parameter, parameter_string)
    
    @staticmethod
    def generate_menu_header():
        Controller.print_lines()
        f = Figlet(font='slant')
        print(colored(f.renderText('Menu'), 'magenta'))
        print("Created by Murat Uğur KİRAZ")
        Controller.print_lines()
        do_methods = [m for m in dir(Controller) if m.startswith('do_')]
        menu_string = "\n".join([getattr(Controller, method).__doc__ for method in do_methods])
        print(menu_string)
        Controller.print_lines()
    
    @staticmethod
    def generate_menu():        
        Controller.generate_menu_header()
        print("Choose an operation:", end="")
        
    @staticmethod
    def run():
        Controller.generate_menu()
        user_input = "00"
        while(user_input != "18"):
            try:
                user_input = str(input())
                if len(user_input) == 1:
                    user_input = "0" + user_input
            except ValueError:
                print("value error")
                Controller.generate_menu()
            finally:
                Controller.generate_menu_header()                
                Controller.execute(user_input)
                print("Choose an operation:", end="")
        print("\nThank you for using Binance Bot by Murat Ugur KİRAZ.")