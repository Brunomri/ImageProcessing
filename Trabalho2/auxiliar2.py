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

# Aplica a difusao de erro de Floyd-Steinberg para cada banda de uma imagem img e gera o resultado em res
def fs(img):
    print("Floyd-Steinberg\n")
    # Divide a imagem em 3 bandas de cor e as adiciona em uma lista
    b, g, r = cv.split(img)
    ch = [b, g, r]

    # Percorre a lista de bandas de cor aplicando o algoritmo a cada uma delas
    for cor in range(len(ch)):
        m, n = ch[cor].shape
        f = np.copy(ch[cor]).astype("float")
        g = np.copy(ch[cor])

        for x in range(m):
            for y in range(n):
                if f[x, y] < 128:
                    g[x, y] = 0
                else:
                    g[x, y] = 1
                erro = f[x, y] - g[x, y] * 255

                # Verificacao para evitar que a propagacao do erro ultrapasse as 
                # dimensoes da imagem
                if 0 < x < m - 1 and y < n - 1:
                    # Propaga o erro aos vizinhos
                    f[x + 1, y]     = f[x + 1, y]     + (7/16) * erro
                    f[x - 1, y + 1] = f[x - 1, y + 1] + (3/16) * erro
                    f[x, y + 1]     = f[x, y + 1]     + (5/16) * erro
                    f[x + 1, y + 1] = f[x + 1, y + 1] + (1/16) * erro

        # Atualiza as bandas de cor apos o procedimento
        ch[cor] = g
    
    # Mescla as bandas de cor para formar a imagem resultante
    res = cv.merge(ch)
    print("Verificando imagem binária: {}\n".format(np.unique(res)))

    # Multiplica imagem resultante por 255 para permitir visualizacao
    return res * 255

# Aplica a difusao de erro de Floyd-Steinberg com percurso alternado para cada banda de uma imagem img e gera o resultado em res
def fs_alt(img):
    print("Floyd-Steinberg alternado\n")
    # Divide a imagem em 3 bandas de cor e as adiciona em uma lista
    b, g, r = cv.split(img)
    ch = [b, g, r]

    # Percorre a lista de bandas de cor aplicando o algoritmo a cada uma delas
    for cor in range(len(ch)):
        m, n = ch[cor].shape
        f = np.copy(ch[cor]).astype("float")
        g = np.copy(ch[cor])

        for x in range(m):
            for y in range(n):
                if f[x, y] < 128:
                    g[x, y] = 0
                else:
                    g[x, y] = 1
                erro = f[x, y] - g[x, y] * 255

                # Verifica se uma linha e par ou impar para aplicar o percurso normal ou alternado
                if x % 2 == 0:
                    # Verificacao para evitar que a propagacao do erro ultrapasse as 
                    # dimensoes da imagem
                    if 0 < x < m - 1 and y < n - 1:
                        # Propaga o erro aos vizinhos
                        f[x + 1, y]     = f[x + 1, y]     + (7/16) * erro
                        f[x - 1, y + 1] = f[x - 1, y + 1] + (3/16) * erro
                        f[x, y + 1]     = f[x, y + 1]     + (5/16) * erro
                        f[x + 1, y + 1] = f[x + 1, y + 1] + (1/16) * erro

                else:
                    # Verificacao para evitar que a propagacao do erro ultrapasse as 
                    # dimensoes da imagem
                    if 0 < x < m - 1 and y < n - 1:
                        # Propaga o erro aos vizinhos
                        f[x - 1, y]     = f[x - 1, y]     + (7/16) * erro
                        f[x + 1, y + 1] = f[x + 1, y + 1] + (3/16) * erro
                        f[x, y + 1]     = f[x, y + 1]     + (5/16) * erro
                        f[x - 1, y + 1] = f[x - 1, y + 1] + (1/16) * erro

        # Atualiza as bandas de cor apos o procedimento
        ch[cor] = g
    
    # Mescla as bandas de cor para formar a imagem resultante
    res = cv.merge(ch)
    print("Verificando imagem binária: {}\n".format(np.unique(res)))

    # Multiplica imagem resultante por 255 para permitir visualizacao
    return res * 255

