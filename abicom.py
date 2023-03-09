import requests
import shutil
from datetime import datetime
from bs4 import BeautifulSoup as bs
from PIL import Image

def baixa_image_ppi():
    data_lanc = datetime.strftime(datetime.today(), "%d-%m-%Y")

    link = "https://abicom.com.br/ppi/ppi-"+ data_lanc +"/"

    req = requests.get(link)

    soup = bs(req.content, "html.parser")

    tags = soup.findAll('img')

    imgs_links = [tag['src'] for tag in tags ]

    ppi = requests.get(imgs_links[2]).content

    with open('ppi_image.png', 'wb') as handler:
        handler.write(ppi)
    




    image = Image.open("ppi_image.png")
    im_1 = image.convert('RGB')
    im_1.save("ppi_rgb.pdf")



