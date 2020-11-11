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
    m, n = img.shape
    f = np.copy(img).astype("float")
    g = np.copy(img)

    for x in range(m - 1):
        print("F", f)
        for y in range(n - 1):
            if f[x, y] < 128:
                g[x, y] = 0
            else:
                g[x, y] = 1
            erro = f[x, y] - g[x, y] * 255

            f[x + 1, y] = f[x + 1, y] + (7/16) * erro
            f[x - 1, y + 1] = f[x - 1, y + 1] + (3/16) * erro
            f[x, y + 1] = f[x, y + 1] + (5/16) * erro
            f[x + 1, y + 1] = f[x + 1, y + 1] + (1/16) * erro

    return g * 255