# Aplica a difusao de erro de Stevenson-Arce para cada banda de uma imagem img e gera o resultado em res
def sa(img):
    print("Stevenson-Arce\n")
    # Divide a imagem em 3 bandas de cor e as adiciona em uma lista
    b, g, r = cv.split(img)
    ch = [b, g, r]

    # Percorre a lista de bandas de cor aplicando o algoritmo a cada uma delas
    for cor in range(len(ch)):
        m, n = ch[cor].shape
        f = np.copy(ch[cor]).astype("float")
        g = np.copy(ch[cor])

        for x in range(m):
            for y in range(n):
                if f[x, y] < 128:
                    g[x, y] = 0
                else:
                    g[x, y] = 1
                erro = f[x, y] - g[x, y] * 255

                # Verificacao para evitar que a propagacao do erro ultrapasse as 
                # dimensoes da imagem
                if 2 < x < m - 3 and y < n - 3:
                    # Propaga o erro aos vizinhos
                    f[x + 2, y]     = f[x + 2, y]     + (32/200) * erro
                    f[x - 3, y + 1] = f[x - 3, y + 1] + (12/200) * erro
                    f[x - 1, y + 1] = f[x - 1, y + 1] + (26/200) * erro
                    f[x + 1, y + 1] = f[x + 1, y + 1] + (30/200) * erro
                    f[x + 3, y + 1] = f[x + 3, y + 1] + (16/200) * erro
                    f[x - 2, y + 2] = f[x - 2, y + 2] + (12/200) * erro
                    f[x, y + 2]     = f[x, y + 2]     + (26/200) * erro
                    f[x + 2, y + 2] = f[x + 2, y + 2] + (12/200) * erro
                    f[x - 3, y + 3] = f[x - 3, y + 3] + (5/200)  * erro
                    f[x - 1, y + 3] = f[x - 1, y + 3] + (12/200) * erro
                    f[x + 1, y + 3] = f[x + 1, y + 3] + (12/200) * erro
                    f[x + 3, y + 3] = f[x + 3, y + 3] + (5/200)  * erro

        # Atualiza as bandas de cor apos o procedimento
        ch[cor] = g
    
    # Mescla as bandas de cor para formar a imagem resultante
    res = cv.merge(ch)
    print("Verificando imagem binária: {}\n".format(np.unique(res)))

    # Multiplica imagem resultante por 255 para permitir visualizacao
    return res * 255

