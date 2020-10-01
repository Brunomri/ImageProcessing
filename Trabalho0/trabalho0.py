# Processamento de imagens
# Trabalho 0

# Aluno: Bruno Mendes Richau
# RA: 157743

# Importar OpenCV, scikit-image, Numpy e Matplotlib
import cv2 as cv
import skimage
import numpy as np
from matplotlib import pyplot as plt
import sys, modulo1

# Funcoes auxiliares

# exibir: exibe a imagem em uma janela e a salva em um arquivo se o usuario entrar "s", senão
# apenas continua a execucao
def exibir(janela,img,saida):
    cv.imshow(janela, img)
    k = cv.waitKey(0) & 0xFF

    if k == ord("s"):
        cv.imwrite(saida, img)

    cv.destroyWindow(janela)

if len(sys.argv) != 3:
    print("Uso: trabalho0.py <imagem.png> <questao>")
    sys.exit()
else:
    if not "1" <= sys.argv[2] <= "5":
        print("Insira uma questao de 1 a 5")
        sys.exit()

    input = sys.argv[1]
    questao = sys.argv[2]

    img = cv.imread(input, 0)
    if img is None:
        sys.exit("Nao foi possivel ler a imagem")
    if questao == "1":
        print("Questao 1")
        modulo1.questao1(img)
    elif questao == "2":
        print("Questao 2")
    elif questao == "3":
        print("Questao 3")
    elif questao == "4":
        print("Questao 4")
    else:
        print("Questao 5")