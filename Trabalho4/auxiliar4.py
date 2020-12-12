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
def codeMsg(img, msg):

    # Calcula o numero maximo de bytes a codificar
    bytesNum = img.shape[0] * img.shape[1] * 3 // 8
    print("Numero de bytes disponiveis:", bytesNum)

    # Verifica se numero de bytes da mensagem cabe no numero de bytes
    # disponivel na imagem
    if len(msg) > bytesNum:
        raise ValueError("Nao ha bytes suficientes na imagem para codificar a mensagem \n{}\n que possui {} bytes em uma imagem que possui {}".format(msg, len(msg), bytesNum))
  
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
                pixel[0] = int(b[:-1] + binMsg[indexMsg], 2)
                indexMsg += 1
            if indexMsg < lenMsg:
                # Substitui bit menos significativo da banda
                # de cor verde do pixel por um bit da mensagem e
                # converte o novo valor para um inteiro decimal
                pixel[1] = int(g[:-1] + binMsg[indexMsg], 2)
                indexMsg += 1
            if indexMsg < lenMsg:
                # Substitui bit menos significativo da banda
                # de cor vermelha do pixel por um bit da mensagem e
                # converte o novo valor para um inteiro decimal
                pixel[2] = int(r[:-1] + binMsg[indexMsg], 2)
                indexMsg += 1
            # Encerra o processamento quando toda a mensagem for codificada
            if indexMsg >= lenMsg:
                break

    return img

def decodeMsg(img):

    # String para armezar os bits extraidos da imagem
    binMsg = ""

    # Percorre os pixels de cada linha da imagem
    for linha in img:
        for pixel in linha:
            # Converte cada banda de cor de um pixel para binario de 8 bits
            b, g, r = convBin(pixel)
            # Extrai o bit menos significativo da banda azul e o adiciona
            # a mensagem em binario
            binMsg += b[-1]
            # Extrai o bit menos significativo da banda verde e o adiciona
            # a mensagem em binario
            binMsg += g[-1]
            # Extrai o bit menos significativo da banda vermelha e o adiciona
            # a mensagem em binario
            binMsg += r[-1]

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
    f = open("saida.txt", "w+")
    f.write(res)
    f.close()

    if path.exists("saida.txt"):
        print("A mensagem decodificada foi escrita no arquivo {}".format("saida.txt"))
    else:
        sys.exit("Nao foi possivel escrever o arquivo {}\n".format("saida.txt"))

    return res