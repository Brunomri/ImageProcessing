# Processamento de imagens
# Trabalho 0

# Aluno: Bruno Mendes Richau
# RA: 157743

import cv2 as cv
import sys, modulo1 as m1

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
        m1.questao1(img)
    elif questao == "2":
        print("Questao 2")
    elif questao == "3":
        print("Questao 3")
    elif questao == "4":
        print("Questao 4")
    else:
        print("Questao 5")