# Aplica a difusao de erro de Stevenson-Arce com percurso alternado para cada banda de uma imagem img e gera o resultado em res
def sa_alt(img):
    print("Stevenson-Arce alternado\n")
    # Divide a imagem em 3 bandas de cor e as adiciona em uma lista
    b, g, r = cv.split(img)
    ch = [b, g, r]

    # Percorre a lista de bandas de cor aplicando o algoritmo a cada uma delas
    for cor in range(len(ch)):
        m, n = ch[cor].shape
        f = np.copy(ch[cor]).astype("float")
        g = np.copy(ch[cor])

        for x in range(m):
            for y in range(n):
                if f[x, y] < 128:
                    g[x, y] = 0
                else:
                    g[x, y] = 1
                erro = f[x, y] - g[x, y] * 255

                # Verifica se uma linha e par ou impar para aplicar o percurso normal ou alternado
                if x % 2 == 0:
                    # Verificacao para evitar que a propagacao do erro ultrapasse as 
                    # dimensoes da imagem
                    if 2 < x < m - 3 and y < n - 3:
                        # Propaga o erro aos vizinhos
                        f[x + 2, y]     = f[x + 2, y]     + (32/200) * erro
                        f[x - 3, y + 1] = f[x - 3, y + 1] + (12/200) * erro
                        f[x - 1, y + 1] = f[x - 1, y + 1] + (26/200) * erro
                        f[x + 1, y + 1] = f[x + 1, y + 1] + (30/200) * erro
                        f[x + 3, y + 1] = f[x + 3, y + 1] + (16/200) * erro
                        f[x - 2, y + 2] = f[x - 2, y + 2] + (12/200) * erro
                        f[x, y + 2]     = f[x, y + 2]     + (26/200) * erro
                        f[x + 2, y + 2] = f[x + 2, y + 2] + (12/200) * erro
                        f[x - 3, y + 3] = f[x - 3, y + 3] + (5/200)  * erro
                        f[x - 1, y + 3] = f[x - 1, y + 3] + (12/200) * erro
                        f[x + 1, y + 3] = f[x + 1, y + 3] + (12/200) * erro
                        f[x + 3, y + 3] = f[x + 3, y + 3] + (5/200)  * erro

                else:
                    # Verificacao para evitar que a propagacao do erro ultrapasse as 
                    # dimensoes da imagem
                    if 2 < x < m - 3 and y < n - 3:
                        # Propaga o erro aos vizinhos
                        f[x - 2, y]     = f[x - 2, y]     + (32/200) * erro
                        f[x + 3, y + 1] = f[x + 3, y + 1] + (12/200) * erro
                        f[x + 1, y + 1] = f[x + 1, y + 1] + (26/200) * erro
                        f[x - 1, y + 1] = f[x - 1, y + 1] + (30/200) * erro
                        f[x - 3, y + 1] = f[x - 3, y + 1] + (16/200) * erro
                        f[x + 2, y + 2] = f[x + 2, y + 2] + (12/200) * erro
                        f[x, y + 2]     = f[x, y + 2]     + (26/200) * erro
                        f[x - 2, y + 2] = f[x - 2, y + 2] + (12/200) * erro
                        f[x + 3, y + 3] = f[x + 3, y + 3] + (5/200)  * erro
                        f[x + 1, y + 3] = f[x + 1, y + 3] + (12/200) * erro
                        f[x - 1, y + 3] = f[x - 1, y + 3] + (12/200) * erro
                        f[x - 3, y + 3] = f[x - 3, y + 3] + (5/200)  * erro

        # Atualiza as bandas de cor apos o procedimento
        ch[cor] = g
    
    # Mescla as bandas de cor para formar a imagem resultante
    res = cv.merge(ch)
    print("Verificando imagem binária: {}\n".format(np.unique(res)))

    # Multiplica imagem resultante por 255 para permitir visualizacao
    return res * 255

# Aplica a difusao de erro de Burkes para cada banda de uma imagem img e gera o resultado em res
def burkes(img):
    print("Burkes\n")
    # Divide a imagem em 3 bandas de cor e as adiciona em uma lista
    b, g, r = cv.split(img)
    ch = [b, g, r]

    # Percorre a lista de bandas de cor aplicando o algoritmo a cada uma delas
    for cor in range(len(ch)):
        m, n = ch[cor].shape
        f = np.copy(ch[cor]).astype("float")
        g = np.copy(ch[cor])

        for x in range(m):
            for y in range(n):
                if f[x, y] < 128:
                    g[x, y] = 0
                else:
                    g[x, y] = 1
                erro = f[x, y] - g[x, y] * 255

                # Verificacao para evitar que a propagacao do erro ultrapasse as 
                # dimensoes da imagem
                if 1 < x < m - 2 and y < n - 1:
                    # Propaga o erro aos vizinhos
                    f[x + 1, y]     = f[x + 1, y]     + (8/32) * erro
                    f[x + 2, y]     = f[x + 2, y]     + (4/32) * erro
                    f[x - 2, y + 1] = f[x - 2, y + 1] + (2/32) * erro
                    f[x - 1, y + 1] = f[x - 1, y + 1] + (4/32) * erro
                    f[x, y + 1]     = f[x, y + 1]     + (8/32) * erro
                    f[x + 1, y + 1] = f[x + 1, y + 1] + (4/32) * erro
                    f[x + 2, y + 1] = f[x + 2, y + 1] + (2/32) * erro


        # Atualiza as bandas de cor apos o procedimento
        ch[cor] = g
    
    # Mescla as bandas de cor para formar a imagem resultante
    res = cv.merge(ch)
    print("Verificando imagem binária: {}\n".format(np.unique(res)))

    # Multiplica imagem resultante por 255 para permitir visualizacao
    return res * 255

