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

# Conversao para garantir intervalo de intensidades entre um lower bound e um upper bound
def intervalo(img, lb, ub):
    img = np.clip(img, lb, ub)
    img = img.astype(np.uint8)
    return img

# aplicaFiltros: recebe um conjunto de filtros e os aplica em uma imagem, exibindo
# o resultado em seguida
def aplicaFiltros(filtros, img, nomeImg):
    for (nomeFiltro, filtro) in filtros:
        print("Aplicando filtro {}".format(nomeFiltro))
        #print("Filtro original\n", filtro)
        #print("Filtro rotacionado\n", cv.flip(filtro, -1))

        # A funcao filter2d da biblioteca OpenCV de fato realiza uma operacao de correlacao e nao
        # convolucao. Por isso, e preciso rotacionar a mascara do filtro em 180 graus para obter o resultado
        # esperado quando a mascara nao e simetrica. A rotacao e feita por cv.flip com parametro -1 para
        # rotacionar simultaneamente a matriz do filtro na horizontal e vertical. O parametro escolhido para
        # o tratamento de bordas e a replicacao dos pixels
        res = cv.filter2D(img, -1, cv.flip(filtro, -1), borderType = cv.BORDER_REPLICATE)
        exibir("{} ".format(nomeFiltro), res, "{}_{}".format(nomeFiltro, nomeImg), 0)

# combFiltros: aplica a combinacao de dois filtros em uma mesma imagem
def combFiltros(filtros, f1, f2, img, nomeImg):
    nomeF1, filtro1 = filtros[f1]
    nomeF2, filtro2 = filtros[f2]
    print("Aplicando composicao de filtros {} e {}".format(nomeF1, nomeF2))
    #print("Filtro 1: ", nomeF1)
    #print("Filtro 2: ", nomeF2)

    # Aplica cada filtro individualmente e armazena o resultado em 2 variaveis
    temp1 = cv.filter2D(img, -1, cv.flip(filtro1, -1), borderType = cv.BORDER_REPLICATE)
    temp2 = cv.filter2D(img, -1, cv.flip(filtro2, -1), borderType = cv.BORDER_REPLICATE)

    # Eleva a matriz resultado de cada filtro ao quadrado
    temp3 = np.square(temp1, dtype="float32")
    #temp3 = intervalo(temp3, 0, 255)
    #print("Temp3\n", temp3)
    temp4 = np.square(temp2, dtype="float32")
    #temp4 = intervalo(temp4, 0, 255)
    #print("Temp4\n", temp4)

    # Soma as duas matrizes resultado de cada filtro
    temp5 = np.add(temp3, temp4,dtype="float32")
    #temp5 = intervalo(temp5, 0, 255)
    res = np.zeros((img.shape[0], img.shape[1]), dtype="float32")

    # Obtém o resultado final extraindo a raiz quadrada da soma anterior
    np.sqrt(temp5, res)

    # Conversao para garantir intervalo de intensidades entre 0 e 255
    res = intervalo(res, 0, 255)

    #print(res)

    exibir("{}_{}".format(nomeF1, nomeF2), res, "{}_{}_{}".format(nomeF1, nomeF2, nomeImg), 0)