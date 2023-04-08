import requests
import cv2
import os
from datetime import datetime
from bs4 import BeautifulSoup as bs
from PIL import Image
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

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

    
    img = Image.open('ppi_image.jpeg')
    box = (860, 87, 985, 105)
    img2 = img.crop(box)
    img2.save('cropped.jpeg')
    '''
    i = Image.open('cropped.jpeg')
    
    text = pytesseract.image_to_string(i)
    ppi_value=text[:6]
    ppi_value = ppi_value.replace(',','.')

    os.remove('ppi_image.jpeg')
    os.remove('cropped.jpeg')
    return ppi_value
    '''

    img = mpimg.imread('ppi_image.jpeg')
    imgplot = plt.imshow(img)
    plt.show()
    r = input('Digite o valor do PPI: ')
    os.remove('ppi_image.jpeg')
    
    return None


