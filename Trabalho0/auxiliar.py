# Funcoes auxiliares

import cv2 as cv
import numpy as np

# exibir: exibe a imagem em uma janela e a salva em um arquivo se o usuario entrar "s", senão
# apenas continua a execucao
def exibir(janela,img,saida):
    cv.imshow(janela, img)
    k = cv.waitKey(0) & 0xFF

    if k == ord("s"):
        cv.imwrite(saida, img)

    cv.destroyWindow(janela)

# correcaoGamma: corrige o brilho da imagem de acordo com a power law transform
def correcaoGamma(img, gamma=1.0):
    invGamma = 1.0 / gamma
    # Utiliza uma tabela para mapear cada pixel e seu valor corrigido
    # permitindo execucao em tempo O(1)
    tabela = np.array([((i/255.0) ** invGamma) * 255
                       for i in np.arange(0,256)]).astype("uint8")

    return cv.LUT(img,tabela)