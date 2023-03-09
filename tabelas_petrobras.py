import pandas as pd
import tabula
import locale
from datetime import datetime, timedelta, date
from warnings import simplefilter
simplefilter(action="ignore", category=pd.errors.PerformanceWarning)

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
                
        # Verifica se a última data de lançamento é diferente a data atual de rodagem do programa
        if datetime.strptime(list(tb.iloc[:,-1:].columns)[0], "%d/%m/%Y") != date.today():
            n_insertion  = abs((datetime.today() - datetime.strptime(list(tb.iloc[:,-1:].columns)[0], "%d/%m/%Y")).days)
            for n in range(n_insertion):
                series = tb.iloc[ : ,-1]
                series.rename(datetime.strftime(datetime.strptime(tb.iloc[ : ,-1].name, "%d/%m/%Y") + timedelta(days = 1), "%d/%m/%Y"), inplace = True)
                tb = pd.concat([tb, series], axis = 1 )

        # Transpoe a tabela para qual as datas se tornam os indices da tabela
        tb = tb.T
        tb = tb.set_axis(tb.iloc[0, :], axis=1)
        tb.drop(tb.index[0], axis=0, inplace=True)
        
        return tb
