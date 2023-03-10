'''
Script para baixar pdf com preços atualizados do óleo combustível A1 e exportar dados para planilha excel
'''
# Módulos padrões
from datetime import datetime, timedelta, date
import pandas as pd

# Módulos desenvolvidos
from pdf_converter import *
from tabelas_petrobras import *
from database_access import *
from converte_unidades import *
from ream import *
from html_page import *
from fuel_oil import *
from abicom import *


#----------------------------------------------------------------------------------------------------------------------------------- 
if __name__ == "__main__":
    # Execucação do script p/ o óleo combustível A14
    catch = 0
    data_ult_lanc = date.today()
    '''  
    while catch == 0:
        link = "https://precos.petrobras.com.br/documents/d/precos-dos-combustiveis/tabelas-de-precos-oc-"+ data_ult_lanc.strftime("%d-%m-%y") +"-pdf"
        if requests.get(link).status_code == 200:
            pdf = Pdf(link, "oc")
            catch += 1
        else:
            data_ult_lanc = data_ult_lanc - timedelta(days=1) 
     
    pdf.baixa_pdf()

    # Criando a tabela com os dados do pdf baixado
    num_pages_a, num_pages_b = Tabela("oc").count_pages()

    a1 = Tabela("oc").concat_pdf_tables(1, num_pages_a)
    a1 = Tabela("oc").rearrange(a1)
    a1 = UnidadeMedida(a1).divide_por(980)
    
    # Chama a tabela do b1 apenas para pegar a coluna de preços de barcarena e subtrair 40 para atribuir a coluna de mesmo nome no OCA1
    b1 = Tabela("oc").concat_pdf_tables(num_pages_a + 1, num_pages_a + num_pages_b)
    b1 = Tabela("oc").rearrange(b1)
    b1 = UnidadeMedida(b1).divide_por(1)
    barcarena_a1 = b1['BARCARENA (PA) LTM'].astype(int) - 40
    a1['BARCARENA (PA) LTM'] = barcarena_a1/980

    # Colocando o valor da Ream para Manaus
    data_atual = date.today()

    # TryExecept para pegar o valor do OCA1 da Ream do mes atual ou anterior caso o valor do mes atual n exista
    try:
        rv = Ream('oca1', data_atual.month, data_atual.year).ream_value()
    except:
        rv = Ream('oca1', data_atual.month-1, data_atual.year).ream_value()

    #Substituindo os valores de Manaus conforme o divulgado pela Ream
    a1['MANAUS (AM) FOB'] = a1['MANAUS (AM) FOB'].replace([''],[str(rv)])

    # Ult lanc do OCA1. Pega a ult linha da DF a1 para inserir no BD ou Excel
    last_a1 = a1.iloc[-1:,:]

    # Valor do fuel Oil
    fuel_oil = fuel_oil_price()

    # Média das refinarias exceto Manaus
    med_ref = last_a1.drop('MANAUS (AM) FOB', axis = 1).values[0]
    med_ref = np.array([round(x,4) for x in med_ref if type(x) == float]).mean()
    med_ref = round(med_ref, 4)

    # Defini a linha para ser inserida no BD ou Excel
    last_a1_values = list(last_a1.values[0])
    for i in range(len(last_a1_values)):
        if type(last_a1_values[i]) == float:
            last_a1_values[i] = str(round(last_a1_values[i],4))

    last_a1_values.append(str(fuel_oil))
    last_a1_values.append(str(med_ref))
    last_a1_values.insert(0, datetime.strftime(data_atual, '%d/%m/%Y'))
    
    os.remove("oc.pdf")
    '''
    # ------------------------------------------------------------------------------------------------------------------------

    # Execução do script p/ o diesel S500 e S10
    catch = 0
    data_ult_lanc = date.today()
    
    while catch == 0:
        link = "https://precos.petrobras.com.br/documents/d/precos-dos-combustiveis/tabelas-de-precos-diesel-s500-e-s10-"+ data_ult_lanc.strftime("%d-%m-%y") +"-pdf"
        if requests.get(link).status_code == 200: 
            pdf = Pdf(link, "diesel")
            catch += 1
        else:
            data_ult_lanc = data_ult_lanc - timedelta(days=1)

    pdf.baixa_pdf()
    num_pages_a, num_pages_b = Tabela("diesel").count_pages()
    
    s10 = Tabela("diesel").concat_pdf_tables(num_pages_a + 1, num_pages_a + num_pages_b)
    s10 = Tabela("diesel").rearrange(s10)
    s10 = UnidadeMedida(s10).divide_por(1000)

    #Substituindo os valores de Manaus conforme o divulgado pela Ream
    data_atual = date.today()
    rv = Ream('s10', data_atual.month, data_atual.year).ream_value()
    s10['Manaus (AM) EXA'] = s10['Manaus (AM) EXA'].replace([''],[str(rv)])

    # Pega a ult linha da df
    last_s10 = s10.iloc[-1:,:]

    # Inserindo o valor da Abicom
    abicom_ppi_value()
    abicom = float(input('Digite o valor do PPI no formato x.xxx: '))
    os.remove("ppi_image.png")
    
    os.remove("diesel.pdf")
    # ------------------------------------------------------------------------------------------------------------------------

    
