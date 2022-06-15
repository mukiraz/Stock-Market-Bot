# -*- coding: utf-8 -*-
"""
Created on Sun May 29 15:42:26 2022

@author: Murat Ugur KIRAZ
"""

import sqlite3

class DatabaseClass(object):
    __DB_LOCATION = "operations.db"
    
    def __init__(self):
        self.__db_connection = sqlite3.connect(self.__DB_LOCATION)
        self.cursor=self.__db_connection.cursor()
        self.transactions = self.get_column_names("transactions")
        self.parameters = self.get_column_names("parameters")
        
    def insert_data(self, table, values):
        add_quest_marks="("
        for i in range(len(values)):
            if i!=(len(values)-1):
                add_quest_marks+="?, "
            else:
                add_quest_marks+="?)"
        if table=="transactions":
            columns=self.transactions
            columns =self.transactions.split(", ")
            columns.remove('id')
            columns = "(" + ", ".join(columns) + ")"
            
    
        sentence="INSERT INTO " + table + " " + columns + " VALUES" + add_quest_marks
        self.cursor.execute(sentence,values)
    
    def update_data(self,table,columns,values,where=1):
        add_quest_marks=""
        where=where
        for i in range(len(columns)):
            if i!=(len(columns)-1):
                add_quest_marks+=columns[i]+"=?, "
            else:
                add_quest_marks+=columns[i]+"=? "
        if table=="parameters":
            where=1
        values.append(where)
        update_str="UPDATE " + table + " SET " + add_quest_marks + " WHERE id=?"
        self.cursor.execute(update_str,values)
        
    def change_has_status(self):
        has_cash=""
        has_coin=""
        for row in self.cursor.execute("SELECT has_cash FROM parameters WHERE id=1"):
            has_cash=row[0]
        self.__db_connection.commit()
        if has_cash==1:
            has_cash=0
            has_coin=1
        else:
            has_cash=1
            has_coin=0
        self.cursor.execute("UPDATE parameters SET has_cash=?, has_coin=? WHERE id=1",[has_cash,has_coin])
    
    def get_parameter_by_name(self,param):
        param_str="SELECT "+ param +" FROM parameters WHERE id=1"
        for row in self.cursor.execute(param_str):
            return row[0]
    
    def get_parameters(self):
        self.__db_connection.row_factory = lambda c, r: dict(zip([col[0] for col in c.description], r))
        c = self.__db_connection.cursor()
        execute_string = "SELECT " + self.parameters + " FROM parameters WHERE id=1"
        

        parameters = c.execute(execute_string).fetchall()
        return parameters[0]
    
    def reset_parameters(self):
        parameters =self.parameters.split(", ")
        parameters.remove('id')
        parameter_values = ["" for i in range(len(parameters))]
        self.update_data("parameters", parameters, parameter_values)
        self.cursor.execute("DELETE FROM transactions;")
    
    def get_column_names(self, table_name):
        cursor_string = "SELECT * FROM " + table_name
        data=self.cursor.execute(cursor_string)
        table = list()
        for column in data.description:
            table.append(column[0])
        return ", ".join(table)
        
        
    def __del__(self):
        self.__db_connection.commit()
        self.__db_connection.close()

