''' Processamento de imagens
    Trabalho 4

    Aluno: Bruno Mendes Richau
    RA: 157743

    Modulo para recuperar a informacao binaria da imagem e gerar a
    mensagem de texto 
    
    Uso: python decodificar.py imagem_saida.png plano_bits texto_saida.txt '''

import cv2 as cv
import sys, auxiliar4 as a

# Verifica se usuario forneceu a quantidade correta de argumentos
if len(sys.argv) != 4:
    print("Uso: python decodificar.py imagem_saida.png plano_bits texto_saida.txt")
    sys.exit()
else:
    # Carrega imagem codificada
    inp = sys.argv[1]
    print("Imagem codificada: {}".format(inp))
    img = cv.imread(inp, 1)

    # Carrega o plano de bits
    plano = sys.argv[2]
    print("Plano: {}".format(plano))

    # Carrega o nome do arquivo de saida onde sera decodificada a mensagem
    nomeSaida = sys.argv[3]
    print("Arquivo de saida: {}\n".format(nomeSaida))

    # Verifica se argumentos de entrada sao validos
    if img is None:
        sys.exit("Nao foi possivel ler a imagem")
    else:
        a.exibir("Codificada", img, "{}".format(inp), 0)

        decMsg = a.decodeMsg(img)
        print("Mensagem decodificada:\n{}".format(decMsg))