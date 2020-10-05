# Processamento de imagens
# Trabalho 0

# Aluno: Bruno Mendes Richau
# RA: 157743

import cv2 as cv
import sys, modulo1 as m1, modulo2 as m2, modulo3 as m3, modulo4 as m4, modulo5 as m5

# Verifica se usuario forneceu os argumentos corretamente
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

    # Decide qual modulo sera executado de acordo com a entrada
    if img is None:
        sys.exit("Nao foi possivel ler a imagem")
    if questao == "1":
        print("Questao 1")
        m1.questao1(img)
    elif questao == "2":
        print("Questao 2")
        m2.questao2(img)
    elif questao == "3":
        m3.questao3(img)
        print("Questao 3")
    elif questao == "4":
        print("Questao 4")
        m4.questao4(img)
    else:
        print("Questao 5")
        m5.questao5(img)