'''
Script para baixar pdf com preços atualizados do óleo combustível A1 e exportar dados para planilha excel
'''
import requests, os 
import tabula
import pandas as pd
import locale
from datetime import datetime, timedelta, date
from IPython.display import HTML

#"https://precos.petrobras.com.br/documents/77785/82038/Tabelas+de+Pre%C3%A7os+-+OC+-+25-01-23.pdf/6842ff74-2eea-3a71-290e-660aa6eb2570?t=1674672690411"

class Pdf:
    """Classe para baixar e salvar localmente o arquivo pdf"""
    def __init__(self, link, file_name):
        self.link = link
        self.file_name = file_name

    def baixa_pdf(self):
        # Baixa arquivo pdf das tabelas converte para csv
        response = requests.get(self.link)
        pdf = open(self.file_name + ".pdf", 'wb')
        pdf.write(response.content)
        pdf.close() 

        
#-----------------------------------------------------------------------------------------------------------------------------------

class Tabela:
    """Classe para gerar tabelas no pandas através da leitura dos dados do arquivo pdf baixado"""
    def __init__(self, file_name):
        self.file_name = file_name

    def count_pages(self):
        '''Método para retornar o números de paginas do histórico de um determinado combustível'''
        df = tabula.read_pdf(self.file_name + ".pdf", pages="all")
        num_pages_a = 1
        num_pages_b = 1
        for i in range(0,len(df)):
            if len(df[i]) == len(df[i+1]):
                num_pages_a += 1
            else:
                for j in range(i+1, len(df)):
                    if len(df[j]) == len(df[j+1]):
                        num_pages_b += 1
                    else:
                        break
                break
  
        return num_pages_a, num_pages_b
        
        
    def concat_pdf_tables(self, pg_start, pg_end):
        '''Concatena as tabelas das páginas do arquivo pdf'''
        df = tabula.read_pdf(self.file_name + ".pdf", pages=[x for x in range(pg_start, pg_end + 1)])

        df = pd.concat(df[:pg_end +1][:], axis = 1)
        df['LOCAL'] = df.iloc[:,0] + ' ' + df.iloc[:,1]
        df.drop(df.columns[1], axis =1, inplace = True)

        df = df.T.drop_duplicates().T

        return df

    def rearrange(self, tb):
        '''Arruma as datas e transpoe a tabela'''
        # Troca o . para / nas datas
        rename_columns = []
        for v in tb.columns:
            rename_columns.append(v.replace('.','/'))
        tb.columns = rename_columns

        # Identifica quantas vezes precisa repetir os dados de uma determinada coluna para os dias que ñ há dados
        delta_days = []
        for i in range(1, len(tb.columns) - 1):
            delta = datetime.strptime(tb.columns[i+1], "%d/%m/%Y") - datetime.strptime(tb.columns[i], "%d/%m/%Y")
            delta_days.append(delta.days)

        col_name_copy = list(tb.columns[1:-1]) #backup dos nomes das colunas da tb
        datas_range = dict(zip(col_name_copy, delta_days))

        # Insere as colunas de dados para as datas inexistentes
        for key in datas_range:
            n_insertion = datas_range[key]
            for n in range(1, n_insertion):

                tb.insert(
                    tb.columns.get_loc(key) + n,
                    datetime.strftime((datetime.strptime(key, '%d/%m/%Y') + timedelta(days = n)), "%d/%m/%Y"),
                    tb[key]
                    )
        # Transpoe a tabela para qual as datas se tornam os indices da tabela
        tb = tb.T
        tb = tb.set_axis(tb.iloc[0, :], axis=1)
        tb.drop(tb.index[0], axis=0, inplace=True)
        
        return tb

#-----------------------------------------------------------------------------------------------------------------------------------
class UnidadeMedida:
    """Classe para converter as unidades de medida da tabela gerada.
    Inicialmente muda a notação do numeral de PTG(x.xxx,x) para ENG(x,xxx.x) 
    """
    locale.setlocale(locale.LC_NUMERIC, 'en_DK.UTF-8')
    def __init__(self, tabelao):
        self.tabelao = tabelao

    def divide_por(self, divisor):
        # Método para percorrer as colunas do tabelao, muda o formato do numeral e divide por um número
        self.tabelao.fillna('0,0', inplace=True)
        for j in range(len(self.tabelao.columns)):
            lista = self.tabelao.iloc[:, j].values
            lista = [locale.atof(x)/divisor for x in lista]
            self.tabelao[self.tabelao.columns[j]] = lista
            
        self.tabelao.replace([float(0)], '', inplace = True)
        
        return self.tabelao

    
#-----------------------------------------------------------------------------------------------------------------------------------
class HtmlPage:
    '''Recebe uma dataframe, converte para html e formata o mesmo'''
    def html_file(self,df, file_name):
        # converte a df para html
        html_file = df.to_html()
        index_file = open(file_name + '.html', 'w')
        index_file.write(html_file)
        index_file.close()
        # Formata o arquivo com código css
        file = open(file_name + '.html', 'a')
        text = '<link rel="stylesheet" href="css/styles.css">'
        file.write(text)
        file.close()

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

    
