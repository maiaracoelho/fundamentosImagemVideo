#!/usr/bin/env python

from PIL import Image
import os
import time
import sys
import string
import MySQLdb
import math
from datetime import datetime, timedelta
from operator import itemgetter
import matplotlib.pyplot as plt
import numpy as np


def openImage(path):
    return Image.open(path)


def saveImage(img, path):
    return img.save(path)


'''Funcao para gerar histograma de uma imagem'''        
def imprimir_arquivo(vetor, arquivo): 
    
    arqCount = open(arquivo, 'w')
    for i in range(len(vetor)):
        print vetor[i]
	arqCount.write(str(vetor[i])+"\n")   
       
    arqCount.close()
    

def mostra_pixels(pixels, largura, altura):

    for i in range(altura):
        for j in range(largura):
            print pixels[j, i], "  ",
        print "\n"


'''Funcao para aplicar brilho a uma imagem'''        
def aplicar_brilho(originalImage, pixelsOriginalImage, altura, largura):  
    
    imgBrilho = Image.new('RGB', (255,255))
    imgBrilho = originalImage
    pixelsBrilho = pixelsOriginalImage
    
    valor = int(raw_input("Informe o valor pretendido de Brilho: "))
    
    for i in range(altura):
        for j in range(largura):
            r = pixelsOriginalImage[j,i][0] + valor
            g = pixelsOriginalImage[j,i][1] + valor
            b = pixelsOriginalImage[j,i][2] + valor

            pixelsBrilho[j,i] = (r,g,b)
    
    saveImage(imgBrilho, 'images/imgBrilho.png')
    imgBrilho.show()


'''Funcao para criar negativo de uma imagem'''        
def criar_negativo(originalImage, pixelsOriginalImage, altura, largura):  

    imgNegative = Image.new('RGB', (255,255))
    imgNegative = originalImage
    pixelsNegative = pixelsOriginalImage

    for i in range(altura):
        for j in range(largura):
            
	    r = 255 - pixelsOriginalImage[j,i][0]
            g = 255 - pixelsOriginalImage[j,i][1]
            b = 255 - pixelsOriginalImage[j,i][2]
            pixelsNegative[j,i] = (r,g,b)
     
    saveImage(imgNegative, 'images/imgNegativo.png')
    imgNegative.show()


'''Funcao para gerar histograma de uma imagem'''        
def gerar_histograma(pixels, inicioI, inicioJ, altura, largura): 

    dictR={}
    dictG={}
    dictB={}
    for i in range(inicioI,altura):
        for j in range(inicioJ,largura):  
	    if (dictR.has_key(pixels[j,i][0])): 
		dictR[pixels[j,i][0]] = dictR[pixels[j,i][0]] + 1
	    else:
		dictR[pixels[j,i][0]] = 1
	    if (dictG.has_key(pixels[j,i][1])): 
		dictG[pixels[j,i][1]] = dictG[pixels[j,i][1]] + 1
	    else:
		dictG[pixels[j,i][1]] = 1
            if (dictB.has_key(pixels[j,i][2])): 
		dictB[pixels[j,i][2]] = dictB[pixels[j,i][2]] + 1
	    else:
		dictB[pixels[j,i][2]] = 1

    dictR_sorted = sorted(dictR.items(), key=itemgetter(0))
    dictG_sorted = sorted(dictG.items(), key=itemgetter(0))
    dictB_sorted = sorted(dictB.items(), key=itemgetter(0))        

    vector=[]
    vector.append(dictR_sorted)
    vector.append(dictG_sorted)
    vector.append(dictB_sorted)
    
    return vector


'''Funcao para gerar histograma global de uma imagem'''        
def gerar_histograma_global(originalImage, pixelsOriginalImage, altura, largura):  

    print "Gerando Histogramas por Canal..."
    
    vetorCarac = []
    vetorCarac = gerar_histograma(pixelsOriginalImage, 0, 0, altura, largura)

    print "Escrevendo no Arquivo GlobalHistrogram.txt..."
    arquivo = "GlobalHistogram.txt"
    imprimir_arquivo(vetorCarac, arquivo)
    print "Arquivo Gerado Com Sucesso..."
      
   
