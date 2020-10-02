# Processamento de imagens
# Trabalho 0
# 1.3 Planos de bits

import cv2 as cv
import numpy as np
import sys, auxiliar as a

def questao3(img):

    # a) Imagem original
    a.exibir("Original",img,"original2.png")

    # b) Plano de bit 0
    r = a.getPlano(img,0)
    a.exibir("Plano de bit 0",r,"baboon1_3b.png")

    # c) Plano de bit 4
    r = a.getPlano(img,4)
    a.exibir("Plano de bit 4",r,"baboon1_3c.png")

    # d) Plano de bit 7
    r = a.getPlano(img,7)
    a.exibir("Plano de bit 7",r,"baboon1_3d.png")