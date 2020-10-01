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

def questao1(img):

    # 1.1 Transformacao de intensidade
    # a) Imagem original

    cv.imshow("Original", img)
    k = cv.waitKey(0) & 0xFF

    # cv.destroyWindow("Original")


    # b) Negativo da imagem
    imgNeg = cv.bitwise_not(img)
    exibir("Negativo",imgNeg,"city1_1b.png")


    # c) Espelhamento vertical
    imgFlip = cv.flip(img,0)
    exibir("Espelhamento vertical",imgFlip,"city1_1c.png")


    # d) Imagem transformada
    print(img[0,0])
    print(img.shape)

    rows,cols = img.shape
    g = img.copy()

    for i in range(rows):
        for j in range(cols):
            f = g[i,j]
            v = ((100*f)/255)+100
            g.itemset((i,j),v)

    exibir("Imagem transformada",g,"city1_1d.png")


    # e) Linhas pares invertidas
    h = img.copy()

    for p in range(rows):
        if p%2 == 0:
            r = h[p][::-1]
            h[p] = r

    exibir("Linhas pares invertidas",h,"city1_1e.png")

    # f) Reflexao de linhas
    i = img.copy()

    for p in range(rows//2):
        r = i[p]
        i[rows-p-1] = r

    exibir("Reflexao de linhas",i,"city1_1f.png") 

    cv.destroyAllWindows()