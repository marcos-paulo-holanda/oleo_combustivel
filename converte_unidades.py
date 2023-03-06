import locale
import pandas as pd

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
