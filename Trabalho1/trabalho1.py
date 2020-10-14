# Processamento de imagens
# Trabalho 1

# Aluno: Bruno Mendes Richau
# RA: 157743

import cv2 as cv
import sys, auxiliar1 as a

# Verifica se usuario forneceu os argumentos corretamente
if len(sys.argv) != 2:
    print("Uso: trabalho1.py <imagem.png>")
    sys.exit()
else:
    inp = sys.argv[1]
    print("Imagem: ", inp)
    img = cv.imread(inp, 0)

    # Decide qual filtro sera executado de acordo com a entrada
    if img is None:
        sys.exit("Nao foi possivel ler a imagem")
    else:
        a.exibir("Original",img,"original.png",0)
        h = a.criaFiltros(filtro)
        res = cv.filter2D(img, -1, h)
        a.exibir("{} ".format(filtro), res, "{}.png".format(filtro), 2)