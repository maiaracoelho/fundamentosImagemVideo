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
from math import floor
#from multiprocessing import Process

 
WINDOWS = 10

def openVideo(path):
    return cv2.VideoCapture(path)

def quantize_image(frame, n):
    
    qtze_image = frame
    height = qtze_image.shape[0]
    width = qtze_image.shape[1]
    
    for i in range(width):
        for j in range(height):
            r = (qtze_image[j, i][0]/n) * n
            g = (qtze_image[j, i][1]/n) * n
            b = (qtze_image[j, i][2]/n) * n
    
            qtze_image[j,i] = (r,g,b)
    return qtze_image


def quantize_image2(frame, n):
    
    #im = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
    pil_im = Image.fromarray(frame)
    qtzeImg = pil_im.convert("P", palette=Image.ADAPTIVE, colors=n).convert("RGB")   
    openCvQtzedImage = np.array(qtzeImg) 
    #open_cv_image = open_cv_image[:, :, ::-1].copy() 
    return openCvQtzedImage


'''Funcao que calcula a similaridade '''
def calcular_dLog(histA, histB):

    dLogAB=0 
    f_histA = f_histB = 0
    for i in range(256):
        if histA[i] == 0:
           f_histA = 0
        elif ((histA[i]>0) and (histA[i]<=1)):
           f_histA = 1
        else:
           f_histA = math.log(histA[i],2)

        if histB[i] == 0:
           f_histB = 0
        elif ((histB[i]>0) and (histB[i]<=1)):
           f_histB = 1
        else:
           f_histB = math.log(histB[i],2)
         
        dif = f_histA - f_histB
        dLogAB = dLogAB + abs(dif)
        
    return dLogAB


'''Funcao para extrair propriedades de cor de uma imagem'''        
def extrair_propriedades_bic(frameQtze):  

    height = frameQtze.shape[0]-1
    width = frameQtze.shape[1]-1


    bordaList = np.zeros((256),dtype=np.int)
    interiorList = np.zeros((256),dtype=np.int)

    for i in xrange(1,width):
        for j in xrange(1,height):
           
            if ((frameQtze[j,i-1][0] != frameQtze[j,i][0]) or (frameQtze[j-1,i][0] != frameQtze[j,i][0]) or (frameQtze[j+1,i][0] != frameQtze[j,i][0]) or (frameQtze[j,i+1][0] != frameQtze[j,i][0])):  
               #print frameQtze[j,i][0], bordaList[frameQtze[j,i][0]] 
	       bordaList[frameQtze[j,i][0]] = bordaList[frameQtze[j,i][0]] + 1
	    else:               
	       #print frameQtze[j,i][0], interiorList[frameQtze[j,i][0]]
	       interiorList[frameQtze[j,i][0]] = interiorList[frameQtze[j,i][0]] + 1
	       
    vetorCarac = []
    vetorCarac = bordaList + interiorList
    
    return vetorCarac
              
def detect_bic(video):
    
    count = 0
    framesCount = 0
    frame_rate = int(video.get(cv2.cv.CV_CAP_PROP_FPS)) 
    nFrames = int(video.get(cv2.cv.CV_CAP_PROP_FRAME_COUNT)) 
    contadorDeFrames = True
    
    video.set(1, count)
    contadorDeFrames, frameAtual = video.read()
    
    print "Quantizando Primeiro Frame..."
    frameAtual_qtze = quantize_image2(frameAtual, 64)
    frameAnterior_qtze = frameAtual_qtze
    
    cv2.imshow("Video", frameAtual_qtze)
    cv2.moveWindow('Video', 100, 178)
    print"Frame: %d" %count
    
    print "Extraindo propriedades de cores do Primeiro Frame..."
    vetorFrameAtual = extrair_propriedades_bic(frameAtual_qtze)
    
    print "Primeiro Frame sera frame anterior"
    frameAnterior_qtze = frameAtual_qtze
    vetorFrameAnterior = vetorFrameAtual
    countShot = 0

    count += WINDOWS 
    framesCount += 1 
    
    while (count < nFrames):
        
        video.set(1, count)
        contadorDeFrames, frameAtual = video.read()
                
	print "Quantizando Frame Atual..."
        frameAtual_qtze = quantize_image2(frameAtual, 64)
        
	cv2.imshow("Video", frameAtual_qtze)
        cv2.moveWindow('Video', 100, 178)
        print"Frame: %d" %count

        print "Extraindo propriedades de cores do Frame Atual..."
        vetorFrameAtual = extrair_propriedades_bic(frameAtual_qtze)
        print vetorFrameAtual

        dLog = calcular_dLog(vetorFrameAnterior, vetorFrameAtual)
	print dLog

	'''	if dLog > LIMIAR:
		countShot += 1
	'''
        print "Frame Atual sera o novo FrameAnterior"
        frameAnterior_qtze = frameAtual_qtze
        vetorFrameAnterior = vetorFrameAtual

        k = cv2.waitKey(33)
        if k==27:    # Esc key to stop
            break
        
        count += WINDOWS 
        framesCount += 1 
                
    print ("Numero de Frames Avaliados: %d" %framesCount)
    print ("Numero de frames: %d" %nFrames)
    video.release()
    cv2.destroyAllWindows()
    
    
#-------Programa Principal------    
if __name__=='__main__':
    
    os.system("clear");
    print "==================================="
    print "======= Video Shot Detector ========"
    print "==================================="
   
    #file_path = str(raw_input("\nDigite o caminho do Video: "))
    video = openVideo("videos/7.mp4")
    detect_bic(video)
