# Funcoes auxiliares

import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt
from skimage.util.shape import view_as_windows
import math

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

    # Obtem o limiar global de Otsu e a imagem resultante
    thr,res = cv.threshold(img, 0, 255, cv.THRESH_BINARY_INV+cv.THRESH_OTSU)
    print("Limiar = {}".format(thr))

    # Exibe a imagem resultante e seu histograma
    exibir("Otsu (T = {})".format(thr), res, "otsu_t{}_{}".format(thr, inp), 0)
    histograma(res, titulo = "Otsu (T = {})".format(thr), rotulo_x = "Intensidade", rotulo_y = "Pixels")

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
def bernsen(img, inp, t_janela = 15, ctr_thr = 30):
    print("Aplicando limiarizacao local de Bensen em {}".format(inp))
    print("Tamanho da janela = {} x {}".format(t_janela, t_janela))

    # Chamada a funcao que calcula os limiares de cada pixel
    thr = get_bernsen_thr(img, t_janela, ctr_thr)
    print("Limiares = \n{}".format(thr))

    # Atribui valor 255 aos pixels menores que o limiar (pixels brancos ao fundo)
    res = ((img < thr) * 255).astype(np.uint8)

    # Exibe a imagem resultante e seu histograma
    exibir("Bernsen (W = {})".format(t_janela), res, "bernsen_w{}_{}".format(t_janela, inp), 0)
    histograma(res, titulo = "Bernsen (W = {})".format(t_janela), rotulo_x = "Intensidade", rotulo_y = "Pixels")

# get_niblack_thr: retorna o limiar de Niblack para cada pixel de uma imagem de entrada img de acordo
# com o tamanho da janela e fator k fornecidos
def get_niblack_thr(img, t_janela = 15, k = -0.2):

    # Definindo numero de linhas e colunas da imagem
    linhas, colunas = img.shape
    i_linhas, i_colunas = linhas + 1, colunas + 1

    # Utilizar imagens integrais para calcular media e desvio padrao
    # Definindo primeira linha e coluna como zero por conveniencia
    integ = np.zeros((i_linhas, i_colunas), np.float)
    sqr_integral = np.zeros((i_linhas, i_colunas), np.float)

    integ[1:, 1:] = np.cumsum(np.cumsum(img.astype(np.float), axis=0), axis=1)
    sqr_img = np.square(img.astype(np.float))
    sqr_integral[1:, 1:] = np.cumsum(np.cumsum(sqr_img, axis=0), axis=1)

    # Definir grid
    x, y = np.meshgrid(np.arange(1, i_colunas), np.arange(1, i_linhas))

    # Obter coordenadas locais
    hw_size = t_janela // 2
    x1 = (x - hw_size).clip(1, colunas)
    x2 = (x + hw_size).clip(1, colunas)
    y1 = (y - hw_size).clip(1, linhas)
    y2 = (y + hw_size).clip(1, linhas)

    # Obter tamanho de areas locais
    l_size = (y2 - y1 + 1) * (x2 - x1 + 1)

    # Calculando somas e somas ao quadrado para o calculo das medias e desvios padrao
    somas = (integ[y2, x2] - integ[y2, x1 - 1] -
            integ[y1 - 1, x2] + integ[y1 - 1, x1 - 1])
    somas_2 = (sqr_integral[y2, x2] - sqr_integral[y2, x1 - 1] -
                sqr_integral[y1 - 1, x2] + sqr_integral[y1 - 1, x1 - 1])

    # Calculando medias locais
    medias = somas / l_size

    # Calculando desvios padrao locais
    desvios = np.sqrt(somas_2 / l_size - np.square(medias))

    # Obtem valores de limiar para cada pixel
    thr = medias + k * desvios

    return thr