# Aplica a difusao de erro de Burkes com percurso alternado para cada banda de uma imagem img e gera o resultado em res
def burkes_alt(img):
    print("Burkes alternado\n")
    # Divide a imagem em 3 bandas de cor e as adiciona em uma lista
    b, g, r = cv.split(img)
    ch = [b, g, r]

    # Percorre a lista de bandas de cor aplicando o algoritmo a cada uma delas
    for cor in range(len(ch)):
        m, n = ch[cor].shape
        f = np.copy(ch[cor]).astype("float")
        g = np.copy(ch[cor])

        for x in range(m):
            for y in range(n):
                if f[x, y] < 128:
                    g[x, y] = 0
                else:
                    g[x, y] = 1
                erro = f[x, y] - g[x, y] * 255

                # Verifica se uma linha e par ou impar para aplicar o percurso normal ou alternado
                if x % 2 == 0:
                    # Verificacao para evitar que a propagacao do erro ultrapasse as 
                    # dimensoes da imagem
                    if 1 < x < m - 2 and y < n - 1:
                        # Propaga o erro aos vizinhos
                        f[x + 1, y]     = f[x + 1, y]     + (8/32) * erro
                        f[x + 2, y]     = f[x + 2, y]     + (4/32) * erro
                        f[x - 2, y + 1] = f[x - 2, y + 1] + (2/32) * erro
                        f[x - 1, y + 1] = f[x - 1, y + 1] + (4/32) * erro
                        f[x, y + 1]     = f[x, y + 1]     + (8/32) * erro
                        f[x + 1, y + 1] = f[x + 1, y + 1] + (4/32) * erro
                        f[x + 2, y + 1] = f[x + 2, y + 1] + (2/32) * erro
                else:
                    # Verificacao para evitar que a propagacao do erro ultrapasse as 
                    # dimensoes da imagem
                    if 1 < x < m - 2 and y < n - 1:
                        # Propaga o erro aos vizinhos
                        f[x - 1, y]     = f[x - 1, y]     + (8/32) * erro
                        f[x - 2, y]     = f[x - 2, y]     + (4/32) * erro
                        f[x + 2, y + 1] = f[x + 2, y + 1] + (2/32) * erro
                        f[x + 1, y + 1] = f[x + 1, y + 1] + (4/32) * erro
                        f[x, y + 1]     = f[x, y + 1]     + (8/32) * erro
                        f[x - 1, y + 1] = f[x - 1, y + 1] + (4/32) * erro
                        f[x - 2, y + 1] = f[x - 2, y + 1] + (2/32) * erro


        # Atualiza as bandas de cor apos o procedimento
        ch[cor] = g
    
    # Mescla as bandas de cor para formar a imagem resultante
    res = cv.merge(ch)
    print("Verificando imagem binária: {}\n".format(np.unique(res)))

    # Multiplica imagem resultante por 255 para permitir visualizacao
    return res * 255

# Aplica a difusao de erro de Sierra para cada banda de uma imagem img e gera o resultado em res
def sierra(img):
    print("Sierra\n")
    # Divide a imagem em 3 bandas de cor e as adiciona em uma lista
    b, g, r = cv.split(img)
    ch = [b, g, r]

    # Percorre a lista de bandas de cor aplicando o algoritmo a cada uma delas
    for cor in range(len(ch)):
        m, n = ch[cor].shape
        f = np.copy(ch[cor]).astype("float")
        g = np.copy(ch[cor])

        for x in range(m):
            for y in range(n):
                if f[x, y] < 128:
                    g[x, y] = 0
                else:
                    g[x, y] = 1
                erro = f[x, y] - g[x, y] * 255

                # Verificacao para evitar que a propagacao do erro ultrapasse as 
                # dimensoes da imagem
                if 1 < x < m - 2 and y < n - 2:
                    # Propaga o erro aos vizinhos
                    f[x + 1, y]     = f[x + 1, y]     + (5/32) * erro
                    f[x + 2, y]     = f[x + 2, y]     + (3/32) * erro
                    f[x - 2, y + 1] = f[x - 2, y + 1] + (2/32) * erro
                    f[x - 1, y + 1] = f[x - 1, y + 1] + (4/32) * erro
                    f[x, y + 1]     = f[x, y + 1]     + (5/32) * erro
                    f[x + 1, y + 1] = f[x + 1, y + 1] + (4/32) * erro
                    f[x + 2, y + 1] = f[x + 2, y + 1] + (2/32) * erro
                    f[x - 1, y + 2] = f[x - 1, y + 2] + (2/32) * erro
                    f[x, y + 2]     = f[x, y + 2]     + (3/32) * erro
                    f[x + 1, y + 2] = f[x + 1, y + 2] + (2/32) * erro

        # Atualiza as bandas de cor apos o procedimento
        ch[cor] = g
    
    # Mescla as bandas de cor para formar a imagem resultante
    res = cv.merge(ch)
    print("Verificando imagem binária: {}\n".format(np.unique(res)))

    # Multiplica imagem resultante por 255 para permitir visualizacao
    return res * 255