'''Funcao para gerar o histograma local de uma imagem'''        
def gerar_histograma_local(originalImage, pixelsOriginalImage, altura, largura):  

    print "Gerando Histogramas Local por Canal..."
    vetor = []
    vetorCarac = []
    a=l=i=j=0
    
    while (i<altura):
      a = a+(altura/2)
      while (j<largura):  
         l = l+(largura/2)
         print i,j,a,l
         vetor = gerar_histograma(pixelsOriginalImage, i, j, a, l)
         vetorCarac.append(vetor)
         j=l+1
      i=a+1
      j=0
      l=0
        
    print "Escrevendo no Arquivo LocalHistrogram.txt..."
    arquivo = "LocalHistogram.txt"
    imprimir_arquivo(vetorCarac, arquivo)
    print "Arquivo Gerado Com Sucesso..."


'''Funcao para detectar bordas de uma imagem usando Operador de Roberts'''        
def detectar_bordas_roberts(originalImage, pixelsOriginalImage, altura, largura):  

    Limiar = 10
    qtzeImg = originalImage.convert("P", palette=Image.ADAPTIVE, colors=128).convert("RGB")   
    pixelsQtzImage = qtzeImg.load()
    larguraQtz = qtzeImg.size[0]
    alturaQtz =  qtzeImg.size[1] 
    qtzeImg.show()
    
    imgFiltro = Image.new('RGB', (128,128))
    imgFiltro = qtzeImg
    pixelsFiltro = imgFiltro.load()

    for i in range(1,alturaQtz-1):
        for j in range(1,larguraQtz-1):
           
            r1=r2=0
            r1 = pixelsQtzImage[j+1,i+1][0] - pixelsQtzImage[j,i][0]
            r2 = pixelsQtzImage[j+1,i][0] - pixelsQtzImage[j,i+1][0]
            r =(int)(math.sqrt((pow(r1,2) + pow(r2,2))))
            
            if r>Limiar:
                 pixelsFiltro[j,i] = (255,255,255)
	    else:
		 pixelsFiltro[j,i] = (0,0,0) 
  
    saveImage(imgFiltro, 'images/imgRoberts.png')
    imgFiltro.show()

'''Funcao para detectar bordas de uma imagem usando Operador de Sobel'''        
def detectar_bordas_sobel(originalImage, pixelsOriginalImage, altura, largura):  

    Limiar = 64
    qtzeImg = originalImage.convert("P", palette=Image.ADAPTIVE, colors=128).convert("RGB")   
    pixelsQtzImage = qtzeImg.load()
    larguraQtz = qtzeImg.size[0]
    alturaQtz =  qtzeImg.size[1] 
    qtzeImg.show()
    
    imgFiltro = Image.new('RGB', (128,128))
    imgFiltro = qtzeImg
    pixelsFiltro = imgFiltro.load()

    for i in range(1,alturaQtz-1):
        for j in range(1,larguraQtz-1):
           
          r1=r2=0

          r1=-pixelsQtzImage[j-1,i-1][0]-2*pixelsQtzImage[j,i-1][0]-pixelsQtzImage[j+1,i-1][0]+pixelsQtzImage[j-1,i+1][0]+2*pixelsQtzImage[j,i+1][0]+pixelsQtzImage[j+1,i+1][0]

          r2=-pixelsQtzImage[j-1,i-1][0]+pixelsQtzImage[j+1,i-1][0]-2*pixelsQtzImage[j-1,i][0]+2*pixelsQtzImage[j+1,i][0]-pixelsQtzImage[j-1,i+1][0]+pixelsQtzImage[j+1,i+1][0]

          r =(int)(math.sqrt((pow(r1,2) + pow(r2,2))))
          if r>Limiar:
                 pixelsFiltro[j,i] = (255,255,255)
	  else:
		 pixelsFiltro[j,i] = (0,0,0) 
    
    saveImage(imgFiltro, 'images/imgSobel.png')
    imgFiltro.show()

'''Funcao que calcula a similaridade '''
def calcular_dLog(histA, histB):

    dLog=0 
    for i in range(255):
        if (not histA.has_key(i)):
           histA[i] = 0
        elif ((histA[i]>0) and (histA[i]<=1)):
           histA[i] = 1
        else:
           histA[i] = math.log(histA[i],2)

        if (not histB.has_key(i)):
           histB[i] = 0
        elif ((histB[i]>0) and (histB[i]<=1)):
           histB[i] = 1
        else:
           histB[i] = math.log(histB[i],2)
         
        dif = histA[i]-histB[i]
        dLog = dLog + abs(dif)
        
    return dLog