# niblack: aplica limiarizacao local de Niblack com tamanho de janela e 
# fator k fornecidos, exibindo a imagem resultante e seu histograma
def niblack(img, inp, t_janela = 15, k = -0.2):
    print("Aplicando limiarizacao local de Niblack em {}".format(inp))
    print("Tamanho da janela = {} x {}".format(t_janela, t_janela))

    # Chamada a funcao que calcula os limiares de cada pixel
    thr = get_niblack_thr(img, t_janela, k)
    print("Limiares = \n{}".format(thr))

    # Atribui valor 255 aos pixels menores que o limiar (pixels brancos ao fundo)
    res = ((img < thr) * 255).astype(np.uint8)

    # Exibe a imagem resultante e seu histograma
    exibir("Niblack (W = {}, k = {})".format(t_janela, k), res, "niblack_w{}_k{}_{}".format(t_janela, k, inp), 0)
    histograma(res, titulo = "Niblack (W = {}, k = {})".format(t_janela, k), rotulo_x = "Intensidade", rotulo_y = "Pixels")

# get_sauvola_thr: retorna o limiar de Sauvola e Pietaksinen para cada pixel de uma imagem de entrada img de acordo
# com o tamanho da janela e fator k fornecidos
def get_sauvola_thr(img, t_janela = 15, k = 0.5, R = 128):

    # Definindo numero de linhas e colunas da imagem
    linhas, colunas = img.shape
    i_linhas, i_colunas = linhas + 1, colunas + 1

    # Utilizar imagens integrais para calcular media e desvio padrao
    # Definindo primeira linha e coluna como zero por conveniencia
    integ = np.zeros((i_linhas, i_colunas), np.float)
    sqr_integral = np.zeros((i_linhas, i_colunas), np.float)

    integ[1:, 1:] = np.cumsum(np.cumsum(img.astype(np.float), axis=0), axis=1)
    sqr_img = np.square(img.astype(np.float))
    sqr_integral[1:, 1:] = np.cumsum(np.cumsum(sqr_img, axis=0), axis=1)

    # Definir grid
    x, y = np.meshgrid(np.arange(1, i_colunas), np.arange(1, i_linhas))

    # Obter coordenadas locais
    hw_size = t_janela // 2
    x1 = (x - hw_size).clip(1, colunas)
    x2 = (x + hw_size).clip(1, colunas)
    y1 = (y - hw_size).clip(1, linhas)
    y2 = (y + hw_size).clip(1, linhas)

    # Obter tamanho de areas locais
    l_size = (y2 - y1 + 1) * (x2 - x1 + 1)

    # Calculando somas e somas ao quadrado para o calculo das medias e desvios padrao
    somas = (integ[y2, x2] - integ[y2, x1 - 1] -
            integ[y1 - 1, x2] + integ[y1 - 1, x1 - 1])
    somas_2 = (sqr_integral[y2, x2] - sqr_integral[y2, x1 - 1] -
                sqr_integral[y1 - 1, x2] + sqr_integral[y1 - 1, x1 - 1])

    # Calculando medias locais
    medias = somas / l_size

    # Calculando desvios padrao locais
    desvios = np.sqrt(somas_2 / l_size - np.square(medias))

    # Obtem valores de limiar para cada pixel
    thr = medias * (1.0 + k * (desvios / R - 1.0))

    return thr

# sauvola: aplica limiarizacao local de Sauvola e Pietaksinen com tamanho de janela e 
# fator k fornecidos, exibindo a imagem resultante e seu histograma
def sauvola(img, inp, t_janela = 15, k = 0.5, R = 128):
    print("Aplicando limiarizacao local de Sauvola e Pietaksinen em {}".format(inp))
    print("Tamanho da janela = {} x {}".format(t_janela, t_janela))

    # Chamada a funcao que calcula os limiares de cada pixel
    thr = get_sauvola_thr(img, t_janela, k, R)
    print("Limiares = \n{}".format(thr))

    # Atribui valor 255 aos pixels menores que o limiar (pixels brancos ao fundo)
    res = ((img < thr) * 255).astype(np.uint8)

    # Exibe a imagem resultante e seu histograma
    exibir("Sauvola e Pietaksinen (W = {}, k = {})".format(t_janela, k), res, "sauvola_w{}_k{}_{}".format(t_janela, k, inp), 0)
    histograma(res, titulo = "Sauvola e Pietaksinen (W = {}, k = {})".format(t_janela, k), rotulo_x = "Intensidade", rotulo_y = "Pixels")

