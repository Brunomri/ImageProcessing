# Processamento de imagens
# Trabalho 0
# 1.4 Mosaico

import cv2 as cv
import numpy as np
import sys, auxiliar as a

def questao4(img):

    # a) Imagem original
    a.exibir("Original",img,"original4.png")

    # b) ordem dos blocos

    # Dicionario t armazena os blocos da imagem original
    t = {}

    # Dicionario p armazena a posicao de cada bloco na nova imagem
    p = {1:6,2:11,3:13,4:3,
         5:8,6:16,7:1,8:9,
         9:12,10:14,11:2,12:7,
         13:4,14:15,15:10,16:5}

    # Loop que extrai cada quadrado da imagem original em armazena em t
    linha = 1
    for i in range(4):
        for j in range(4):
            t[i + j + linha] = img[i*128:(i+1)*128,j*128:(j+1)*128]
        linha += 3

    # Loop que cria uma lista onde cada bloco aparece na ordem que deve ser
    # inserido na nova imagem
    blocos = []
    for i in t:
        dest = p.get(i)
        bloco = t.get(dest)
        blocos.append(bloco)

    # Loop que percorre a lista de blocos agrupando 2 a 2 
    # os 4 blocos que formam uma linha
    linhas = []
    for b in range(0,15,4):
        temp1 = np.hstack((blocos[b],blocos[b+1]))
        temp2 = np.hstack((blocos[b+2],blocos[b+3]))
        linha = np.hstack((temp1,temp2))
        linhas.append(linha)

    # Agrupa as 4 linhas formando a nova imagem completa
    temp1 = np.vstack((linhas[0],linhas[1]))
    temp2 = np.vstack((linhas[2],linhas[3]))
    res = np.vstack((temp1,temp2))

    a.exibir("Mosaico",res,"baboon1_4d.png")

    cv.destroyAllWindows()