'''Funcao para extrair propriedades de cor de uma imagem'''        
def extrair_propriedades_bic(originalImage, pixelsOriginalImage, altura, largura):  

    qtzeImg = originalImage.convert("P", palette=Image.ADAPTIVE, colors=64).convert("RGB")   
    pixelsQtzImage = qtzeImg.load()
    larguraQtz = qtzeImg.size[0]
    alturaQtz =  qtzeImg.size[1] 
    qtzeImg.show()

    dictBorda={}
    dictInterior={}
    for i in range(1,alturaQtz-1):
        for j in range(1,larguraQtz-1):
           
            if ((pixelsQtzImage[j,i-1][0] != pixelsQtzImage[j,i][0]) or (pixelsQtzImage[j-1,i][0] != pixelsQtzImage[j,i][0]) or (pixelsQtzImage[j+1,i][0] != pixelsQtzImage[j,i][0]) or (pixelsQtzImage[j,i+1][0] != pixelsQtzImage[j,i][0])):  
               
	       if (dictBorda.has_key(pixelsQtzImage[j,i][0])): 
		  dictBorda[pixelsQtzImage[j,i][0]] = dictBorda[pixelsQtzImage[j,i][0]] + 1
	       else:
		  dictBorda[pixelsQtzImage[j,i][0]] = 1

	    else:
               
	       if (dictInterior.has_key(pixelsQtzImage[j,i][0])): 
		  dictInterior[pixelsQtzImage[j,i][0]] = dictInterior[pixelsQtzImage[j,i][0]] + 1
	       else:
		  dictInterior[pixelsQtzImage[j,i][0]] = 1
             
    dictBorda_sorted = sorted(dictBorda.items(), key=itemgetter(0))
    dictInterior_sorted = sorted(dictInterior.items(), key=itemgetter(0))
    
    #dLog = calcular_dLog(dictBorda, dictInterior)    
    #print dLog

    vetorCarac=[]
    vetorCarac.append(dictBorda_sorted)
    vetorCarac.append(dictInterior_sorted)
    
    print "Escrevendo no Arquivo BICHistrogram.txt..."

    arquivo = "BICHistogram.txt"
    imprimir_arquivo(vetorCarac, arquivo)
    print "Arquivo Gerado Com Sucesso..."
              

#-------Programa Principal------    
def menu():
    
  
    os.system("clear");
    print "==================================="
    print "======= Image Editor ========"
    print "==================================="
    opcao = raw_input("Escolha opcao desejada\n\n[1] - Aplicar Brilho\n[2] - Criar Negativo\n[3] - Gerar Histograma Global\n[4] - Gerar Histograma Local\n[5] - Detectar Bordas - Roberts \n[6]- Extrair propriedades de cor usando BIC\n[7] - Sair")
 
    try:
        opcao = int(opcao)
        if opcao<1 or opcao>7:
            os.system("clear");
            print "OPCAO INVALIDA: Verifique o valor digitado"
            time.sleep(2)
            menu()
    except:
        os.system("clear");
        print "OPCAO INVALIDA: Verifique o valor digitado"
        time.sleep(2)
        menu()
 
    if opcao != 7:
	file_path = str(raw_input("\nDigite o caminho da Imagem: "))
        originalImage = openImage(file_path)
        pixelsOriginalImage = originalImage.load()
        largura = originalImage.size[0]
        altura =  originalImage.size[1]
        originalImage.show()

    if opcao == 1:
        aplicar_brilho(originalImage, pixelsOriginalImage, altura, largura)
       
    elif opcao == 2:
        criar_negativo(originalImage, pixelsOriginalImage, altura, largura)
       
    elif opcao == 3:
        gerar_histograma_global(originalImage, pixelsOriginalImage, altura, largura)
       
    elif opcao == 4:
        gerar_histograma_local(originalImage, pixelsOriginalImage, altura, largura)
       
    elif opcao == 5:
        detectar_bordas_roberts(originalImage, pixelsOriginalImage, altura, largura)
       
    #elif opcao == 6:
    #    detectar_bordas_sobel(originalImage, pixelsOriginalImage, altura, largura)
       
    elif opcao == 6:
        extrair_propriedades_bic(originalImage, pixelsOriginalImage, altura, largura)
       
    elif opcao == 7:
        sys.exit()

    #time.sleep(2)
    #menu()


if __name__=='__main__':
    menu()
