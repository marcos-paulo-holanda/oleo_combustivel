import cv2
import numpy as np
import matplotlib.pyplot as plt

def identificar_regiao_vermelha(imagem):
    # converte a imagem para o espaço de cor HSV
    hsv = cv2.cvtColor(imagem, cv2.COLOR_BGR2HSV)

    # define o intervalo de valores para a cor vermelha
    lower_red = np.array([0,50,50])
    upper_red = np.array([10,255,255])
    mask1 = cv2.inRange(hsv, lower_red, upper_red)

    lower_red = np.array([170,50,50])
    upper_red = np.array([180,255,255])
    mask2 = cv2.inRange(hsv, lower_red, upper_red)

    # combina as duas máscaras
    mask = cv2.bitwise_or(mask1, mask2)

    # aplica um filtro para remover ruídos da imagem
    kernel = np.ones((5,5),np.uint8)
    opening = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)

    # encontra os contornos na imagem filtrada
    contours, hierarchy = cv2.findContours(opening, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # desenha os contornos na imagem original
    imagem_contornos = cv2.drawContours(imagem.copy(), contours, -1, (0,0,255), 3)

    return imagem_contornos

def identificar_regiao_vermelha2(imagem):
    # converte a imagem para o espaço de cor HSV
    hsv = cv2.cvtColor(imagem, cv2.COLOR_BGR2HSV)

    # define o intervalo de valores para a cor vermelha
    lower_red = np.array([0,50,50])
    upper_red = np.array([10,255,255])
    mask1 = cv2.inRange(hsv, lower_red, upper_red)

    lower_red = np.array([170,50,50])
    upper_red = np.array([180,255,255])
    mask2 = cv2.inRange(hsv, lower_red, upper_red)

    # combina as duas máscaras
    mask = cv2.bitwise_or(mask1, mask2)

    # aplica um filtro para remover ruídos da imagem
    kernel = np.ones((5,5),np.uint8)
    opening = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)

    # encontra os contornos na imagem filtrada
    contours, hierarchy = cv2.findContours(opening, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # cria uma máscara com as regiões identificadas em vermelho
    mascara_vermelha = np.zeros(imagem.shape[:2], dtype="uint8")
    cv2.drawContours(mascara_vermelha, contours, -1, 255, -1)

    # aplica a máscara na imagem original
    imagem_identificada = cv2.bitwise_and(imagem, imagem, mask=mascara_vermelha)

    return imagem_identificada

# carrega a imagem
imagem = cv2.imread("ppi_image.png")

# identifica a região vermelha na imagem
imagem_identificada = identificar_regiao_vermelha2(imagem)

# exibe a imagem com a região identificada
plt.imshow(cv2.cvtColor(imagem_identificada, cv2.COLOR_BGR2RGB))
plt.show()

    
