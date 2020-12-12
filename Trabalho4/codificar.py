''' Processamento de imagens
    Trabalho 4

    Aluno: Bruno Mendes Richau
    RA: 157743

    Modulo para converter os caracteres de uma mensagem para sua codificacao ASCII correspondente
    e alterar os bits menos significativos da imagem com os bits da mensagem 
    
    Uso: python codificar.py imagem_entrada.png texto_entrada.txt plano_bits imagem_saida.png '''

import cv2 as cv
import sys, auxiliar4 as a

# Verifica se usuario forneceu a quantidade correta de argumentos
if len(sys.argv) != 5:
    print("Uso: python codificar.py imagem_entrada.png texto_entrada.txt plano_bits imagem_saida.png")
    sys.exit()
else:
    # Carrega imagem de entrada
    inp = sys.argv[1]
    print("Imagem original: {}".format(inp))
    img = cv.imread(inp, 1)

    # Carrega o texto da mensagem
    print("Arquivo de entrada: {}".format(sys.argv[2]))
    f = open(sys.argv[2], "r")
    msg = f.read()
    f.close()
    print("Texto de entrada:\n{}".format(msg))

    # Carrega o plano de bits
    plano = sys.argv[3]
    print("Plano: {}".format(plano))

    # Carrega o nome da imagem de saida onde sera armazenada a mensagem
    nomeSaida = sys.argv[4]
    print("Imagem de saida: {}\n".format(nomeSaida))

    # Verifica se argumentos de entrada sao validos
    if img is None:
        sys.exit("Nao foi possivel ler a imagem")
    else:
        a.exibir("Original", img, "{}".format(inp), 0)

        msgImg = a.codeMsg(img, msg)
        a.exibir("Codificada", msgImg, "{}".format(nomeSaida), 0)