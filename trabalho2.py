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
import numpy as np
import cv2
 
WINDOWS = 10

def openVideo(path):
    return cv2.VideoCapture(path)

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
def extrair_propriedades_bic(frameAnterior, frameAtual):  

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
    
    vetorCarac=[]
    vetorCarac.append(dictBorda_sorted)
    vetorCarac.append(dictInterior_sorted)
    
    print "Escrevendo no Arquivo BICHistrogram.txt..."

    arquivo = "BICHistogram.txt"
    imprimir_arquivo(vetorCarac, arquivo)
    print "Arquivo Gerado Com Sucesso..."
              
def detect_bic(video):
    
    count = 0
    framesCount = 0
    frame_rate = int(video.get(cv2.cv.CV_CAP_PROP_FPS)) 
    nFrames = int(video.get(cv2.cv.CV_CAP_PROP_FRAME_COUNT)) 
    contadorDeFrames = True
    
    video.set(1, count)
    contadorDeFrames, frame = video.read()
    cv2.imshow("Video", frame)
    cv2.moveWindow('Video', 100, 178)
    print"Frame: %d" %count
    count += WINDOWS 
    framesCount += 1 
    frameAnterior = frame
        
    while (count < nFrames):
        
        video.set(1, count)
        contadorDeFrames, frame = video.read()
        cv2.imshow("Video", frame)
        cv2.moveWindow('Video', 100, 178)
        print"Frame: %d" %count
        
        #frameAnterior = quantize_image()
        #frame = quantize_image()
        #vetorFrameAnterior = extrair_propriedades_bic(frameAnterior)
        #vetorFrameAtual = extrair_propriedades_bic(frameframe)
        #dLog(vetorFrameAnterior, vetorFrameAtual)
                
        k = cv2.waitKey(33)
        if k==27:    # Esc key to stop
            break
        
        count += WINDOWS 
        framesCount += 1 
                
    print ("Numero de Frames Avaliados: %d" %framesCount)
    print ("Numero de frames: %d" %nFrames)
    video.release()
    cv2.destroyAllWindows()
    
    
#-------Programa Principal------    1
def menu():
    
  
    os.system("clear");
    print "==================================="
    print "======= Video Shot Detector ========"
    print "==================================="
    opcao = raw_input("Escolha opcao desejada\n\n[1] - BIC\n[2] - Criar Negativo\n[3] - Gerar Histograma Global\n[4] - Gerar Histograma Local\n[5] - Detectar Bordas - Roberts \n[6]- Extrair propriedades de cor usando BIC\n[7] - Sair")
 
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
	#file_path = str(raw_input("\nDigite o caminho do Video: "))
        video = openVideo("videos/2.mp4")

    if opcao == 1:
        detect_bic(video)
       
    elif opcao == 2:
        pass
       
    elif opcao == 3:
        pass
       
    elif opcao == 4:
        pass
       
    elif opcao == 5:
        pass
       
    #elif opcao == 6:
    #    detectar_bordas_sobel(originalImage, pixelsOriginalImage, altura, largura)
       
    elif opcao == 6:
        pass
       
    elif opcao == 7:
        sys.exit()


if __name__=='__main__':
    menu()