# get_more_thr: retorna o limiar de Phansalskar, More e Sabale para cada pixel de uma imagem de entrada img de acordo
# com o tamanho da janela e fator k fornecidos
def get_more_thr(img, t_janela = 15, k = 0.25, R = 0.5, p = 2, q = 10):

    # Definindo numero de linhas e colunas da imagem
    linhas, colunas = img.shape
    i_linhas, i_colunas = linhas + 1, colunas + 1

    # Utilizar imagens integrais para calcular media e desvio padrao
    # Definindo primeira linha e coluna como zero por conveniencia
    integ = np.zeros((i_linhas, i_colunas), np.float)
    sqr_integral = np.zeros((i_linhas, i_colunas), np.float)

    integ[1:, 1:] = np.cumsum(np.cumsum(img.astype(np.float), axis=0), axis=1)
    sqr_img = np.square(img.astype(np.float))
    sqr_integral[1:, 1:] = np.cumsum(np.cumsum(sqr_img, axis=0), axis=1)

    # Definir grid
    x, y = np.meshgrid(np.arange(1, i_colunas), np.arange(1, i_linhas))

    # Obter coordenadas locais
    hw_size = t_janela // 2
    x1 = (x - hw_size).clip(1, colunas)
    x2 = (x + hw_size).clip(1, colunas)
    y1 = (y - hw_size).clip(1, linhas)
    y2 = (y + hw_size).clip(1, linhas)

    # Obter tamanho de areas locais
    l_size = (y2 - y1 + 1) * (x2 - x1 + 1)

    # Calculando somas e somas ao quadrado para o calculo das medias e desvios padrao
    somas = (integ[y2, x2] - integ[y2, x1 - 1] -
            integ[y1 - 1, x2] + integ[y1 - 1, x1 - 1])
    somas_2 = (sqr_integral[y2, x2] - sqr_integral[y2, x1 - 1] -
                sqr_integral[y1 - 1, x2] + sqr_integral[y1 - 1, x1 - 1])

    # Calculando medias locais
    medias = somas / l_size

    # Calculando desvios padrao locais
    desvios = np.sqrt(somas_2 / l_size - np.square(medias))

    # Obtem valores de limiar para cada pixel
    thr = medias * (1.0 + p * np.power(math.e, (-q * medias)) + k * (desvios / R - 1.0))

    return thr

# more: aplica limiarizacao local de Phansalskar, More e Sabale com tamanho de janela e 
# fator k fornecidos, exibindo a imagem resultante e seu histograma
def more(img, inp, t_janela = 15, k = 0.5, R = 128, p = 2, q = 10):
    print("Aplicando limiarizacao local de Sauvola e Pietaksinen em {}".format(inp))
    print("Tamanho da janela = {} x {}".format(t_janela, t_janela))

    # Chamada a funcao que calcula os limiares de cada pixel
    thr = get_more_thr(img, t_janela, k, R, p, q)
    print("Limiares = \n{}".format(thr))

    # Atribui valor 255 aos pixels menores que o limiar (pixels brancos ao fundo)
    res = ((img < thr) * 255).astype(np.uint8)

    # Exibe a imagem resultante e seu histograma
    exibir("Phansalskar, More e Sabale (W = {}, k = {})".format(t_janela, k), res, "more_w{}_k{}_{}".format(t_janela, k, inp), 0)
    histograma(res, titulo = "Phansalskar, More e Sabale (W = {}, k = {})".format(t_janela, k), rotulo_x = "Intensidade", rotulo_y = "Pixels")