# Aplica a difusao de erro de Sierra com percurso alternado para cada banda de uma imagem img e gera o resultado em res
def sierra_alt(img):
    print("Sierra alternado\n")
    # Divide a imagem em 3 bandas de cor e as adiciona em uma lista
    b, g, r = cv.split(img)
    ch = [b, g, r]

    # Percorre a lista de bandas de cor aplicando o algoritmo a cada uma delas
    for cor in range(len(ch)):
        m, n = ch[cor].shape
        f = np.copy(ch[cor]).astype("float")
        g = np.copy(ch[cor])

        for x in range(m):
            for y in range(n):
                if f[x, y] < 128:
                    g[x, y] = 0
                else:
                    g[x, y] = 1
                erro = f[x, y] - g[x, y] * 255

                # Verifica se uma linha e par ou impar para aplicar o percurso normal ou alternado
                if x % 2 == 0:
                    # Verificacao para evitar que a propagacao do erro ultrapasse as 
                    # dimensoes da imagem
                    if 1 < x < m - 2 and y < n - 2:
                        # Propaga o erro aos vizinhos
                        f[x + 1, y]     = f[x + 1, y]     + (5/32) * erro
                        f[x + 2, y]     = f[x + 2, y]     + (3/32) * erro
                        f[x - 2, y + 1] = f[x - 2, y + 1] + (2/32) * erro
                        f[x - 1, y + 1] = f[x - 1, y + 1] + (4/32) * erro
                        f[x, y + 1]     = f[x, y + 1]     + (5/32) * erro
                        f[x + 1, y + 1] = f[x + 1, y + 1] + (4/32) * erro
                        f[x + 2, y + 1] = f[x + 2, y + 1] + (2/32) * erro
                        f[x - 1, y + 2] = f[x - 1, y + 2] + (2/32) * erro
                        f[x, y + 2]     = f[x, y + 2]     + (3/32) * erro
                        f[x + 1, y + 2] = f[x + 1, y + 2] + (2/32) * erro
                else:
                    # Verificacao para evitar que a propagacao do erro ultrapasse as 
                    # dimensoes da imagem
                    if 1 < x < m - 2 and y < n - 2:
                        # Propaga o erro aos vizinhos
                        f[x - 1, y]     = f[x - 1, y]     + (5/32) * erro
                        f[x - 2, y]     = f[x - 2, y]     + (3/32) * erro
                        f[x + 2, y + 1] = f[x + 2, y + 1] + (2/32) * erro
                        f[x + 1, y + 1] = f[x + 1, y + 1] + (4/32) * erro
                        f[x, y + 1]     = f[x, y + 1]     + (5/32) * erro
                        f[x - 1, y + 1] = f[x - 1, y + 1] + (4/32) * erro
                        f[x - 2, y + 1] = f[x - 2, y + 1] + (2/32) * erro
                        f[x + 1, y + 2] = f[x + 1, y + 2] + (2/32) * erro
                        f[x, y + 2]     = f[x, y + 2]     + (3/32) * erro
                        f[x - 1, y + 2] = f[x - 1, y + 2] + (2/32) * erro

        # Atualiza as bandas de cor apos o procedimento
        ch[cor] = g
    
    # Mescla as bandas de cor para formar a imagem resultante
    res = cv.merge(ch)
    print("Verificando imagem binária: {}\n".format(np.unique(res)))

    # Multiplica imagem resultante por 255 para permitir visualizacao
    return res * 255

