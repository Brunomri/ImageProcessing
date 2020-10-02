# Processamento de imagens
# Trabalho 0
# 1.2 Ajuste de brilho

import cv2 as cv
import sys, auxiliar as a

def questao2(img):

    # a) Imagem original
    a.exibir("Original",img,"original2.png")

    # b) gamma = 1.5
    r = a.correcaoGamma(img,1.5)
    a.exibir("Gamma 1.5",r,"baboon1_2b.png")

    # c) gamma = 2.5
    r = a.correcaoGamma(img,2.5)
    a.exibir("Gamma 2.5",r,"baboon1_2c.png")

    # d) gamma = 3.5
    r = a.correcaoGamma(img,3.5)
    a.exibir("Gamma 3.5",r,"baboon1_2d.png")

    cv.destroyAllWindows()