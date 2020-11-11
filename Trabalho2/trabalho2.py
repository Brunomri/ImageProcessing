# Processamento de imagens
# Trabalho 2

# Aluno: Bruno Mendes Richau
# RA: 157743

import cv2 as cv
import sys, auxiliar2 as a

# Verifica se usuario forneceu os argumentos corretamente
if len(sys.argv) != 2:
    print("Uso: trabalho1.py <imagem.png>")
    sys.exit()
else:
    inp = sys.argv[1]
    print("Imagem original: ", inp)
    img = cv.imread(inp, 1)

    # Decide qual filtro sera executado de acordo com a entrada
    if img is None:
        sys.exit("Nao foi possivel ler a imagem")
    else:
        a.exibir("Original", img, "{}".format(inp), 0)

        r1 = a.fs(img)
        a.exibir("Floyd-Steinberg", r1, "{}".format(inp), 0)
        print("R1", r1)

        cv.destroyAllWindows()