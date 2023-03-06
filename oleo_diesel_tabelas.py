'''
Script para baixar pdf com preços atualizados do óleo combustível A1 e exportar dados para planilha excel
'''
# Módulos padrões
from datetime import datetime, timedelta, date

# Módulos desenvolvidos
from pdf_converter import *
from tabelas_petrobras import *
from converte_unidades import *
from ream import *
from html_page import *


#----------------------------------------------------------------------------------------------------------------------------------- 
if __name__ == "__main__":
    # Execucação do script p/ o óleo combustível A14
    catch = 0
    data_ult_lanc = date.today()
    
    while catch == 0:
        link = "https://precos.petrobras.com.br/documents/d/precos-dos-combustiveis/tabelas-de-precos-oc-"+ data_ult_lanc.strftime("%d-%m-%y") +"-pdf"
        if requests.get(link).status_code == 200:
            pdf = Pdf(link, "oleoCombustivel")
            catch += 1
        else:
            data_ult_lanc = data_ult_lanc - timedelta(days=1) 
            
    pdf.baixa_pdf()

    # Criando a tabela com os dados do pdf baixado
    num_pages_a, num_pages_b = Tabela("oleoCombustivel").count_pages()
    
    a1 = Tabela("oleoCombustivel").concat_pdf_tables(1, num_pages_a)
    a1 = Tabela("oleoCombustivel").rearrange(a1)
    a1 = UnidadeMedida(a1).divide_por(980)

    # Chamando a tabela do b1 apenas para pegar a coluna de preços de barcarena e subtraindo 40 para atribuir a coluna de mesmo nome no OCA1
    b1 = Tabela("oleoCombustivel").concat_pdf_tables(num_pages_a + 1, num_pages_a + num_pages_b)
    b1 = Tabela("oleoCombustivel").rearrange(b1)
    b1 = UnidadeMedida(b1).divide_por(1)
    barcarena_a1 = b1['BARCARENA (PA) LTM'].astype(int) - 40
    a1['BARCARENA (PA) LTM'] = barcarena_a1/980

    # Colocando o valor da Ream para Manaus
    data_atual = date.today()

    try:
        rv = Ream('oca1', data_atual.month, data_atual.year).ream_value()
    except:
        rv = Ream('oca1', data_atual.month-1, data_atual.year).ream_value()
        
    if datetime.strptime(a1.index[-1], '%d/%m/%Y').day != data_atual.day:
        pass
    else:
        pass
    
    print(a1)
    print('')
    print(rv)
    exit()

    HtmlPage().html_file(a1, 'oca1')

    os.remove("oleoCombustivel.pdf")
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
    HtmlPage().html_file(s10, 'diesel_s10')
    
    os.remove("diesel.pdf")
    # ------------------------------------------------------------------------------------------------------------------------

    
