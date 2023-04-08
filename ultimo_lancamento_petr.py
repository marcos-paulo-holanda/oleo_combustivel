import requests
import os
import tabula
import locale
from datetime import datetime, timedelta, date

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

class Tabela:
    """Classe para gerar tabelas no pandas através da leitura dos dados do arquivo pdf baixado"""
    def __init__(self, file_name):
        self.file_name = file_name        
        
    def concat_pdf_tables(self, pg_start, pg_end):
        '''Concatena as tabelas das páginas do arquivo pdf'''
        df = tabula.read_pdf(self.file_name + ".pdf", pages=[x for x in range(pg_start, pg_end + 1)])

        df = pd.concat(df[:pg_end +1][:], axis = 1)
        df['LOCAL'] = df.iloc[:,0] + ' ' + df.iloc[:,1]
        df.drop(df.columns[1], axis =1, inplace = True)

        df = df.T.drop_duplicates().T

        return df


if __name__ == "__main__":
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
    
    s10 = Tabela("diesel").concat_pdf_tables(14, 15)
    print(s10)