# Funcoes auxiliares

import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt
from skimage.util.shape import view_as_windows

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

# histograma: calcula e exibe o histograma da imagem. O percentual de pixels preto é informado no console.
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

# otsu: aplica limiarizacao global de otsu em uma imagem de entrada, exibindo a imagem
# resultante e seu histograma
def otsu(img, inp):
    print("Aplicando limiarizacao global de Otsu em {}".format(inp))
    thr,res = cv.threshold(img, 0, 255, cv.THRESH_BINARY_INV+cv.THRESH_OTSU)
    print("Limiar = {}".format(thr))
    exibir("Otsu T = {}".format(thr), res, "otsu_t{}_{}".format(thr, inp), 0)
    histograma(res, titulo = "Otsu T = {}".format(thr), rotulo_x = "Intensidade", rotulo_y = "Pixels")

# get_bernsen_thr: retorna o limiar de Bernsen para cada pixel de uma imagem de entrada img de acordo
# com o tamanho da janela e limiar de contraste de regiao fornecidos
def get_bernsen_thr(img, t_janela = 15, ctr_thr = 30):

    thr = np.zeros(img.shape, np.uint8)

    # Tratamento de bordas com padding em funcao do tamanho da janela
    hw_size = t_janela // 2
    borda_img = np.ones((img.shape[0] + t_janela - 1,
                          img.shape[1] + t_janela - 1)) * np.nan
    borda_img[hw_size: -hw_size,
               hw_size: -hw_size] = img

    # Obtem janelas do tamanho especificado
    janelas = view_as_windows(borda_img, (t_janela, t_janela))

    # Calcula o valor minimo e maximo em cada janela
    minimos = np.nanmin(janelas, axis=(2, 3))
    maximos = np.nanmax(janelas, axis=(2, 3))

    # Calcula contrastes e valores medios
    ctr = maximos - minimos
    medios = (maximos + minimos) / 2

    # Obtem valores de limiar para cada pixel
    thr[ctr <= ctr_thr] = 128
    thr[ctr > ctr_thr] = medios[ctr > ctr_thr]

    return thr

# bernsen: aplica limiarizacao local de Bernsen com tamanho de janela e limiar de contraste 
# de regiao fornecidos, exibindo a imagem resultante e seu histograma
def bernsen(img, inp, t_janela = 15, ctr_thr = 30, wp_val = 255):
    print("Aplicando limiarizacao local de Bensen em {}".format(inp))
    print("Tamanho da janela = {} x {}".format(t_janela, t_janela))
    thr = get_bernsen_thr(img, t_janela, ctr_thr)
    print("Limiares = \n{}".format(thr))
    res = ((img < thr) * wp_val).astype(np.uint8)
    exibir("Bernsen", res, "bernsen_w{}_{}".format(t_janela, inp), 0)
    histograma(res, titulo = "Bernsen", rotulo_x = "Intensidade", rotulo_y = "Pixels")