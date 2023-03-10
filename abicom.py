import requests
import os
from datetime import datetime
from bs4 import BeautifulSoup as bs
import matplotlib.pyplot as plt
import matplotlib.image as img
from PIL import Image
import tabula
import pytesseract
import cv2

def abicom_ppi_value():
    
    data_lanc = datetime.strftime(datetime.today(), "%d-%m-%Y")

    link = "https://abicom.com.br/ppi/ppi-"+ data_lanc +"/"

    req = requests.get(link)

    soup = bs(req.content, "html.parser")

    tags = soup.findAll('img')

    imgs_links = [tag['src'] for tag in tags ]

    ppi = requests.get(imgs_links[2]).content

    with open('ppi_image.jpeg', 'wb') as handler:
        handler.write(ppi)


    image = img.imread('ppi_image.jpeg')
    #plt.imshow(image)
    #plt.show()

    img = Image.open('ppi_image.jpeg')

    box = (860, 87, 999, 113)
    img2 = img.crop(box)
    #img2.show()
    #img2 = img2.convert('RGB')
    #img2.save('ppi_image_cropped.pdf')

    #df = tabula.read_pdf('ppi_image_cropped.pdf', pages='all')
