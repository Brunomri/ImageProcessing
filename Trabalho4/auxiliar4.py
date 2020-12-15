# Funcoes auxiliares

import cv2 as cv
import numpy as np
import sys
import os.path
from os import path

# exibir: exibe a imagem em uma janela e a salva em um arquivo se o usuario entrar "s", senão
# apenas continua a execucao
def exibir(janela,img,saida,close):
    print("Exibindo {}".format(saida))
    cv.imshow(janela, img)
    k = cv.waitKey(0) & 0xFF

    if k == ord("s"):
        print("Gerando arquivo {}".format(saida))
        cv.imwrite(saida, img)

    print()

    # Parametro close == 1 fecha apenas a janela selecionada
    # Parametro close == 2 fecha todas as janelas
    if close == 1:
        cv.destroyWindow(janela)
    elif close == 2:
        cv.destroyAllWindows()
    else:
        return

# convBin: Converte diversos tipos de variaveis para binario com 8 bits
def convBin(msg):
    if type(msg) == str:
        return ''.join([format(ord(i), "08b") for i in msg ])
    elif type(msg) == bytes or type(msg) == np.ndarray:
        return [format(i, "08b") for i in msg ]
    elif type(msg) == int or type(msg) == np.uint8:
        return format(msg, "08b")
    else:
        raise TypeError("Tipo nao suportado")

# codeMsg: Codifica a mensagem nos bits menos significativos de cada banda de cor
# de um pixel da imagem de entrada
def codeMsg(img, msg, plano):

    # Calcula o numero maximo de bytes a codificar
    bytesNum = img.shape[0] * img.shape[1] * 3 // 8
    print("Numero de bytes disponiveis: {}".format(bytesNum))

    # Verifica se numero de bytes da mensagem cabe no numero de bytes
    # disponivel na imagem
    if len(msg) > bytesNum:
        raise ValueError("Nao ha bytes suficientes na imagem para codificar a mensagem \n{}\n que possui {} bytes em uma imagem que possui {}".format(msg, len(msg), bytesNum))
    print("Numero de bytes da mensagem: {}".format(len(msg)))
  
    # Adiciona a mensagem o delimitador de fim de cadeia
    msg += "#####"

    # Indice utilizado para percorre a mensagem
    indexMsg = 0
    # Converte mensagem para binario de 8 bits
    binMsg = convBin(msg)
    # Obtem o comprimento da mensagem
    lenMsg = len(binMsg)

    # Percorre os pixels de cada linha da imagem
    for linha in img:
        for pixel in linha:
            # Converte cada banda de cor de um pixel para binario de 8 bits
            b, g, r = convBin(pixel)
            # Modifica o bit menos significativo da imagem se ainda houve caracteres
            # a processar na mensagem
            if indexMsg < lenMsg:
                # Substitui bit menos significativo da banda
                # de cor azul do pixel por um bit da mensagem e
                # converte o novo valor para um inteiro decimal
                #pixel[0] = int(b[:-1] + binMsg[indexMsg], 2)
                pixel[0] = int(b[:(7 - plano)] + binMsg[indexMsg] + b[(7 - plano):-1], 2)
                indexMsg += 1
            if indexMsg < lenMsg:
                # Substitui bit menos significativo da banda
                # de cor verde do pixel por um bit da mensagem e
                # converte o novo valor para um inteiro decimal
                #pixel[1] = int(g[:-1] + binMsg[indexMsg], 2)
                pixel[1] = int(g[:(7 - plano)] + binMsg[indexMsg] + g[(7 - plano):-1], 2)
                indexMsg += 1
            if indexMsg < lenMsg:
                # Substitui bit menos significativo da banda
                # de cor vermelha do pixel por um bit da mensagem e
                # converte o novo valor para um inteiro decimal
                #pixel[2] = int(r[:-1] + binMsg[indexMsg], 2)
                pixel[2] = int(r[:(7 - plano)] + binMsg[indexMsg] + r[(7 - plano):-1], 2)
                indexMsg += 1
            # Encerra o processamento quando toda a mensagem for codificada
            if indexMsg >= lenMsg:
                break

    return img

