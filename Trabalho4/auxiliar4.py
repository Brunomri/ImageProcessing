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