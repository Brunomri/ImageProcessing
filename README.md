# MC920A/MO443A - Introdu��o ao Processamento Digital de Imagem
## Unicamp - 2� semestre de 2020

## Atividades variadas de Processamento de Imagens

### Descri��o

Projeto contendo 5 atividades de Processamento de Imagens:
- Trabalho 0: transforma��o de intensidade, ajuste de brilho, plano de bits, mosaico e combina��o de imagens
- Trabalho 1: filtragem no dom�nio espacial via opera��o de convolu��o
- Trabalho 2: t�cnicas de meios-tons com difus�o de erro
- Trabalho 3: m�todos de limiariza��o global e local
- Trabalho 4: t�cnica de esteganografia

### Utiliza��o

O projeto foi desenvolvido em Python e requer as bibliotecas OpenCV, Numpy, scikit-image e Matplotlib, que podem ser
facilmente instaladas por um gerenciador de pacotes como o PIP ou Conda. Cada atividade possui um diret�rio espec�fico
dentro do projeto e nele est�o os arquivos Python principais, auxiliares e algumas imagem como exemplo para execu��o. Veja
abaixo como executar o processamento referente a cada trabalho.

#### Trabalho 0

```
python trabalho0.py <imagem.png> <questao>
```

Par�metros de execu��o:
- imagem.png: caminho para um arquivo de imagem de entrada no formato .png
- questao: n�mero de 1 a 5 referente ao processamento a ser aplicado, onde 1 = transforma��o de intensidade, 2 = ajuste de brilho,
3 = plano de bits, 4 = mosaico e 5 = combina��o de imagens

#### Trabalho 1

```
python trabalho1.py <imagem.png>
```

Par�metros de execu��o:
- imagem.png: caminho para um arquivo de imagem de entrada no formato .png

#### Trabalho 2

```
python trabalho1.py <imagem.png>
```

Par�metros de execu��o:
- imagem.png: caminho para um arquivo de imagem de entrada no formato .png

#### Trabalho 3

```
python trabalho1.py <imagem.png>
```

Par�metros de execu��o:
- imagem.png: caminho para um arquivo de imagem de entrada no formato .png

#### Trabalho 4

Para codificar o texto de um arquivo .txt em nos pixels de uma imagem .png:

```
python codificar.py imagem_entrada.png texto_entrada.txt plano_bits imagem_saida.png
```

Par�metros de execu��o:
- imagem_entrada.png: caminho para um arquivo de imagem de entrada no formato .png
- texto_entrada.txt: caminho para um arquivo de texto de entrada no formato .txt
- plano_bits: n�mero de 0 a 7 referente a qual plano de bits da imagem o texto ser� inserido
- imagem_saida.png: nome do arquivo de imagem de sa�da no formato .png que ser� gerado contendo o texto codificado, salvo no subdiret�rio Trabalho4

Para decodificar o texto escondido nos pixels de uma imagem .png e salv�-lo em um arquivo .txt:

```
python decodificar.py imagem_saida.png plano_bits texto_saida.txt
```

Par�metros de execu��o:
- imagem_saida.png: caminho para um arquivo de imagem no formato .png que foi gerado pelo processo de codifica��o anterior
- plano_bits: n�mero de 0 a 7 referente a qual plano de bits da imagem foi usado durante a etapa de codifica��o
- texto_saida.txt: nome do arquivo de texto de sa�da no formato .txt que ser� gerado contendo o texto decodificado, deve conter o mesmo
texto do arquivo texto_entrada.txt fornecido na etapa de codifica��o, salvo no subdiret�rio Trabalho4