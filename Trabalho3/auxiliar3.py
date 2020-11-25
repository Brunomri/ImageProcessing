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

def histograma(img, ch = 0, bins = 256, lb = 0, ub = 256, titulo = "", rotulo_x = "", rotulo_y = ""):
    hist = cv.calcHist([img], [ch], None, [bins], [lb, ub])
    #print("Hist = {}".format(hist))
    fig = plt.figure()
    fig.canvas.set_window_title(titulo)
    plt.title(titulo, fontsize = 15)
    plt.xlabel(rotulo_x,fontsize=10)
    plt.ylabel(rotulo_y,fontsize=10)

    pix = (img.shape[0] * img.shape[1])
    preto = hist[0, 0].astype("int")
    print("Pixels pretos = {}".format(preto))
    print("Total de pixels = {}".format(pix))
    percent = (preto/pix).astype("float")
    print("% Preto = {}%\n".format(percent * 100))

    #plt.legend(hist, loc='upper left')
    plt.plot(hist)
    plt.show()

def otsu(img, inp):
    print("Aplicando limiarizacao global de Otsu")
    thr,res = cv.threshold(img,0,255,cv.THRESH_BINARY_INV+cv.THRESH_OTSU)
    print("Limiar = {}".format(thr))
    exibir("Otsu", res, "otsu_{}".format(inp), 0)
    histograma(res, titulo = "Otsu", rotulo_x = "Intensidade", rotulo_y = "Pixels")