# Aplica a difusao de erro de Stucki para cada banda de uma imagem img e gera o resultado em res
def stucki(img):
    print("Stucki\n")
    # Divide a imagem em 3 bandas de cor e as adiciona em uma lista
    b, g, r = cv.split(img)
    ch = [b, g, r]

    # Percorre a lista de bandas de cor aplicando o algoritmo a cada uma delas
    for cor in range(len(ch)):
        m, n = ch[cor].shape
        f = np.copy(ch[cor]).astype("float")
        g = np.copy(ch[cor])

        for x in range(m):
            for y in range(n):
                if f[x, y] < 128:
                    g[x, y] = 0
                else:
                    g[x, y] = 1
                erro = f[x, y] - g[x, y] * 255

                # Verificacao para evitar que a propagacao do erro ultrapasse as 
                # dimensoes da imagem
                if 1 < x < m - 2 and y < n - 2:
                    # Propaga o erro aos vizinhos
                    f[x + 1, y]     = f[x + 1, y]     + (8/42) * erro
                    f[x + 2, y]     = f[x + 2, y]     + (4/42) * erro
                    f[x - 2, y + 1] = f[x - 2, y + 1] + (2/42) * erro
                    f[x - 1, y + 1] = f[x - 1, y + 1] + (4/42) * erro
                    f[x, y + 1]     = f[x, y + 1]     + (8/42) * erro
                    f[x + 1, y + 1] = f[x + 1, y + 1] + (4/42) * erro
                    f[x + 2, y + 1] = f[x + 2, y + 1] + (2/42) * erro
                    f[x - 2, y + 2] = f[x - 2, y + 2] + (1/42) * erro
                    f[x - 1, y + 2] = f[x - 1, y + 2] + (2/42) * erro
                    f[x, y + 2]     = f[x, y + 2]     + (4/42) * erro
                    f[x + 1, y + 2] = f[x + 1, y + 2] + (2/42) * erro
                    f[x + 2, y + 2] = f[x + 2, y + 2] + (1/42) * erro

        # Atualiza as bandas de cor apos o procedimento
        ch[cor] = g
    
    # Mescla as bandas de cor para formar a imagem resultante
    res = cv.merge(ch)
    print("Verificando imagem binária: {}\n".format(np.unique(res)))

    # Multiplica imagem resultante por 255 para permitir visualizacao
    return res * 255

