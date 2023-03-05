from scrapy import Selector
import requests
import time

url = "https://ream.com.br/o-que-fazemos/#PRECOS"


#url = "https://sisdipre.ream.com.brlancamentos/2/export/excel/?produto=2&data__year=2023&data_month=1&"

r = requests.get(url)

html = r.content

sel = Selector(text=html)


