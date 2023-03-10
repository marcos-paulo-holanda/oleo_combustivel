'''
Captura em tempo real o valor de cotação do Petróleo Brent, salvo os valores em um bd e gera gráficos que são salvos numa pasta.
Link de acesso para valor do Brent: https://oilprice.com/oil-price-charts/#Brent-Crude
Link de acesso para cotação do dolar: https://olinda.bcb.gov.br/olinda/servico/PTAX/versao/v1/aplicacao#!/recursos/CotacaoDolarPeriodo
'''
import os
import requests as req
import pandas as pd
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import time
from bs4 import BeautifulSoup
import mysql.connector

class Dolar:
    '''Objeto para retonar a data e cotação de venda do dólar'''
    def cotacao_dolar(self):
            
        dI = datetime.today().strftime("%m-%d-%Y")
        dF = datetime.today() - timedelta(days=3) # range de dias a serem buscado
        dF = dF.strftime("%m-%d-%Y")

        prd = "https://olinda.bcb.gov.br/olinda/servico/PTAX/versao/v1/odata/CotacaoDolarPeriodo(dataInicial=@dataInicial,dataFinalCotacao=@dataFinalCotacao)?@dataInicial=" \
        + "'" + dF + "'" + "&@dataFinalCotacao=" + "'" + dI + "'" + "&$top=100000&$format=json&$select=cotacaoCompra,cotacaoVenda,dataHoraCotacao"

        cotacao = req.get(prd).json()

        datas, venda = [], []

        for i in range(len(cotacao['value'])):
            venda.append(cotacao['value'][i]['cotacaoVenda'])
            datas.append(cotacao['value'][i]['dataHoraCotacao'])

        datas = [x[:10] for x in datas]

        return datas[-1], venda[-1] #o indice -1 pega o valor mais recente cotado no mercado

class Oleo:
    def brent(self):
        url = 'https://oilprice.com/oil-price-charts/#Brent-Crude'

        r = req.get(url)
        html_doc = r.text
        soup = BeautifulSoup(html_doc, "html.parser")

        tag = soup.find_all('td', {'class':'last_price'})

        brent_last_price = tag[1].get_text()

        return brent_last_price

        
def fuel_oil_price():
    data_cotac, venda_cotac = Dolar().cotacao_dolar()
    brent_cotac = float(Oleo().brent())
    fuel_oil = round(venda_cotac*brent_cotac*0.0071388,2)
    return fuel_oil


    
    

    
