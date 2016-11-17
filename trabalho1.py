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

def openImage(path):
    return Image.open(path)

def mostra_pixels(pixels, largura, altura):

    for i in range(altura):
        for j in range(largura):
            print pixels[j, i], "  ",
        print "\n"


'''Funcao para aplicar brilho a uma imagem'''        
def aplicar_brilho(file_path):  
    
    originalImage = openImage(file_path)
    pixelsOriginalImage = originalImage.load()
    largura = originalImage.size[0]
    altura =  originalImage.size[1]
    
    imgBrilho = Image.new('RGB', (255,255))
    imgBrilho = originalImage
    pixelsBrilho = pixelsOriginalImage
    
    valor = raw_input("Informe o valor pretendido de Brilho: ")
    
    for i in range(altura):
        for j in range(largura):
            r = pixelsOriginalImage[j,i][0] + valor
            g = pixelsOriginalImage[j,i][1] + valor
            b = pixelsOriginalImage[j,i][2] + valor

            pixels_brilho[j,i] = (r,g,b)
    
    originalImage.show()
    imgBrilho.show()
           
#-------Programa Principal------    
def menu():
    
    os.system("clear");
    print "==================================="
    print "======= Image Editor ========"
    print "==================================="
    opcao = raw_input("Escolha opcao desejada\n\n[1] - Aplicar Brilho\n[2] - Aplicar Tons de Cinza\n[3] - Criar Negativo\n[4] - Coletar Instabilidade\n[5] - Coletar Popularidade\n[6]- Gerar Graficos Gerais\n[7] - Sair")
 
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
 
    file_path = str(raw_input("\nDigite o caminho da Imagem: "))
    
    if opcao == 1:
        aplicar_brilho(file_path)
        
    elif opcao == 2:
        aplicarTonsCinza(file_path)
 
    elif opcao == 3:
        criarNegativo(file_path)
 
    elif opcao == 4:
        aplicarBrilho(file_path)
 
    elif opcao == 5:
        aplicarBrilho(file_path)
    
    elif opcao == 6:
        aplicarBrilho(file_path)
 
    elif opcao == 7:
        sys.exit()

if __name__=='__main__':
    menu()