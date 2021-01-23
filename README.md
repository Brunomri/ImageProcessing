# MC920A/MO443A - Introdução ao Processamento Digital de Imagem
## Unicamp - 2º semestre de 2020

## Atividades variadas de Processamento de Imagens

### Descrição

Projeto contendo 5 atividades de Processamento de Imagens:
- Trabalho 0: transformação de intensidade, ajuste de brilho, plano de bits, mosaico e combinação de imagens
- Trabalho 1: filtragem no domínio espacial via operação de convolução
- Trabalho 2: técnicas de meios-tons com difusão de erro
- Trabalho 3: métodos de limiarização global e local
- Trabalho 4: técnica de esteganografia

### Utilização

O projeto foi desenvolvido em Python e requer as bibliotecas OpenCV, Numpy, scikit-image e Matplotlib, que podem ser
facilmente instaladas por um gerenciador de pacotes como o PIP ou Conda. Cada atividade possui um diretório específico
dentro do projeto e nele estão os arquivos Python principais, auxiliares e algumas imagem como exemplo para execução. Veja
abaixo como executar o processamento referente a cada trabalho.

#### Trabalho 0

```
python trabalho0.py <imagem.png> <questao>
```

Parâmetros de execução:
- imagem.png: caminho para um arquivo de imagem de entrada no formato .png
- questao: número de 1 a 5 referente ao processamento a ser aplicado, onde 1 = transformação de intensidade, 2 = ajuste de brilho,
3 = plano de bits, 4 = mosaico e 5 = combinação de imagens

#### Trabalho 1

```
python trabalho1.py <imagem.png>
```

Parâmetros de execução:
- imagem.png: caminho para um arquivo de imagem de entrada no formato .png

#### Trabalho 2

```
python trabalho1.py <imagem.png>
```

Parâmetros de execução:
- imagem.png: caminho para um arquivo de imagem de entrada no formato .png

#### Trabalho 3

```
python trabalho1.py <imagem.png>
```

Parâmetros de execução:
- imagem.png: caminho para um arquivo de imagem de entrada no formato .png

#### Trabalho 4

Para codificar o texto de um arquivo .txt em nos pixels de uma imagem .png:

```
python codificar.py imagem_entrada.png texto_entrada.txt plano_bits imagem_saida.png
```

Parâmetros de execução:
- imagem_entrada.png: caminho para um arquivo de imagem de entrada no formato .png
- texto_entrada.txt: caminho para um arquivo de texto de entrada no formato .txt
- plano_bits: número de 0 a 7 referente a qual plano de bits da imagem o texto será inserido
- imagem_saida.png: nome do arquivo de imagem de saída no formato .png que será gerado contendo o texto codificado, salvo no subdiretório Trabalho4

Para decodificar o texto escondido nos pixels de uma imagem .png e salvá-lo em um arquivo .txt:

```
python decodificar.py imagem_saida.png plano_bits texto_saida.txt
```

Parâmetros de execução:
- imagem_saida.png: caminho para um arquivo de imagem no formato .png que foi gerado pelo processo de codificação anterior
- plano_bits: número de 0 a 7 referente a qual plano de bits da imagem foi usado durante a etapa de codificação
- texto_saida.txt: nome do arquivo de texto de saída no formato .txt que será gerado contendo o texto decodificado, deve conter o mesmo
texto do arquivo texto_entrada.txt fornecido na etapa de codificação, salvo no subdiretório Trabalho4