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