# Aplica a difusao de erro de Stucki com percurso alternado para cada banda de uma imagem img e gera o resultado em res
def stucki_alt(img):
    print("Stucki alternado\n")
    # Divide a imagem em 3 bandas de cor e as adiciona em uma lista
    b, g, r = cv.split(img)
    ch = [b, g, r]

    # Percorre a lista de bandas de cor aplicando o algoritmo a cada uma delas
    for cor in range(len(ch)):
        m, n = ch[cor].shape
        f = np.copy(ch[cor]).astype("float")
        g = np.copy(ch[cor])

        for x in range(m):
            for y in range(n):
                if f[x, y] < 128:
                    g[x, y] = 0
                else:
                    g[x, y] = 1
                erro = f[x, y] - g[x, y] * 255

                # Verifica se uma linha e par ou impar para aplicar o percurso normal ou alternado
                if x % 2 == 0:
                    # Verificacao para evitar que a propagacao do erro ultrapasse as 
                    # dimensoes da imagem
                    if 1 < x < m - 2 and y < n - 2:
                        # Propaga o erro aos vizinhos
                        f[x + 1, y]     = f[x + 1, y]     + (8/42) * erro
                        f[x + 2, y]     = f[x + 2, y]     + (4/42) * erro
                        f[x - 2, y + 1] = f[x - 2, y + 1] + (2/42) * erro
                        f[x - 1, y + 1] = f[x - 1, y + 1] + (4/42) * erro
                        f[x, y + 1]     = f[x, y + 1]     + (8/42) * erro
                        f[x + 1, y + 1] = f[x + 1, y + 1] + (4/42) * erro
                        f[x + 2, y + 1] = f[x + 2, y + 1] + (2/42) * erro
                        f[x - 2, y + 2] = f[x - 2, y + 2] + (1/42) * erro
                        f[x - 1, y + 2] = f[x - 1, y + 2] + (2/42) * erro
                        f[x, y + 2]     = f[x, y + 2]     + (4/42) * erro
                        f[x + 1, y + 2] = f[x + 1, y + 2] + (2/42) * erro
                        f[x + 2, y + 2] = f[x + 2, y + 2] + (1/42) * erro
                else:
                    # Verificacao para evitar que a propagacao do erro ultrapasse as 
                    # dimensoes da imagem
                    if 1 < x < m - 2 and y < n - 2:
                        # Propaga o erro aos vizinhos
                        f[x - 1, y]     = f[x - 1, y]     + (8/42) * erro
                        f[x - 2, y]     = f[x - 2, y]     + (4/42) * erro
                        f[x + 2, y + 1] = f[x + 2, y + 1] + (2/42) * erro
                        f[x + 1, y + 1] = f[x + 1, y + 1] + (4/42) * erro
                        f[x, y + 1]     = f[x, y + 1]     + (8/42) * erro
                        f[x - 1, y + 1] = f[x - 1, y + 1] + (4/42) * erro
                        f[x - 2, y + 1] = f[x - 2, y + 1] + (2/42) * erro
                        f[x + 2, y + 2] = f[x + 2, y + 2] + (1/42) * erro
                        f[x + 1, y + 2] = f[x + 1, y + 2] + (2/42) * erro
                        f[x, y + 2]     = f[x, y + 2]     + (4/42) * erro
                        f[x - 1, y + 2] = f[x - 1, y + 2] + (2/42) * erro
                        f[x - 2, y + 2] = f[x - 2, y + 2] + (1/42) * erro

        # Atualiza as bandas de cor apos o procedimento
        ch[cor] = g
    
    # Mescla as bandas de cor para formar a imagem resultante
    res = cv.merge(ch)
    print("Verificando imagem binária: {}\n".format(np.unique(res)))

    # Multiplica imagem resultante por 255 para permitir visualizacao
    return res * 255

# Aplica a difusao de erro de Jarvis, Judice e Ninke para cada banda de uma imagem img e gera o resultado em res
def jjn(img):
    print("Jarvis-Judice-Ninke\n")
    # Divide a imagem em 3 bandas de cor e as adiciona em uma lista
    b, g, r = cv.split(img)
    ch = [b, g, r]

    # Percorre a lista de bandas de cor aplicando o algoritmo a cada uma delas
    for cor in range(len(ch)):
        m, n = ch[cor].shape
        f = np.copy(ch[cor]).astype("float")
        g = np.copy(ch[cor])

        for x in range(m):
            for y in range(n):
                if f[x, y] < 128:
                    g[x, y] = 0
                else:
                    g[x, y] = 1
                erro = f[x, y] - g[x, y] * 255

                # Verificacao para evitar que a propagacao do erro ultrapasse as 
                # dimensoes da imagem
                if 1 < x < m - 2 and y < n - 2:
                    # Propaga o erro aos vizinhos
                    f[x + 1, y]     = f[x + 1, y]     + (7/48) * erro
                    f[x + 2, y]     = f[x + 2, y]     + (5/48) * erro
                    f[x - 2, y + 1] = f[x - 2, y + 1] + (3/48) * erro
                    f[x - 1, y + 1] = f[x - 1, y + 1] + (5/48) * erro
                    f[x, y + 1]     = f[x, y + 1]     + (7/48) * erro
                    f[x + 1, y + 1] = f[x + 1, y + 1] + (5/48) * erro
                    f[x + 2, y + 1] = f[x + 2, y + 1] + (3/48) * erro
                    f[x - 2, y + 2] = f[x - 2, y + 2] + (1/48) * erro
                    f[x - 1, y + 2] = f[x - 1, y + 2] + (3/48) * erro
                    f[x, y + 2]     = f[x, y + 2]     + (5/48) * erro
                    f[x + 1, y + 2] = f[x + 1, y + 2] + (3/48) * erro
                    f[x + 2, y + 2] = f[x + 2, y + 2] + (1/48) * erro

        # Atualiza as bandas de cor apos o procedimento
        ch[cor] = g
    
    # Mescla as bandas de cor para formar a imagem resultante
    res = cv.merge(ch)
    print("Verificando imagem binária: {}\n".format(np.unique(res)))

    # Multiplica imagem resultante por 255 para permitir visualizacao
    return res * 255

