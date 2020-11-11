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

        #r1 = a.fs(img)
        #a.exibir("Floyd-Steinberg", r1, "fs_{}".format(inp), 0)

        #r2 = a.fs_alt(img)
        #a.exibir("Floyd-Steinberg alternado", r2, "fs_alt_{}".format(inp), 0)

        #r3 = a.sa(img)
        #a.exibir("Stevenson-Arce", r3, "sa_{}".format(inp), 0)

        #r4 = a.sa_alt(img)
        #a.exibir("Stevenson-Arce alternado", r4, "sa_alt_{}".format(inp), 0)

        #r5 = a.burkes(img)
        #a.exibir("Burkes", r5, "burkes_{}".format(inp), 0)

        #r6 = a.burkes_alt(img)
        #a.exibir("Burkes alternado", r6, "burkes_alt_{}".format(inp), 0)

        r7 = a.sierra(img)
        a.exibir("Sierra", r7, "sierra_{}".format(inp), 0)

        cv.destroyAllWindows()