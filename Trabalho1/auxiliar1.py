# Funcoes auxiliares

import cv2 as cv
import numpy as np

# exibir: exibe a imagem em uma janela e a salva em um arquivo se o usuario entrar "s", senão
# apenas continua a execucao
def exibir(janela,img,saida,close):
    cv.imshow(janela, img)
    k = cv.waitKey(0) & 0xFF

    if k == ord("s"):
        cv.imwrite(saida, img)

    if close == 1:
        cv.destroyWindow(janela)
    elif close == 2:
        cv.destroyAllWindows()
    else:
        return

# correcaoGamma: corrige o brilho da imagem de acordo com a power law transform
def correcaoGamma(img, gamma=1.0):
    invGamma = 1.0 / gamma
    # Utiliza uma tabela para mapear cada pixel e seu valor corrigido
    tabela = np.array([((i/255.0) ** invGamma) * 255
                       for i in np.arange(0,256)]).astype("uint8")

    return cv.LUT(img,tabela)

# getPlano: cria uma máscara para obter um determinado plano de bits de uma imagem
def getPlano(img, plano):
    plano = np.full((img.shape[0], img.shape[1]), 2 ** plano, np.uint8)
    t = cv.bitwise_and(plano, img)
    # Aumentar a intensidade dos pixels
    r = t * 255
    return r

def criaFiltros(filtro):
    h1 = np.array((
        [0, 0, -1, 0, 0],
        [0, -1, -2, -1, 0],
        [-1, -2, 16, -2, -1],
        [0, -1, -2, -1, 0],
        [0, 0, -1, 0, 0]), dtype="int")

    h2 = np.array((
        [1, 4, 6, 4, 1],
        [4, 16, 24, 16, 4],
        [6, 24, 36, 24, 6],
        [4, 16, 24, 16, 4],
        [1, 4, 6, 4, 1]) / 256, dtype="float")

    h3 = np.array((
        [-1, 0, 1],
        [-2, 0, 2],
        [-1, 0, 1]), dtype="int")

    h4 = np.array((
        [-1, -2, -1],
        [0, 0, 0],
        [1, 2, 1]), dtype="int")

    h5 = np.array((
        [-1, -1, -1],
        [-1, 8, -1],
        [-1, -1, -1]), dtype="int")

    h6 = np.ones((3,3), dtype="float") / 9

    h7 = np.array((
        [-1, -1, 2],
        [-1, 2, -1],
        [2, -1, -1]), dtype="int")

    h8 = np.array((
        [2, -1, -1],
        [-1, 2, -1],
        [-1, -1, 2]), dtype="int")

    h9 = np.diag(np.ones(9, dtype="float")) / 9

    h10 = np.array((
        [-1, -1, -1, -1, -1],
        [-1, 2, 2, 2, -1],
        [-1, 2, 8, 2, -1],
        [-1, 2, 2, 2, -1],
        [-1, -1, -1, -1, -1]), dtype="float") / 8

    h11 = np.array((
        [-1, -1, 0],
        [-1, 0, 1],
        [0, 1, 1]), dtype="int")