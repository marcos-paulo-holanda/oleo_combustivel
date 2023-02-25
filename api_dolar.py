'''
Captura em tempo real o valor de cotação do Petróleo Brent, salvo os valores em um bd e gera gráficos que são salvos numa pasta.
Link de acesso para valor do Brent: https://oilprice.com/oil-price-charts/#Brent-Crude
Link de acesso para cotação do dóalr: https://olinda.bcb.gov.br/olinda/servico/PTAX/versao/v1/aplicacao#!/recursos/CotacaoDolarPeriodo
'''
import requests as req
import pandas as pd
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
from scipy import interpolate
import sqlite3
from datetime import datetime, timedelta
from bs4 import BeautifulSoup

class Dolar:
    '''Objeto para retonar a data e cotação de venda do dólar'''
    def cotacao_dolar(self):
            
        dI = datetime.today().strftime("%m-%d-%Y")
        dF = datetime.today() - timedelta(days=1) # range de dias a serem buscado
        dF = dF.strftime("%m-%d-%Y")

        prd = "https://olinda.bcb.gov.br/olinda/servico/PTAX/versao/v1/odata/CotacaoDolarPeriodo(dataInicial=@dataInicial,dataFinalCotacao=@dataFinalCotacao)?@dataInicial=" \
        + "'" + dF + "'" + "&@dataFinalCotacao=" + "'" + dI + "'" + "&$top=100000&$format=json&$select=cotacaoCompra,cotacaoVenda,dataHoraCotacao"

        cotacao = req.get(prd).json()

        datas, venda = [], []

        for i in range(len(cotacao['value'])):
            venda.append(cotacao['value'][i]['cotacaoVenda'])
            datas.append(cotacao['value'][i]['dataHoraCotacao'])

        datas = [x[:10] for x in datas]

        return datas[0], venda[0]

class Oleo:
    def brent(self):
        url = 'https://oilprice.com/oil-price-charts/#Brent-Crude'

        r = req.get(url)
        html_doc = r.text
        soup = BeautifulSoup(html_doc, "html.parser")

        tag = soup.find_all('td', {'class':'last_price'})

        brent_last_price = tag[1].get_text()

        return brent_last_price

class DatabaseConnector:
    '''Classe para conectar ao banco de dados.'''
    def __init__(self,  db_path):
        self.db_path = db_path

    def conecta_db(self):
        '''Conecta ao banco com o caminho especificado pelo atributo db_path'''
        self.conn = sqlite3.connect(self.db_path)
        self.cur = self.conn.cursor()

    def desconecta_db(self):
        '''Encerra a conecção com o banco de dados'''
        self.conn.close()
        self.conn = None
        self.cur = None

class DatabaseTable(DatabaseConnector):
    '''Conecta ao banco e realiza operações de CRUD'''

    def cria_registros(self, table_name, data_tuple):
        '''Recebe o nome da tabela e cria registro nela'''
        sql_query = "INSERT INTO " + table_name +  " VALUES (?,?,?);"
        self.cur.execute(sql_query, data_tuple)
        self.conn.commit()

    def create_table(self):
        '''Cria a tabela caso não exista'''
        sql_query = "CREATE TABLE IF NOT EXISTS ParidadeOCA1 (data text, dolar float, brent text)"
        self.cur.execute(sql_query)
        self.conn.commit()

class Dataframe:
    '''Classe para colocar os dados do db numa dataframe do pandas'''
    def pandas_df(self, database_name, table_name):
        cnx = sqlite3.connect(database_name)
        df = pd.read_sql_query("SELECT * FROM " + table_name, cnx)
        cnx.commit()
        cnx.close()
        df.brent = pd.to_numeric(df.brent)
        df['fuel oil'] = round(df.dolar*df.brent*0.71388,2)
        
        return df

class Grafico:
    '''Classe para criação de gráficos dos dados da dataframe gerada através do bd.
    Os gráficos gerados são salvos na pasta de imagens.
    '''
    def linha(self, df):
        ano_mes = str(df.data[0][:7])
        x = [int(value[8:]) for value in df['data']]
        y = [float(value) for value in df['fuel oil']]
        
        sns.set_style("darkgrid")
        
        g = sns.lineplot(x=x , y=y, color='green', marker='o', linestyle='dashed')
        
        plt.title('Fuel Oil -- Período ' + ano_mes)
        plt.xlim(min(x) - 0.3, max(x) + 0.3),plt.ylim(min(y) - 20, max(y) + 20)
        plt.xlabel('Dia'), plt.ylabel('Fuel Oil')
        plt.xticks(x, rotation=0)
        for a,b in zip(x,y):
            plt.text(a,b,str(b), rotation = 75)
    
        plt.savefig('images/fuel_line_img.jpg')


    def barra(self,df):
        ano_mes = str(df.data[0][:7])
        x = [int(value[8:]) for value in df['data']]
        y = df['fuel oil']
        sns.set_style("darkgrid")
        g = sns.barplot(data=df, x=x, y=y, color ='#eab676')
        g.bar_label(g.containers[0])
        plt.title('Fuel Oil -- Período ' + ano_mes)
        plt.xlabel('Dia')
        plt.ylabel('Fuel Oil')
        for a,b in zip(x,y):
            plt.text(a,b,str(b))

        plt.savefig('images/fuel_bar_img.jpg')
        
if __name__ == "__main__":
    data_cotac, venda_cotac = Dolar().cotacao_dolar()
    brent_cotac = Oleo().brent()
    data_tuple = tuple([data_cotac,venda_cotac, brent_cotac])
    db = DatabaseTable('oleo_database.db')
    db.conecta_db()
    db.create_table()
    db.cria_registros('ParidadeOCA1',data_tuple)
    db.desconecta_db()

    # Criação das imagens do gráficos
    df = Dataframe().pandas_df('oleo_database.db', 'ParidadeOCA1')

    Grafico().barra(df)
    Grafico().linha(df)
    print('----- The process has been completed --', '\n')
    input('----- Press any button to finish ------')
    
    
    
