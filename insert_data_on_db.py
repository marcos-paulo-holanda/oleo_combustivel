import pandas as pd
import locale
from datetime import datetime, timedelta, date
import mysql.connector

def insert_data(table_name, data_tuple):
    sql_query = "INSERT INTO " + table_name +  " VALUES (NULL, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"
    
    conn = mysql.connector.connect(
            user='mrndblogin',
            password='senha@2023',
            host="mrn-mysql-database.mysql.database.azure.com",
            port=3306,
            database='oleo_database',
            ssl_disabled=True)
    cur = conn.cursor()
    
    cur.execute(sql_query, data_tuple)
    
    conn.commit()

def insert_data_diesel(table_name, data_tuple):
    sql_query = "INSERT INTO " + table_name +  " VALUES (NULL, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,\
%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,\
 %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"
    
    conn = mysql.connector.connect(
            user='mrndblogin',
            password='senha@2023',
            host="mrn-mysql-database.mysql.database.azure.com",
            port=3306,
            database='oleo_database',
            ssl_disabled=True)
    cur = conn.cursor()
    
    cur.execute(sql_query, data_tuple)
    
    conn.commit()

def insert_commodity(data_tuple):
    sql = "INSERT INTO bd_commodity VALUES (NULL, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"
    conn = mysql.connector.connect(
            user='mrndblogin',
            password='senha@2023',
            host="mrn-mysql-database.mysql.database.azure.com",
            port=3306,
            database='oleo_database',
            ssl_disabled=True)
    cur = conn.cursor()
    
    cur.execute(sql_query, data_tuple)
    
    conn.commit()

df = pd.read_excel('commodity.xlsx', header=0)
df.data = df.data.dt.strftime('%d/%m/%Y')


for i in range(0, len(df)+1):
    tupla = []
    for x in df.loc[i].values:
        if type(x) != str:
            tupla.append(str(round(x,4)))
        else:
            tupla.append(x)
    insert_commodity(tupla)





