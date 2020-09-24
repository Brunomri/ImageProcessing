# Processamento de imagens
# Trabalho 0

# Importar OpenCV e scikit-image
import cv2 as cv
import skimage
import sys

print(cv.__version__)
print(skimage.__version__)

# 1.1 Transformacao de intensidade
# a) Imagem original
img = cv.imread("city.png")

if img is None:
    sys.exit("Could not read the image.")

cv.imshow("Original", img)
k = cv.waitKey(0)

# b) Negativo da imagem
imgNeg = cv.bitwise_not(img)
cv.imshow("Negativo", imgNeg)
k = cv.waitKey(0)