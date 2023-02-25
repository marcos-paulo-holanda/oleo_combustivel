'''
Script para baixar pdf com preços atualizados do óleo combustível A1 e exportar dados para planilha excel
'''
import requests, os 
import tabula as tb, pandas as pd
import locale
from datetime import datetime, timedelta
from IPython.display import HTML

#"https://precos.petrobras.com.br/documents/77785/82038/Tabelas+de+Pre%C3%A7os+-+OC+-+25-01-23.pdf/6842ff74-2eea-3a71-290e-660aa6eb2570?t=1674672690411"

class GerarPdf:
    """Classe para baixar e salvar localmente o arquivo pdf"""
    def __init__(self, link, file_name):
        self.link = link
        self.file_name = file_name

    def baixa_pdf_csv(self):
        # Baixa arquivo pdf das tabelas converte para csv
        response = requests.get(self.link)
        pdf = open(self.file_name + ".pdf", 'wb')
        pdf.write(response.content)
        pdf.close() 

        df = tb.read_pdf(self.file_name + ".pdf", pages="all")
        return tb.convert_into(self.file_name + ".pdf", self.file_name + ".csv", output_format = "csv", pages = "all")


#-----------------------------------------------------------------------------------------------------------------------------------

class GerarTabelas:
    """Classe para gerar tabelas no pandas através da leitura dos dados do arquivo pdf baixado"""
    def __init__(self, numLin, skipLinhas, csv_file_name):
        self.numLin = numLin
        self.skipLinhas = skipLinhas
        self.csv_file_name = csv_file_name
        
    def tabela(self):
        # Função que gera a tabela e concatena LOCAL com MODALIDADE, além de renomear tal coluna gerada
        t = pd.read_csv(self.csv_file_name + ".csv",  delimiter="," , nrows = self.numLin, skiprows = self.skipLinhas, encoding='latin-1')
        t['LOCAL'] = t.iloc[:,0] + ' ' + t.iloc[:,1]
        t.drop(t.columns[[1]], axis = 1, inplace = True)
        
        return t
    
    def tabela_sem_indices(self):
        # Função para gerar a tabela sem a primeira coluna de localidade e modalidade
        t = pd.read_csv(self.csv_file_name + ".csv",  delimiter="," , nrows = self.numLin, skiprows = self.skipLinhas, encoding='latin-1')
        t.rename(columns = {'MODALIDADE DE\rVENDA':'MODALIDADE DE VENDA'}, inplace = True)
        t.drop(t.columns[[0,1]], axis = 1, inplace = True)
        
        return t

#-----------------------------------------------------------------------------------------------------------------------------------
class JuntaTabelas:
    """Classe que junta as tabelas do pandas e a rotaciona em 90º"""
    def __init__(self,a,b,c,d,e,f,g,h):
        # Construtor que recebe as tabelas como parâmetros
        self.a = a
        self.b = b
        self.c = c
        self.d = d
        self.e = e
        self.f = f
        self.g = g
        self.h = h
        
    def tabela_final(self):
        # Função que concatena as tabelas
        tf = pd.concat([self.a, self.b, self.c, self.d, self.e, self.f, self.g, self.h], axis = 1)
        tf_t = tf.T
        tf_t = tf_t.set_axis(tf_t.iloc[0, :], axis=1)
        tf_t.drop(tf_t.index[0], axis=0, inplace=True)
        idx = list(tf_t.index)
        idx = [v.replace('.', '/') for v in idx]
        tf_t.index = idx

        for i in range(1,len(tf_t)):
            data_inicio = datetime.strptime(tf_t.index[i-1], '%d/%m/%Y')
            data_fim = datetime.strptime(tf_t.index[i], '%d/%m/%Y')
            delta_dias = data_fim - data_inicio
            delta_dias = delta_dias.days
            nova_linha = list(tf_t.iloc[i-1,:]) 
            
            for d in range(1, delta_dias):
                incremento  = data_inicio + timedelta(days=d)
                data_incremento = incremento.strftime('%d/%m/%Y')
                tf_t.loc[data_incremento] = nova_linha
          
        return tf_t

#-----------------------------------------------------------------------------------------------------------------------------------
class ConverterUnidadeMedida:
    """Classe para converter as unidades de medida da tabela gerada.
    Inicialmente muda a notação do numeral de PTG(x.xxx,x) para ENG(x,xxx.x) 
    """
    locale.setlocale(locale.LC_NUMERIC, 'en_DK.UTF-8')
    def __init__(self, tabela):
        self.tabelao = tabelao

    def converte(self, divisor):
        # Método para percorrer as colunas do tabelao, muda o formato do numeral e divide por 980
        tabelao.fillna('0,0', inplace=True)
        for j in range(len(tabelao.columns)):
            lista = tabelao.iloc[:, j].values
            lista = [locale.atof(x)/divisor for x in lista]
            tabelao[tabelao.columns[j]] = lista
            
        tabelao.replace([float(0)], '', inplace = True)
        
        return tabelao
    
    def diesel_s(self):
        tabelao.fillna('0,0', inplace=True)
        for j in range(len(tabelao.columns)):
            lista = tabelao.iloc[:, j].values
            lista = [locale.atof(x)/1000 for x in lista]
            tabelao[tabelao.columns[j]] = lista
            
        tabelao.replace([float(0)], '', inplace = True)
        
        return tabelao
    
