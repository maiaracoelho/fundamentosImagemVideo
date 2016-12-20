import Image
import random

def mostra_pixels(img, larg, alt):
    pixels = img.load()
    for i in range (alt):
        for j in range (larg):
            print pixels[j, i], "  ",
        print "\n"

def gera_img_2_por_4_cinzas():
    l = 4
    a = 2
    img = Image.new('RGB', (l,a))
    p = img.load()
    mostra_pixels(img, 4, 2)
    p[0,0] = (0,0,0)
    p[1,0] = (30,30,30)
    p[2,0] = (60,60,60)
    p[3,0] = (90,90,90)
    p[0,1] = (120,120,120)
    p[1,1] = (150,150,150)
    p[2,1] = (180,180,180)
    p[3,1] = (210,210,210)
    return img

def gera_img_2_por_4():
    l = 4
    a = 2
    img2 = Image.new('RGB', (l,a))
    p = img2.load()
    mostra_pixels(img2, 4, 2)
    p[0,0] = (240,30,5)
    p[1,0] = (240,30,5)
    p[2,0] = (240,30,5)
    p[3,0] = (240,30,5)
    p[0,1] = (10,50,190)
    p[1,1] = (10,50,190)
    p[2,1] = (10,50,190)
    p[3,1] = (10,50,190)
    return img2

def gera_img_100_por_200():
    l = 200
    a = 100
    img = Image.new('RGB', (l,a))
    p = img.load()
    for i in range (a):
        for j in range (l):
            if i < 50:
                r = 255
                g = 255
                b = 255
            else:
                r = 125
                g = 200
                b = 178
            p[j, i] = (r, g, b)
    return img


def gera_img2():
    largura = 500
    altura = 200
    img = Image.new('RGB', (largura, altura))
    pixels = img.load()
    fator = altura / 255.0
    for i in range (altura):
        r = int(i/fator)
        g = int(i/fator)
        b = int(i/fator)
        for j in range (largura):
            pixels[j, i] = (r, g, b)
    return img

def gera_img_aleatoria():
    largura = 1024
    altura = 768
    img = Image.new('RGB', (largura, altura))
    pixels = img.load()
    for i in range (largura):
        for j in range (altura):
            r = int(random.random() * 256)
            g = int(random.random() * 256)
            b = int(random.random() * 256)
            pixels[i, j] = (r, g, b)
    return img

img = gera_img_100_por_200()
#mostra_pixels(img, img.size[0], img.size[1])
img.save("c:\hame\ensino\CG_PDI\imagens\img_xyz.jpg")
img2 = gera_img_2_por_4()
mostra_pixels(img2, img2.size[0], img2.size[1])
img2.format = "png"
img2.save("c:\hame\ensino\CG_PDI\imagens\img_2_por_4_br.png")
print "C'est fini"
