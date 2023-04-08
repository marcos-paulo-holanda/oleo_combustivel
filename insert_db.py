import pandas as pd
from datetime import datetime, timedelta, date
import mysql.connector
from warnings import simplefilter
simplefilter(action="ignore", category=pd.errors.PerformanceWarning)

def conecta_db():
    conn = mysql.connector.connect(
            user='mrndblogin',
            password='senha@2023',
            host="mrn-mysql-database.mysql.database.azure.com",
            port=3306,
            database='oleo_database',
            ssl_disabled=True)
    cur = conn.cursor()
    return conn, cur

def insert_oc(data_tuple):
    sql_query = "INSERT INTO bd_oc VALUES (NULL, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"
    conn, cur = conecta_db()

    cur.execute(sql_query, data_tuple)
    conn.commit()

def insert_diesel(data_tuple):
    sql_query = "INSERT INTO bd_diesel_s10 VALUES (NULL, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,\
%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,\
 %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"
    conn, cur = conecta_db()

    cur.execute(sql_query, data_tuple)
    conn.commit()

def insert_commodity(data_tuple):
    sql_query = "INSERT INTO bd_commodity VALUES (NULL, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"
    conn, cur = conecta_db()

    cur.execute(sql_query, data_tuple)
    conn.commit()

#------------------------------------------------------------------------
def insert_db(planilha: str, subplanilha: str,banco):
    arquivo_excel = pd.ExcelFile(planilha + '.xlsx')
    df = pd.read_excel(arquivo_excel, subplanilha, header=0)
    df.fillna('', inplace = True)
    df.data = df.data.dt.strftime('%d/%m/%Y')
    for i in range(len(df)):
        tupla = []
        for x in df.loc[i].values:
            if type(x) != str:
                tupla.append(str(round(x,4)))
            else:
                tupla.append(x)
        banco(tupla)
        
if __name__ == "__main__":
    
    insert_db('combustiveis','oc', insert_oc)
    insert_db('combustiveis','s10', insert_diesel)
    insert_db('combustiveis', 'commodity', insert_commodity)

print('--Mission completed -- ')
