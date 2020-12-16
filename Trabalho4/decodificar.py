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
    sys.exit("Uso: python decodificar.py imagem_saida.png plano_bits texto_saida.txt")
else:
    # Carrega imagem codificada
    inp = sys.argv[1]
    img = cv.imread(inp, 1)

    if img is None:
        sys.exit("Erro: Nao foi possivel ler a imagem {}\n".format(inp))
    else:
        print("Imagem codificada: {}".format(inp))

    # Carrega o plano de bits
    plano = int(sys.argv[2])
    
    if not 0 <= plano <= 7:
        sys.exit("Erro: O plano deve estar entre 0 e 7 inclusive. O plano {} nao faz parte da imagem.\n".format(plano))
    else:
        print("Plano: {}".format(plano))

    # Carrega o nome do arquivo de saida onde sera decodificada a mensagem
    nomeSaida = sys.argv[3]
    print("Arquivo de saida: {}\n".format(nomeSaida))

    # Decodifica imagem
    decMsg = a.decodeMsg(img, nomeSaida, plano)
    a.exibir("Codificada", img, "{}".format(inp), 0)
    print("Mensagem decodificada:\n{}\n".format(decMsg))

    # Exibe os planos de bits
    a.exibirPlanos(img, inp, [0, 1, 2, 7])