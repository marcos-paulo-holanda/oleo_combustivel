import tabula
import pandas as pd
from datetime import datetime, timedelta

df = tabula.read_pdf("oleoCombustivel" + ".pdf", pages=[1,2,3,4,5,6,7,8])

df = pd.concat(df[:8][:],axis =1)

'''
df[0]['LOCAL'] = df[0].iloc[:,0] + ' ' + df[0].iloc[:,1]
df[0].drop(df[0].columns[[1]], axis =1, inplace = True)

for i in range(1,8):
    df[i].rename(columns = {'MODALIDADE DE\rVENDA':'MODALIDADE DE VENDA'}, inplace = True)
    df[i].drop(df[i].columns[[0,1]], axis = 1, inplace = True)

tb = pd.concat([df[0], df[1], df[2], df[3], df[4], df[5], df[6], df[7]], axis = 1)

#tbb = pd.concat(df[:num_pags + 1 ][:], axis = 1)




rename_columns = []
for v in tb.columns:
    rename_columns.append(v.replace('.','/'))
tb.columns = rename_columns

delta_days = []
for i in range(1, len(tb.columns) - 1):
    delta = datetime.strptime(tb.columns[i+1], "%d/%m/%Y") - datetime.strptime(tb.columns[i], "%d/%m/%Y")
    delta_days.append(delta.days)

col_name_copy = list(tb.columns[1:-1]) #backup dos nomes das colunas da tb

datas_range = dict(zip(col_name_copy, delta_days))

for key in datas_range:
    n_insertion = datas_range[key]
    for n in range(1, n_insertion):

        tb.insert(
            tb.columns.get_loc(key) + n,
            datetime.strftime((datetime.strptime(key, '%d/%m/%Y') + timedelta(days = n)), "%d/%m/%Y"),
            tb[key]
            )

tb = tb.T
tb = tb.set_axis(tb.iloc[0, :], axis=1)
tb.drop(tb.index[0], axis=0, inplace=True)

'''
