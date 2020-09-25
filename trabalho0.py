# Processamento de imagens
# Trabalho 0

# Importar OpenCV, scikit-image, Numpy e Matplotlib
import cv2 as cv
import skimage
import numpy as np
from matplotlib import pyplot as plt
import sys

# print(cv.__version__)
# print(skimage.__version__)

# Funcoes auxiliares
# exibir: exibe a imagem em uma janela e a salva em um arquivo se o usuario entrar "s", senão
# apenas continua a execucao
def exibir(janela,img,saida):
    cv.imshow(janela, img)
    k = cv.waitKey(0) & 0xFF

    if k == ord("s"):
        cv.imwrite(saida, img)

    cv.destroyWindow(janela)


# 1.1 Transformacao de intensidade
# a) Imagem original
img = cv.imread("city.png", 0)

if img is None:
    sys.exit("Could not read the image.")

cv.imshow("Original", img)
k = cv.waitKey(0) & 0xFF

# cv.destroyWindow("Original")

# b) Negativo da imagem
imgNeg = cv.bitwise_not(img)
exibir("Negativo",imgNeg,"city1_1b")

# c) Espelhamento vertical
imgFlip = cv.flip(img,0)
exibir("Espelhamento vertical",imgFlip,"city1_1c")

# d) Imagem transformada
print(img[0,0])
print(img.shape)

rows,cols = img.shape
g = img

for i in range(rows):
    for j in range(cols):
        f = img[i,j]
        v = ((100*f)/255)+100
        g.itemset((i,j),v)

exibir("Imagem transformada",g,"city1_1c")

# e) Linhas pares invertidas

cv.destroyAllWindows()