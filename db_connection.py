#---------------------------------------------------------------------------------------------------#
# File name: db_connection.py                                                                       #
# Autor: Chrissi2802                                                                                #
# Created on: 19.12.2022                                                                            #
#---------------------------------------------------------------------------------------------------#
# This file provides classes / functions to connect and communicate with a database.
# Exact description in the functions.


import yaml
from yaml.loader import SafeLoader
import pyodbc
import pandas as pd


class SQL_Connection():
    """This class can be used to establish a connection to an SQL server.
    """
    
    def __init__(self):
        """Initialisation of the class (constructor).
        """
        
        # Read yaml file
        self.stream = open("db_connection.yaml", "r")
        login_data_yaml = list(yaml.load_all(self.stream, Loader = SafeLoader))[0]  # Data are only in the first element -> dictionary
        
        self.driver = "ODBC Driver 17 for SQL Server"
        self.server = login_data_yaml["server"]
        self.database = login_data_yaml["database"]
        self.username = login_data_yaml["username"]
        self.password = login_data_yaml["password"]
        self.login = "DRIVER={" + self.driver + "};SERVER=" + self.server + ";DATABASE=" + self.database + \
                     ";UID=" + self.username + ";PWD=" + self.password
                     
        self.connect()
        
    def connect(self):
        """This method connects to the database.
        """

        try:
            self.conn = pyodbc.connect(self.login)
            self.cursor = self.conn.cursor()
        except pyodbc.Error as e_connection:
            print("Error with SQL connection!")
            print("Error number:", e_connection)

    def disconnect(self):
        """This method disconnects from the database.
        """
        
        self.conn.close()
        
        
class MSSQL_Connection(SQL_Connection):
    """This class can be used to connect to an SQL server and execute commands.

    Args:
        SQL_Connection (class): Parent class from which is inherited
    """

    def __init__(self, table):
        """Initialisation of the class (constructor).
        
        Args:
            table (string): Table name
        """
        
        super().__init__()
        self.table = table
        
    def count_id(self): 
        """This method counts all ids in the table.
        
        Returns:
            count (integer): Number of ids
        """
        
        sql_command = "SELECT COUNT(ID) FROM " + self.database + "." + self.table + ";"
        df = pd.read_sql(sql_command, self.conn)
        count = df.iloc[0, 0]   # only the count as integer
        
        return count
        
    def read_data(self, where = ""):
        """This method reads all data from the table into a DataFrame.
        
        Args:
            where (string, optional): SQL WHERE statement, if only a part of the data is to be considered. Defaults to "".
            
        Returns:
            df (pandas DataFrame): Data from the table
        """
        
        sql_command = "SELECT * FROM " + self.database + "." + self.table + where + ";"
        df = pd.read_sql(sql_command, self.conn)
        
        return df
    
    def read_data_select(self, sql_command):
        """This method reads all data from the table into a DataFrame with a passed SELECT command.

        Args:
            sql_command (string): Complete SELECT command

        Returns:
            df (pandas DataFrame): data from the table
        """
        
        df = pd.read_sql(sql_command, self.conn)
        
        return df
    
    
if (__name__ == "__main__"):

    table = "dbo.table"
    select_command = "SELECT ID, NAME FROM Customers." + table + " WHERE STATUS = 'active';"
    
    CMSSQL_Connection = MSSQL_Connection(table)
    
    counts = CMSSQL_Connection.count_id()
    df_complete = CMSSQL_Connection.read_data()
    df_part = CMSSQL_Connection.read_data_select(select_command)
    
    CMSSQL_Connection.disconnect()
    
    print(counts)
    print(df_complete)
    print(df_part)

    