# get_contrast_thr: retorna o limiar de Metodo do Contraste para cada pixel da imagem de entrada utilizando 
# o tamanho de janela fornecido
def get_contrast_thr(img, t_janela = 15):

    thr = np.zeros(img.shape)

    # Tratamento de bordas com padding em funcao do tamanho da janela
    hw_size = t_janela // 2
    borda_img = np.ones((img.shape[0] + t_janela - 1,
                          img.shape[1] + t_janela - 1)) * np.nan
    borda_img[hw_size: -hw_size, hw_size: -hw_size] = img

    # Obtem janelas do tamanho especificado
    janelas = view_as_windows(borda_img, (t_janela, t_janela))

    # Calcula o valor minimo e maximo em cada janela
    minimos = np.nanmin(janelas, axis=(2, 3))
    maximos = np.nanmax(janelas, axis=(2, 3))

    # Calcula diferencas entre os pixels da imagem e o minimo e maximo de sua vizinhanca
    min_dif = img - minimos
    max_dif = maximos - img

    # Define o limiar de acordo com a proximidade entre valor do pixel e o minimo
    # ou maximo local
    thr[min_dif <= max_dif] = 256
    thr[min_dif > max_dif] = 0

    return thr

# contrast: aplica limiarizacao local do Metodo do Contraste com tamanho de janela
# fornecido, exibindo a imagem resultante e seu histograma
def contrast(img, inp, t_janela = 15):
    print("Aplicando limiarizacao local do Metodo do Contraste em {}".format(inp))
    print("Tamanho da janela = {} x {}".format(t_janela, t_janela))

    # Chamada a funcao que calcula os limiares de cada pixel
    thr = get_contrast_thr(img, t_janela)
    print("Limiares = \n{}".format(thr))

    # Atribui valor 255 aos pixels menores que o limiar (pixels brancos ao fundo)
    res = ((img < thr) * 255).astype(np.uint8)

    # Exibe a imagem resultante e seu histograma
    exibir("Metodo do Contraste (W = {})".format(t_janela), res, "contrast_w{}_{}".format(t_janela, inp), 0)
    histograma(res, titulo = "Metodo do Contraste (W = {})".format(t_janela), rotulo_x = "Intensidade", rotulo_y = "Pixels")

# get_mean_thr: retorna o limiar de Metodo da Media para cada pixel da imagem de entrada utilizando 
# o tamanho de janela fornecido
def get_mean_thr(img, t_janela = 15):

    # Definindo numero de linhas e colunas da imagem
    linhas, colunas = img.shape
    i_linhas, i_colunas = linhas + 1, colunas + 1

    # Calculando imagem integral
    integ = np.zeros((i_linhas, i_colunas), np.float)

    integ[1:, 1:] = np.cumsum(np.cumsum(img.astype(np.float), axis=0), axis=1)

    # Definir grid
    x, y = np.meshgrid(np.arange(1, i_colunas), np.arange(1, i_linhas))

    # Obter coordenadas locais
    hw_size = t_janela // 2
    x1 = (x - hw_size).clip(1, colunas)
    x2 = (x + hw_size).clip(1, colunas)
    y1 = (y - hw_size).clip(1, linhas)
    y2 = (y + hw_size).clip(1, linhas)

    # Obter tamanho de areas locais
    l_size = (y2 - y1 + 1) * (x2 - x1 + 1)

    # Calculando somas
    somas = (integ[y2, x2] - integ[y2, x1 - 1] -
            integ[y1 - 1, x2] + integ[y1 - 1, x1 - 1])

    # Calculando medias locais
    thr = somas / l_size

    return thr

# mean: aplica limiarizacao local do Metodo da Media com tamanho de janela
# fornecido, exibindo a imagem resultante e seu histograma
def mean(img, inp, t_janela = 15):
    print("Aplicando limiarizacao local do Metodo da Media em {}".format(inp))
    print("Tamanho da janela = {} x {}".format(t_janela, t_janela))

    # Chamada a funcao que calcula os limiares de cada pixel
    thr = get_mean_thr(img, t_janela)
    print("Limiares = \n{}".format(thr))

    # Atribui valor 255 aos pixels menores que o limiar (pixels brancos ao fundo)
    res = ((img < thr) * 255).astype(np.uint8)

    # Exibe a imagem resultante e seu histograma
    exibir("Metodo da Media (W = {})".format(t_janela), res, "mean_w{}_{}".format(t_janela, inp), 0)
    histograma(res, titulo = "Metodo da Media (W = {})".format(t_janela), rotulo_x = "Intensidade", rotulo_y = "Pixels")