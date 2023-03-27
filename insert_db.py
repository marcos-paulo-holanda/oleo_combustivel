import pandas as pd
from datetime import datetime, timedelta, date
import mysql.connector

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
def insert_db(planilha: str, banco):
    df = pd.read_excel(planilha + '.xlsx', header=0)
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

def insert_same(tabela_bd: str):
    if tabela_bd == 'bd_oc':
        conn, cur = conecta_db()
        "create temporary table tmptable select * from bd_oc order by id desc limit 1;"
    elif tabela_bd == 'bd_diesel_s10':
        conn, cur = conecta_db()
    elif tabela_bd == 'bd_commodity':
        conn, cur = conecta_db()
        "create temporary table tmptable select * from bd_commodity order by id desc limit 1;"
        "update tmptable set id = id+1;"
        "insert into bd_commodity select * from tbmtable;"
        "DROP TEMPORARY TABLE IF EXISTS tmptable;"
        


if __name__ == "__main__":
    tarefa = int(input('Digite 0 replicar registros, 1 para inserir novos registros: '))
    if tarefa == 0:
        pass
    elif tarefa == 1:
        insert_db('historico_oc', insert_oc)
        insert_db('historico_s10', insert_diesel)
        insert_db('commodity', insert_oc)

print('--Mission completed -- ')
