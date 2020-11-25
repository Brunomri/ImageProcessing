# Funcoes auxiliares

import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt

# exibir: exibe a imagem em uma janela e a salva em um arquivo se o usuario entrar "s", senão
# apenas continua a execucao
def exibir(janela,img,saida,close):
    print("Exibindo {}".format(saida))
    cv.imshow(janela, img)
    k = cv.waitKey(0) & 0xFF

    if k == ord("s"):
        print("Gerando arquivo {}".format(saida))
        cv.imwrite(saida, img)

    print()

    # Parametro close == 1 fecha apenas a janela selecionada
    # Parametro close == 2 fecha todas as janelas
    if close == 1:
        cv.destroyWindow(janela)
    elif close == 2:
        cv.destroyAllWindows()
    else:
        return

def histograma(img, titulo, legenda_x, legenda_y):
    hist = cv.calcHist([img], [0], None, [256], [0, 256])
    fig = plt.figure()
    fig.canvas.set_window_title(titulo)
    plt.title(titulo, fontsize = 15)
    plt.xlabel(legenda_x,fontsize=10)
    plt.ylabel(legenda_y,fontsize=10)
    plt.plot(hist)
    plt.show()
