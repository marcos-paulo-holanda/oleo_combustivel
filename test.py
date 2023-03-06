import pandas as pd
import locale
from datetime import datetime, timedelta, date

def ream(oleo, mes, ano):
    '''Função busca o óleo nos meses de um respectivo ano no site da ream'''
    locale.setlocale(locale.LC_NUMERIC, 'en_DK.UTF-8')
    # Definindo o URL de busca

    if oleo == 's10':
        int_oleo = 2
        mod = 'EXA'
    elif oleo == 's500':
        int_oleo = 3
        mod = 'EXA'
    elif oleo == 'oca1':
        int_oleo = 8
        mod = 'FOB'

    # Monta a url conforme o nome do óleo, mes e ano inseridos
    url = "https://sisdipre.ream.com.br/lancamentos/?produto="+str(int_oleo)+"&data__year=20"+str(ano)+"&data__month="+str(mes)

    # Lê a única tabelas existente na url e transforma para um df do pandas
    ream_table = pd.read_html(url)[0]
    # Busca na tabela o último lançamento para uma determinada modalidade de venda
    str_value = ream_table[ream_table['Modalidade de Venda'] == mod].tail(1)['Preço'].values[0][3:]
    if oleo == 'oca1':
        value  = round(locale.atof(str_value)/1000,4)
    else:
        value  = locale.atof(str_value)
    
    return value