#-----------------------------------------------------------------------------------------------------------------------------------
class HtmlPage:
    '''Recebe uma dataframe, converte para html e formata o mesmo'''
    def html_file(self,df, file_name):
        # converte a df para html
        html_file = df.to_html()
        index_file = open('index_' + file_name + '.html', 'w')
        index_file.write(html_file)
        index_file.close()
        # Formata o arquivo com código css
        file = open('index_' + file_name + '.html', 'a')
        text = '<link rel="stylesheet" href="css/styles.css">'
        file.write(text)
        file.close()

    
if __name__ == "__main__":
    # Execucação do script p/ o óleo combustível A1
    pdf = GerarPdf("https://precos.petrobras.com.br/documents/77785/82038/Tabelas+de+Pre%C3%A7os+-+OC+-+25-01-23.pdf/\
6842ff74-2eea-3a71-290e-660aa6eb2570?t=1674672690411",
                   "oleoCombustivel"
        )
    
    pdf.baixa_pdf_csv()
    
    a = GerarTabelas(16,0, "oleoCombustivel").tabela()
    b = GerarTabelas(16,17, "oleoCombustivel").tabela_sem_indices()
    c = GerarTabelas(16,34, "oleoCombustivel").tabela_sem_indices()
    d = GerarTabelas(16,51, "oleoCombustivel").tabela_sem_indices()
    e = GerarTabelas(16,68, "oleoCombustivel").tabela_sem_indices()
    f = GerarTabelas(16,85, "oleoCombustivel").tabela_sem_indices()
    g = GerarTabelas(16,102, "oleoCombustivel").tabela_sem_indices()
    h = GerarTabelas(16,119, "oleoCombustivel").tabela_sem_indices()
    tabelao = JuntaTabelas(a,b,c,d,e,f,g,h).tabela_final()
    saum = ConverterUnidadeMedida(tabelao).converte(980)
    
    #convertendo dataframe para html e escrevendo no arquivo index.html
    HtmlPage().html_file(saum, 'sa1')

    os.remove("oleoCombustivel.pdf")
    os.remove("oleoCombustivel.csv")
    # ------------------------------------------------------------------------------------------------------------------------
    
    # Execução do script p/ o diesel S500 e S10
    pdf = GerarPdf("https://precos.petrobras.com.br/documents/77785/82029/Tabelas+de+Pre%C3%A7os+-+Diesel+S500+e+S10+01-23.pdf/\
6227f015-3ba6-2a50-0caf-071511053bfe?t=1672661792975",
                   "diesel"
        )
    
    pdf.baixa_pdf_csv()

    s500a = GerarTabelas(77,0, "diesel").tabela()
    s500b = GerarTabelas(77,78, "diesel").tabela_sem_indices()
    s500c = GerarTabelas(77,156, "diesel").tabela_sem_indices()
    s500d = GerarTabelas(77,234, "diesel").tabela_sem_indices()
    s500e = GerarTabelas(77,312, "diesel").tabela_sem_indices()
    s500f = GerarTabelas(77,390, "diesel").tabela_sem_indices()
    s500g = GerarTabelas(77,468, "diesel").tabela_sem_indices()
    tabelao = JuntaTabelas(s500a, s500b, s500c, s500d, s500e, s500f, s500g, s500g).tabela_final()
    tabelao.drop(tabelao.columns[[-1]], axis = 1, inplace = True)
    s500 = ConverterUnidadeMedida(tabelao).converte(1000)
    
    HtmlPage().html_file(s500, 's500')

    s10a = GerarTabelas(71,546, "diesel").tabela()
    s10b = GerarTabelas(71,618, "diesel").tabela_sem_indices()
    s10c = GerarTabelas(71,690, "diesel").tabela_sem_indices()
    s10d = GerarTabelas(71,762, "diesel").tabela_sem_indices()
    s10e = GerarTabelas(71,834, "diesel").tabela_sem_indices()
    s10f = GerarTabelas(71,906, "diesel").tabela_sem_indices()
    s10g = GerarTabelas(71,978, "diesel").tabela_sem_indices()
    tabelao = JuntaTabelas(s10a, s10b, s10c, s10d, s10e, s10f, s10g, s10g).tabela_final()
    tabelao.drop(tabelao.columns[[-1]], axis = 1, inplace = True)
    s10 = ConverterUnidadeMedida(tabelao).converte(1000)

    HtmlPage().html_file(s10, 's10')
    
    os.remove("diesel.pdf")
    os.remove("diesel.csv")

    # ------------------------------------------------------------------------------------------------------------------------


    
