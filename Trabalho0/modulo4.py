# Processamento de imagens
# Trabalho 0
# 1.4 Mosaico

import cv2 as cv
import numpy as np
import sys, auxiliar as a

def questao4(img):

    # a) Imagem original
    a.exibir("Original",img,"original2.png")

    # b) ordem dos blocos
    t1 = img[0:128,0:128]
    #print(t1.shape)
    #a.exibir("Recorte",t1,"teste.png")

    t2 = img[0:128,128:256]
    #print(t2.shape)
    #a.exibir("Recorte",t2,"teste.png")

    t3 = np.concatenate((t1,t2),axis=1)
    #a.exibir("Conc",t3,"teste.png")

    # Dicionario t armazena os blocos da imagem original
    t = {}
    r = np.full((img.shape[0],img.shape[1]), 0, np.uint8)

    p = {1:6,2:11,3:13,4:3,
         5:8,6:16,7:1,8:9,
         9:12,10:14,11:2,12:7,
         13:4,14:15,15:10,16:5}

    #print(p.values())

    contador = 0
    linha = 1
    for i in range(4):
        for j in range(4):
            t[i + j + linha] = img[i*128:(i+1)*128,j*128:(j+1)*128]
            #a.exibir("Recorte",t[(i+1)*(j+1)],"teste.png")
            contador += 1
            #print("T: ",t.keys())
            #dest = p.get((i+1)*(j+1))
            #bloco = t.get(dest)
        linha += 3

    print(contador)
    #print(p[2])

    pos_x = 0
    pos_y = 0
    for x in range(r.shape[0]):
        pos_x = x // 128
        for y in range(r.shape[1]):
            pos_y = y // 128
            pos = pos_x + pos_y + 1
            bloco = p[pos]
            #print("\nBloco: ", bloco)
            #a.exibir("Bloco",t[bloco],"teste.png")
            for u in range((t[bloco]).shape[0]):
                for v in range((t[bloco]).shape[1]):
                    pixel = (t[bloco])[u,v]
                    r.itemset((x,y),pixel)

    a.exibir("Recorte",r,"teste.png")