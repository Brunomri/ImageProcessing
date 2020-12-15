''' Processamento de imagens
    Trabalho 4

    Aluno: Bruno Mendes Richau
    RA: 157743

    Modulo para converter os caracteres de uma mensagem para sua codificacao ASCII correspondente
    e alterar os bits menos significativos da imagem com os bits da mensagem 
    
    Uso: python codificar.py imagem_entrada.png texto_entrada.txt plano_bits imagem_saida.png '''

import cv2 as cv
import sys, auxiliar4 as a
import os.path
from os import path

# Verifica se usuario forneceu a quantidade correta de argumentos
if len(sys.argv) != 5:
    sys.exit("Uso: python codificar.py imagem_entrada.png texto_entrada.txt plano_bits imagem_saida.png")
else:
    # Carrega imagem de entrada
    inp = sys.argv[1]
    img = cv.imread(inp, 1)

    if img is None:
        sys.exit("Erro: Nao foi possivel ler a imagem {}\n".format(inp))
    else:
        print("Imagem original: {}".format(inp))

    # Carrega o texto da mensagem
    entrada = sys.argv[2]

    msg = ""
    if path.exists(entrada):
        f = open(entrada, "r")
        print("Arquivo de entrada: {}".format(entrada))
        msg = f.read()
        f.close()
        print("Texto de entrada:\n{}".format(msg))
    else:
        sys.exit("Erro: O arquivo {} nao existe\n".format(entrada))

    # Carrega o plano de bits
    plano = int(sys.argv[3])

    if not 0 <= plano <= 7:
        sys.exit("Erro: O plano deve estar entre 0 e 7 inclusive. O plano {} nao faz parte da imagem.\n".format(plano))
    else:
        print("Plano: {}".format(plano))

    # Carrega o nome da imagem de saida onde sera armazenada a mensagem
    nomeSaida = sys.argv[4]
    print("Imagem de saida: {}\n".format(nomeSaida))

    a.exibir("Original", img, "{}".format(inp), 0)

    msgImg = a.codeMsg(img, msg, plano)
    a.exibir("Codificada", msgImg, "{}".format(nomeSaida), 0)