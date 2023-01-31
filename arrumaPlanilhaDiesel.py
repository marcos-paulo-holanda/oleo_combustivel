'''
Script para baixar pdf com preços atualizado do diesel S500 e S10 e export os dados para planilha excel 
'''

import requests, os 
import tabula as tb, pandas as pd

#----------------------------------------------------------------------------------------------------------------
diesel = "https://precos.petrobras.com.br/documents/77785/82029/Tabelas+de+Pre%C3%A7os+-+Diesel+S500+e+S10+01-23.pdf/6227f015-3ba6-2a50-0caf-071511053bfe?t=1672661792975"
response = requests.get(diesel)
pdf = open("diesel"+".pdf", 'wb')
pdf.write(response.content)
pdf.close()

df = tb.read_pdf("diesel.pdf", pages="all")
tb.convert_into("diesel.pdf", "diesel.csv", output_format = "csv", pages = "all")

os.remove("diesel.pdf")
#----------------------------------------------------------------------------------------------------------------

s500a = pd.read_csv("diesel.csv",  delimiter="," , nrows = 77, skiprows = 0, encoding='latin-1')
s500a.rename(columns = {'MODALIDADE\rDE VENDA':'MODALIDADE DE VENDA'}, inplace = True)

s500b = pd.read_csv("diesel.csv",  delimiter="," , nrows = 77, skiprows = list(range(78)), encoding='latin-1')
s500b.rename(columns = {'MODALIDADE\rDE VENDA':'MODALIDADE DE VENDA'}, inplace = True)
s500b.drop(s500b.columns[[0,1]], axis = 1, inplace = True)

s500c = pd.read_csv("diesel.csv",  delimiter="," , nrows = 77, skiprows = list(range(156)), encoding='latin-1')
s500c.rename(columns = {'MODALIDADE\rDE VENDA':'MODALIDADE DE VENDA'}, inplace = True)
s500c.drop(s500c.columns[[0,1]], axis = 1, inplace = True)

s500d = pd.read_csv("diesel.csv",  delimiter="," , nrows = 77, skiprows = list(range(234)), encoding='latin-1')
s500d.rename(columns = {'MODALIDADE\rDE VENDA':'MODALIDADE DE VENDA'}, inplace = True)
s500d.drop(s500d.columns[[0,1]], axis = 1, inplace = True)

s500e = pd.read_csv("diesel.csv",  delimiter="," , nrows = 77, skiprows = list(range(312)), encoding='latin-1')
s500e.rename(columns = {'MODALIDADE\rDE VENDA':'MODALIDADE DE VENDA'}, inplace = True)
s500e.drop(s500e.columns[[0,1]], axis = 1, inplace = True)

s500f = pd.read_csv("diesel.csv",  delimiter="," , nrows = 77, skiprows = list(range(390)), encoding='latin-1')
s500f.rename(columns = {'MODALIDADE\rDE VENDA':'MODALIDADE DE VENDA'}, inplace = True)
s500f.drop(s500f.columns[[0,1]], axis = 1, inplace = True)

s500g = pd.read_csv("diesel.csv",  delimiter="," , nrows = 77, skiprows = list(range(468)), encoding='latin-1')
s500g.rename(columns = {'MODALIDADE\rDE VENDA':'MODALIDADE DE VENDA'}, inplace = True)
s500g.drop(s500g.columns[[0,1]], axis = 1, inplace = True)

s500 = pd.concat([s500a, s500b, s500c, s500d, s500e, s500f, s500g], axis = 1)

s500_t = s500.T
s500_t = s500_t.set_axis(s500_t.iloc[0, :], axis=1)
s500_t.drop(s500_t.index[0], axis=0, inplace=True)

##datas = [x for x in s500_t.index.values[1:]]
##datas.insert(0,'MODALIDADE DE VENDA')
##s500_t.insert(loc=0,column='LOCAL',value = datas)

#s500.to_excel(r's500.xlsx', sheet_name='S500', index=False)
s500_t.to_excel(r's500_t.xlsx', sheet_name='S500_transposta', index=True)

#----------------------------------------------------------------------------------------------------------------
s10a = pd.read_csv("diesel.csv",  delimiter="," , nrows = 71, skiprows = list(range(546)), encoding='latin-1')
s10a.rename(columns = {'MODALIDADE\rDE VENDA':'MODALIDADE DE VENDA'}, inplace = True)

s10b = pd.read_csv("diesel.csv",  delimiter="," , nrows = 71, skiprows = list(range(618)), encoding='latin-1')
s10b.rename(columns = {'MODALIDADE\rDE VENDA':'MODALIDADE DE VENDA'}, inplace = True)
s10b.drop(s10b.columns[[0,1]], axis = 1, inplace = True)

s10c = pd.read_csv("diesel.csv",  delimiter="," , nrows = 71, skiprows = list(range(690)), encoding='latin-1')
s10c.rename(columns = {'MODALIDADE\rDE VENDA':'MODALIDADE DE VENDA'}, inplace = True)
s10c.drop(s10c.columns[[0,1]], axis = 1, inplace = True)

s10d = pd.read_csv("diesel.csv",  delimiter="," , nrows = 71, skiprows = list(range(762)), encoding='latin-1')
s10d.rename(columns = {'MODALIDADE\rDE VENDA':'MODALIDADE DE VENDA'}, inplace = True)
s10d.drop(s10d.columns[[0,1]], axis = 1, inplace = True)

s10e = pd.read_csv("diesel.csv",  delimiter="," , nrows = 71, skiprows = list(range(834)), encoding='latin-1')
s10e.rename(columns = {'MODALIDADE\rDE VENDA':'MODALIDADE DE VENDA'}, inplace = True)
s10e.drop(s10e.columns[[0,1]], axis = 1, inplace = True)

s10f = pd.read_csv("diesel.csv",  delimiter="," , nrows = 71, skiprows = list(range(906)), encoding='latin-1')
s10f.rename(columns = {'MODALIDADE\rDE VENDA':'MODALIDADE DE VENDA'}, inplace = True)
s10f.drop(s10f.columns[[0,1]], axis = 1, inplace = True)

s10g = pd.read_csv("diesel.csv",  delimiter="," , nrows = 71, skiprows = list(range(978)), encoding='latin-1')
s10g.rename(columns = {'MODALIDADE\rDE VENDA':'MODALIDADE DE VENDA'}, inplace = True)
s10g.drop(s10g.columns[[0,1]], axis = 1, inplace = True)

s10 = pd.concat([s10a, s10b, s10c, s10d, s10e, s10f, s10g], axis = 1)
s10_t = s10.T
s10_t = s10_t.set_axis(s10_t.iloc[0, :], axis=1)
s10_t.drop(s10_t.index[0], axis=0, inplace=True)

##datas = [x for x in s10_t.index.values[1:]]
##datas.insert(0,'MODALIDADE DE VENDA')
##s10_t.insert(loc=0,column='LOCAL',value = datas)

#s10.to_excel(r's10.xlsx', sheet_name='S10', index=False)
s10_t.to_excel(r's10_t.xlsx', sheet_name='S10_transposta', index=True)

#----------------------------------------------------------------------------------------------------------------
os.remove("diesel.csv")
