'''
Script para baixar pdf com preços atualizados do óleo combustível A1 e exportar dados para planilha excel
'''
import requests, os 
import tabula as tb, pandas as pd

oc = "https://precos.petrobras.com.br/documents/77785/82038/Tabelas+de+Pre%C3%A7os+-+OC+-+25-01-23.pdf/6842ff74-2eea-3a71-290e-660aa6eb2570?t=1674672690411"

response = requests.get(oc)
pdf = open("oleoCombustivel"+".pdf", 'wb')
pdf.write(response.content)
pdf.close() 

df = tb.read_pdf("oleoCombustivel.pdf", pages="all")
tb.convert_into("oleoCombustivel.pdf", "oleoCombustivel.csv", output_format = "csv", pages = "all")

os.remove("oleoCombustivel.pdf")

#----------------------------------------------------------------------------------------------------------------

a1a = pd.read_csv("oleoCombustivel.csv",  delimiter="," , nrows = 16, skiprows = 0, encoding='latin-1')
a1a.rename(columns = {'MODALIDADE DE\rVENDA':'MODALIDADE DE VENDA'}, inplace = True)

a1b = pd.read_csv("oleoCombustivel.csv",  delimiter="," , nrows = 16, skiprows = list(range(17)), encoding='latin-1')
a1b.rename(columns = {'MODALIDADE DE\rVENDA':'MODALIDADE DE VENDA'}, inplace = True)
a1b.drop(a1b.columns[[0,1]], axis = 1, inplace = True)

a1c = pd.read_csv("oleoCombustivel.csv",  delimiter="," , nrows = 16, skiprows = list(range(34)), encoding='latin-1')
a1c.rename(columns = {'MODALIDADE DE\rVENDA':'MODALIDADE DE VENDA'}, inplace = True)
a1c.drop(a1c.columns[[0,1]], axis = 1, inplace = True)

a1d = pd.read_csv("oleoCombustivel.csv",  delimiter="," , nrows = 16, skiprows = list(range(51)), encoding='latin-1')
a1d.rename(columns = {'MODALIDADE DE\rVENDA':'MODALIDADE DE VENDA'}, inplace = True)
a1d.drop(a1d.columns[[0,1]], axis = 1, inplace = True)

a1e = pd.read_csv("oleoCombustivel.csv",  delimiter="," , nrows = 16, skiprows = list(range(68)), encoding='latin-1')
a1e.rename(columns = {'MODALIDADE DE\rVENDA':'MODALIDADE DE VENDA'}, inplace = True)
a1e.drop(a1e.columns[[0,1]], axis = 1, inplace = True)

a1f = pd.read_csv("oleoCombustivel.csv",  delimiter="," , nrows = 16, skiprows = list(range(85)), encoding='latin-1')
a1f.rename(columns = {'MODALIDADE DE\rVENDA':'MODALIDADE DE VENDA'}, inplace = True)
a1f.drop(a1f.columns[[0,1]], axis = 1, inplace = True)

a1g = pd.read_csv("oleoCombustivel.csv",  delimiter="," , nrows = 16, skiprows = list(range(102)), encoding='latin-1')
a1g.rename(columns = {'MODALIDADE DE\rVENDA':'MODALIDADE DE VENDA'}, inplace = True)
a1g.drop(a1g.columns[[0,1]], axis = 1, inplace = True)

a1h = pd.read_csv("oleoCombustivel.csv",  delimiter="," , nrows = 16, skiprows = list(range(119)), encoding='latin-1')
a1h.rename(columns = {'MODALIDADE DE\rVENDA':'MODALIDADE DE VENDA'}, inplace = True)
a1h.drop(a1h.columns[[0,1]], axis = 1, inplace = True)

a1 = pd.concat([a1a, a1b, a1c, a1d, a1e, a1f, a1g, a1h], axis = 1)
a1_t = a1.T
a1_t = a1_t.set_axis(a1_t.iloc[0, :], axis=1)
a1_t.drop(a1_t.index[0], axis=0, inplace=True)

a1_t.to_excel(r'oleoCombustivelA1.xlsx', sheet_name='oleoA1_transposta', index=True)
#a1.to_excel(r'oleoCombustivelA1.xlsx', sheet_name='oleoA1', index=True)

#----------------------------------------------------------------------------------------------------------------
os.remove("oleoCombustivel.csv")
