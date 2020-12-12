# Funcoes auxiliares

import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt

# exibir: exibe a imagem em uma janela utilizando matplotlib imshow
def exibir(janela, img, saida, axis = "on"):
    print("Exibindo {}".format(saida))
    #cv.imshow(janela, img)
    fig = plt.figure()
    fig.canvas.set_window_title(janela)
    plt.axis(axis)
    plt.imshow(img)
    plt.show()

# convBin: Converte diversos tipos de variaveis para binario com 8 bits
def convBin(msg):
    if type(msg) == str:
        return ''.join([format(ord(i), "08b") for i in msg ])
    elif type(msg) == bytes or type(msg) == np.ndarray:
        return [format(i, "08b") for i in msg ]
    elif type(msg) == int or type(msg) == np.uint8:
        return format(msg, "08b")
    else:
        raise TypeError("Tipo nao suportado")

# codeMsg: Codifica a mensagem nos bits menos significativos de cada banda de cor
# de um pixel da imagem de entrada
def codeMsg(img, msg):

    # Calcula o numero maximo de bytes a codificar
    bytesNum = img.shape[0] * img.shape[1] * 3 // 8
    print("Maximum bytes to encode:", bytesNum)

    # Verifica se numero de bytes da mensagem cabe no numero de bytes
    # disponivel na imagem
    if len(msg) > bytesNum:
        raise ValueError("Nao ha bytes suficientes na imagem para codificar a mensagem \n{}\n que possui {} bytes em uma imagem que possui {}".format(msg, len(msg), bytesNum))
  
    # Adiciona a mensagem o delimitador de fim de cadeia
    msg += "#####"

    # Indice utilizado para percorre a mensagem
    indexMsg = 0
    # Converte mensagem para binario de 8 bits
    binMsg = convBin(msg)
    # Obtem o comprimento da mensagem
    lenMsg = len(binMsg)

    # Percorre os pixels de cada linha da imagem
    for values in img:
        for pixel in values:
            # Converte cada banda de cor de um pixel para binario de 8 bits
            r, g, b = convBin(pixel)
            # Modifica o bit menos significativo da imagem se ainda houve caracteres
            # a processar na mensagem
            if indexMsg < lenMsg:
                # Substitui bit menos significativo da banda
                # de cor vermelha do pixel por um bit da mensagem e
                # converte o novo valor para um inteiro decimal
                pixel[0] = int(r[:-1] + binMsg[indexMsg], 2)
                indexMsg += 1
            if indexMsg < lenMsg:
                # hide the data into least significant bit of green pixel
                pixel[1] = int(g[:-1] + binMsg[indexMsg], 2)
                indexMsg += 1
            if indexMsg < lenMsg:
                # hide the data into least significant bit of  blue pixel
                pixel[2] = int(b[:-1] + binMsg[indexMsg], 2)
                indexMsg += 1
            # if data is encoded, just break out of the loop
            if indexMsg >= lenMsg:
                break

    return img