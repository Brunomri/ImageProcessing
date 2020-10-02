# Processamento de imagens
# Trabalho 0
# 1.1 Transformacao de intensidade

import cv2 as cv
import sys, auxiliar as a

def questao1(img):

    # a) Imagem original

    a.exibir("Original",img,"original1.png")

    # b) Negativo da imagem
    imgNeg = cv.bitwise_not(img)
    a.exibir("Negativo",imgNeg,"city1_1b.png")


    # c) Espelhamento vertical
    imgFlip = cv.flip(img,0)
    a.exibir("Espelhamento vertical",imgFlip,"city1_1c.png")


    # d) Imagem transformada
    rows,cols = img.shape
    g = img.copy()

    for i in range(rows):
        for j in range(cols):
            f = g[i,j]
            v = ((100*f)/255)+100
            g.itemset((i,j),v)

    a.exibir("Imagem transformada",g,"city1_1d.png")


    # e) Linhas pares invertidas
    h = img.copy()

    for p in range(rows):
        if p%2 == 0:
            r = h[p][::-1]
            h[p] = r

    a.exibir("Linhas pares invertidas",h,"city1_1e.png")

    # f) Reflexao de linhas
    i = img.copy()

    for p in range(rows//2):
        r = i[p]
        i[rows-p-1] = r

    a.exibir("Reflexao de linhas",i,"city1_1f.png") 

    cv.destroyAllWindows()