# Processamento de imagens
# Trabalho 0

# Importar OpenCV, scikit-image, Numpy e Matplotlib
import cv2 as cv
import skimage
import numpy as np
from matplotlib import pyplot as plt
import sys

print(cv.__version__)
print(skimage.__version__)

# 1.1 Transformacao de intensidade
# a) Imagem original
img = cv.imread("city.png", 0)

if img is None:
    sys.exit("Could not read the image.")

cv.imshow("Original", img)
k = cv.waitKey(0) & 0xFF

# cv.destroyWindow("Original")

# b) Negativo da imagem
imgNeg = cv.bitwise_not(img)
cv.imshow("Negativo", imgNeg)
k = cv.waitKey(0) & 0xFF

if k == ord("s"):
    cv.imwrite("city1_1b.png", imgNeg)

cv.destroyWindow("Negativo")

# c) Espelhamento vertical
imgFlip = cv.flip(img,0)
cv.imshow("Espelhamento vertical", imgFlip)
k = cv.waitKey(0) & 0xFF

if k == ord("s"):
    cv.imwrite("city1_1c.png", imgFlip)

cv.destroyWindow("Espelhamento vertical")

# d) Imagem transformada
print(img[0,0])
print(img.shape)

rows,cols = img.shape
g = img

for i in range(rows):
    for j in range(cols):
        f = img[i,j]
        v = ((100*f)/255)+100
        g.itemset((i,j),v)

cv.imshow("Imagem transformada", g)
k = cv.waitKey(0) & 0xFF

if k == ord("s"):
    cv.imwrite("city1_1d.png", g)

cv.destroyWindow("Imagem transformada")

# e) Linhas pares invertidas

cv.destroyAllWindows()