def decodeMsg(img, nomeSaida, plano):

    # String para armezar os bits extraidos da imagem
    binMsg = ""

    # Percorre os pixels de cada linha da imagem
    for linha in img:
        for pixel in linha:
            # Converte cada banda de cor de um pixel para binario de 8 bits
            b, g, r = convBin(pixel)
            # Extrai o bit menos significativo da banda azul e o adiciona
            # a mensagem em binario
            #binMsg += b[-1]
            binMsg += b[7 - plano]
            # Extrai o bit menos significativo da banda verde e o adiciona
            # a mensagem em binario
            #binMsg += g[-1]
            binMsg += g[7 - plano]
            # Extrai o bit menos significativo da banda vermelha e o adiciona
            # a mensagem em binario
            #binMsg += r[-1]
            binMsg += r[7 - plano]

    # Agrupa a mensagem binaria em 8 bits para permitir conversao em
    # caracteres ASCII
    bytesMsg = [binMsg[i: i+8] for i in range(0, len(binMsg), 8) ]

    # Converte os bytes da mensagem em caracteres até encontrar o
    # delimitador de final de cadeia
    decodedMsg = ""
    for byte in bytesMsg:
        decodedMsg += chr(int(byte, 2))
        if decodedMsg[-5:] == "#####":
            break
    #print(decodedMsg)

    # Remove o delimitador de fim de cadeia e retorna a mensagem
    res = decodedMsg[:-5]

    # Cria uma arquivo de texto para a mensagem decodificada e
    # retorna o resultado ao programa principal
    f = open(nomeSaida, "w+")
    f.write(res)
    f.close()

    if path.exists(nomeSaida):
        print("A mensagem decodificada foi escrita no arquivo {}\n".format(nomeSaida))
    else:
        sys.exit("Nao foi possivel escrever o arquivo {}\n".format(nomeSaida))

    return res

# getPlano: cria uma máscara para obter um determinado plano de bits de uma imagem
def getPlano(img, plano):
    mask = np.full((img.shape[0], img.shape[1]), 2 ** plano, np.uint8)
    t = cv.bitwise_and(mask, img)
    # Aumentar a intensidade dos pixels
    r = t * 255
    return r

def exibirPlanos(img, inp):
    b, g, r = cv.split(img)
    
    exibir("Plano 0 azul", getPlano(b, 0), "b_p0_{}".format(inp), 0)
    exibir("Plano 1 azul", getPlano(b, 1), "b_p1_{}".format(inp), 0)
    exibir("Plano 2 azul", getPlano(b, 2), "b_p2_{}".format(inp), 0)
    #exibir("Plano 4 azul", getPlano(b, 4), "b_p4_{}".format(inp), 0)
    exibir("Plano 7 azul", getPlano(b, 7), "b_p7_{}".format(inp), 0)
    #cv.destroyAllWindows()

    exibir("Plano 0 verde", getPlano(g, 0), "g_p0_{}".format(inp), 0)
    exibir("Plano 1 verde", getPlano(g, 1), "g_p1_{}".format(inp), 0)
    exibir("Plano 2 verde", getPlano(g, 2), "g_p2_{}".format(inp), 0)
    #exibir("Plano 4 verde", getPlano(g, 4), "g_p4_{}".format(inp), 0)
    exibir("Plano 7 verde", getPlano(g, 7), "g_p7_{}".format(inp), 0)
    #cv.destroyAllWindows()

    exibir("Plano 0 vermelho", getPlano(r, 0), "r_p0_{}".format(inp), 0)
    exibir("Plano 1 vermelho", getPlano(r, 1), "r_p1_{}".format(inp), 0)
    exibir("Plano 2 vermelho", getPlano(r, 2), "r_p2_{}".format(inp), 0)
    #exibir("Plano 4 vermelho", getPlano(r, 4), "r_p4_{}".format(inp), 0)
    exibir("Plano 7 vermelho", getPlano(r, 7), "r_p7_{}".format(inp), 0)
    #cv.destroyAllWindows()