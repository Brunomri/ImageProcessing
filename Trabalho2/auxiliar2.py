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

# Conversao para garantir intervalo de intensidades entre um lower bound e um upper bound
def intervalo(img, lb, ub):
    img = np.clip(img, lb, ub)
    img = img.astype(np.uint8)
    return img

# Aplica a difusao de erro de Floyd-Steinberg em uma imagem f e gera o resultado em g.
def fs(img):
    b, g, r = cv.split(img)
    ch = [b, g, r]

    for cor in range(len(ch)):
        m, n = ch[cor].shape
        f = np.copy(ch[cor]).astype("float")
        g = np.copy(ch[cor])

        for x in range(m - 1):
            for y in range(n - 1):
                if f[x, y] < 128:
                    g[x, y] = 0
                else:
                    g[x, y] = 1
                erro = f[x, y] - g[x, y] * 255

                f[x + 1, y]     = f[x + 1, y]     + (7/16) * erro
                f[x - 1, y + 1] = f[x - 1, y + 1] + (3/16) * erro
                f[x, y + 1]     = f[x, y + 1]     + (5/16) * erro
                f[x + 1, y + 1] = f[x + 1, y + 1] + (1/16) * erro

        ch[cor] = g
        print("Cor", cor)

    res = cv.merge(ch)

    return res * 255