# Aplica a difusao de erro de Jarvis, Judice e Ninke com percurso alternado para cada banda de uma imagem img e gera o resultado em res
def jjn_alt(img):
    print("Jarvis-Judice-Ninke alternado\n")
    # Divide a imagem em 3 bandas de cor e as adiciona em uma lista
    b, g, r = cv.split(img)
    ch = [b, g, r]

    # Percorre a lista de bandas de cor aplicando o algoritmo a cada uma delas
    for cor in range(len(ch)):
        m, n = ch[cor].shape
        f = np.copy(ch[cor]).astype("float")
        g = np.copy(ch[cor])

        for x in range(m):
            for y in range(n):
                if f[x, y] < 128:
                    g[x, y] = 0
                else:
                    g[x, y] = 1
                erro = f[x, y] - g[x, y] * 255

                # Verifica se uma linha e par ou impar para aplicar o percurso normal ou alternado
                if x % 2 == 0:
                    # Verificacao para evitar que a propagacao do erro ultrapasse as 
                    # dimensoes da imagem
                    if 1 < x < m - 2 and y < n - 2:
                        # Propaga o erro aos vizinhos
                        f[x + 1, y]     = f[x + 1, y]     + (7/48) * erro
                        f[x + 2, y]     = f[x + 2, y]     + (5/48) * erro
                        f[x - 2, y + 1] = f[x - 2, y + 1] + (3/48) * erro
                        f[x - 1, y + 1] = f[x - 1, y + 1] + (5/48) * erro
                        f[x, y + 1]     = f[x, y + 1]     + (7/48) * erro
                        f[x + 1, y + 1] = f[x + 1, y + 1] + (5/48) * erro
                        f[x + 2, y + 1] = f[x + 2, y + 1] + (3/48) * erro
                        f[x - 2, y + 2] = f[x - 2, y + 2] + (1/48) * erro
                        f[x - 1, y + 2] = f[x - 1, y + 2] + (3/48) * erro
                        f[x, y + 2]     = f[x, y + 2]     + (5/48) * erro
                        f[x + 1, y + 2] = f[x + 1, y + 2] + (3/48) * erro
                        f[x + 2, y + 2] = f[x + 2, y + 2] + (1/48) * erro

                else:
                    # Verificacao para evitar que a propagacao do erro ultrapasse as 
                    # dimensoes da imagem
                    if 1 < x < m - 2 and y < n - 2:
                        # Propaga o erro aos vizinhos
                        f[x - 1, y]     = f[x - 1, y]     + (7/48) * erro
                        f[x - 2, y]     = f[x - 2, y]     + (5/48) * erro
                        f[x + 2, y + 1] = f[x + 2, y + 1] + (3/48) * erro
                        f[x + 1, y + 1] = f[x + 1, y + 1] + (5/48) * erro
                        f[x, y + 1]     = f[x, y + 1]     + (7/48) * erro
                        f[x - 1, y + 1] = f[x - 1, y + 1] + (5/48) * erro
                        f[x - 2, y + 1] = f[x - 2, y + 1] + (3/48) * erro
                        f[x + 2, y + 2] = f[x + 2, y + 2] + (1/48) * erro
                        f[x + 1, y + 2] = f[x + 1, y + 2] + (3/48) * erro
                        f[x, y + 2]     = f[x, y + 2]     + (5/48) * erro
                        f[x - 1, y + 2] = f[x - 1, y + 2] + (3/48) * erro
                        f[x - 2, y + 2] = f[x - 2, y + 2] + (1/48) * erro

        # Atualiza as bandas de cor apos o procedimento
        ch[cor] = g
    
    # Mescla as bandas de cor para formar a imagem resultante
    res = cv.merge(ch)
    print("Verificando imagem binária: {}\n".format(np.unique(res)))

    # Multiplica imagem resultante por 255 para permitir visualizacao
    return res * 255