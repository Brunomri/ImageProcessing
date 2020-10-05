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
    #r = np.full((4,4), 0, np.uint8)

    p = {1:6,2:11,3:13,4:3,
         5:8,6:16,7:1,8:9,
         9:12,10:14,11:2,12:7,
         13:4,14:15,15:10,16:5}

    #print("Matriz r: ", r)

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

    blocos = []
    for i in t:
        print("i: ",i)
        #a.exibir("Recorte",t[i],"teste.png")
        dest = p.get(i)
        print("Destino: ",dest)
        bloco = t.get(dest)
        #a.exibir("Recorte",bloco,"teste.png")
        blocos.append(bloco)

    print("No de blocos: ", len(blocos))

    #teste = np.hstack((blocos[1],blocos[2]))
    #a.exibir("Recorte",teste,"teste.png")

    linhas = []
    for b in range(0,15,4):
        temp1 = np.hstack((blocos[b],blocos[b+1]))
        temp2 = np.hstack((blocos[b+2],blocos[b+3]))
        linha = np.hstack((temp1,temp2))
        linhas.append(linha)
        #a.exibir("Linhas",linha,"teste.png")

    temp1 = np.vstack((linhas[0],linhas[1]))
    temp2 = np.vstack((linhas[2],linhas[3]))
    res = np.vstack((temp1,temp2))

    #a.exibir("Recorte",l,"teste.png")
    a.exibir("Recorte",res,"teste.png")

    #print(contador)
    #print(p[2])

    #a.exibir("Recorte",r,"teste.png")