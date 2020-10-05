# Processamento de imagens
# Trabalho 0
# 1.5 Combinacao de imagens

import cv2 as cv
import numpy as np
import sys, auxiliar as a

def questao5(img, img2):

    # a) Imagem A
    a.exibir("Original A",img,"original5a.png")

    # b) Imagem B
    a.exibir("Original B",img2,"original5b.png")

    # c) Combinar 0.2*A + 0.8*B
    alpha = 0.2
    beta = (1 - alpha)
    res = cv.addWeighted(img, alpha, img2, beta, 0.0)
    a.exibir("0.2*A + 0.8*B", res, "comb1_5c")

    # d) Combinar 0.5*A + 0.5*B
    alpha = 0.5
    beta = (1 - alpha)
    res = cv.addWeighted(img, alpha, img2, beta, 0.0)
    a.exibir("0.5*A + 0.5*B", res, "comb1_5d")

    # e) Combinar 0.8*A + 0.2*B
    alpha = 0.8
    beta = (1 - alpha)
    res = cv.addWeighted(img, alpha, img2, beta, 0.0)
    a.exibir("0.8*A + 0.2*B", res, "comb1_5e")

    cv.destroyAllWindows()