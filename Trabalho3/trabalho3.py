# Processamento de imagens
# Trabalho 3

# Aluno: Bruno Mendes Richau
# RA: 157743

import cv2 as cv
import sys, auxiliar3 as a

# Verifica se usuario forneceu os argumentos corretamente
if len(sys.argv) != 2:
    print("Uso: trabalho1.py <imagem.pgm>")
    sys.exit()
else:
    inp = sys.argv[1]
    print("Imagem original: ", inp)
    img = cv.imread(inp, 0)

    if img is None:
        sys.exit("Nao foi possivel ler a imagem")
    else:
        a.exibir("Original", img, "{}".format(inp), 0)
        a.histograma(img, titulo = "Original", rotulo_x = "Intensidade", rotulo_y = "Pixels")
        a.otsu(img, inp)
        a.bernsen(img, inp)
        a.niblack(img, inp)
        a.sauvola(img, inp, k = -0.35)
        a.more(img, inp, k = -0.5)
        a.contrast(img, inp)
        a.mean(img, inp)