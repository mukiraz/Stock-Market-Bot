# -*- coding: utf-8 -*-
"""
Created on Tue Jun  7 03:21:40 2022

This class logs events and errors.

@author: Murat Uğur KİRAZ
"""

from datetime import date,datetime
from pathlib import Path

class Logging():
    #In construction, folders are created year and monthly.
    def __init__(self,message):
        today=date.today()
        year=today.strftime("%Y")
        month=today.strftime("%m")
        file_name=today.strftime("%d_%m_%Y")+".txt"
        
        path_error="logs"+"/errorLogs/"+year+"/"+month
        path_operation="logs"+"/operationLogs/"+year+"/"+month
        
        Path(path_error).mkdir(parents=True, exist_ok=True)
        Path(path_operation).mkdir(parents=True, exist_ok=True)
        
        full_path_error=path_error+"/"+file_name
        full_path_operation=path_operation+"/"+file_name
        
        if not Path(full_path_error).exists():
            file=open(full_path_error,"w")
            file.close()
            
        if not Path(full_path_operation).exists():
            file=open(full_path_operation,"w")
            file.close()
        
        self.errorfile=full_path_error
        self.operationfile=full_path_operation
        self.message=str(message)
        
    # This method logs events.
    def logEvent(self, current_time=""):
        if current_time=="":            
            current_time=str(datetime.now(tz=None))            
        file=open(self.operationfile, "a")
        file.write(current_time + "   " + self.message + "\n")
        file.close()

    # This method logs errors.
    def logBinanceError(self, function_name, status_code = "", current_time = ""):
        if current_time == "":            
            current_time = str(datetime.now(tz=None))          
        file=open(self. errorfile, "a")
        file.write(current_time +
                   "  function_name: " + function_name +
                   " message: " + self.message +
                   " status_code: " + str(status_code) +
                   "\n")
        file.close()