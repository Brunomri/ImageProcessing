# Funcoes auxiliares

import cv2 as cv
import numpy as np

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

# criaFiltros: cria as matrizes referentes aos filtros contidos no enunciado e
# retorna um conjunto de tuplas com o nome de cada filtro e a matriz correspondente
def criaFiltros():
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
        [1, 4, 6, 4, 1]), dtype="float") / 256

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

    filtros = (
        ("h1",h1),
        ("h2",h2),
        ("h3",h3),
        ("h4",h4),
        ("h5",h5),
        ("h6",h6),
        ("h7",h7),
        ("h8",h8),
        ("h9",h9),
        ("h10",h10),
        ("h11",h11)
        )

    return filtros


# aplicaFiltros: recebe um conjunto de filtros e os aplica em uma imagem, exibindo
# o resultado em seguida
def aplicaFiltros(filtros, img, nomeImg):
    for (nomeFiltro, filtro) in filtros:
        print("Aplicando filtro {}".format(nomeFiltro))
        #print("Filtro original\n", filtro)
        #print("Filtro rotacionado\n", cv.flip(filtro, -1))
        res = cv.filter2D(img, -1, cv.flip(filtro, -1), borderType = cv.BORDER_REPLICATE)
        exibir("{} ".format(nomeFiltro), res, "{}_{}".format(nomeFiltro, nomeImg), 0)