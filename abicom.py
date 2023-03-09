import requests
import shutil
from datetime import datetime
from bs4 import BeautifulSoup as bs


def baixa_image_ppi():
    data_lanc = datetime.strftime(datetime.today(), "%d-%m-%Y")

    link = "https://abicom.com.br/ppi/ppi-"+ data_lanc +"/"

    req = requests.get(link)

    soup = bs(req.content, "html.parser")

    tags = soup.findAll('img')

    imgs_links = [tag['src'] for tag in tags ]

    ppi = requests.get(imgs_links[2]).content

    with open('ppi_image.jpeg', 'wb') as handler:
        handler.write(ppi)
    
    

from PIL import Image
import pytesseract



#text = pytesseract.image_to_string(Image.open('ppi_image.jpeg'))

#print(ocr_core('ppi_image.jpeg'))
