from PIL import Image
import random

# img = Image.open("c:\hame\ensino\CG_PDI\imagens\LennaSoderberg.jpg")
# pixels = img.load()

# img2 = Image.open("c:\hame\ensino\CG_PDI\imagens\pba74707.jpg")
# pixels2 = img2.load()

img3 = Image.open("images/6.png")
pixels3 = img3.load()

# print "tamanho da imagem LennaSoderberg.jpg = ", img.size[0], "X", img.size[1]
# print "tamanho da imagem aviao BA 747 = ", img2.size[0], "X", img2.size[1]

#largura = 1024
#altura = 768
#img = Image.new('RGB', (largura, altura))

# A partir daqui vem os procedimentos/funcos como alterar_brilho, negativo,
# histograma, recorte, etc.

def mostra_pixels(pixels, largura, altura):

    for i in range(altura):
        for j in range(largura):
            print pixels[j, i], "  ",
        print "\n"

def aplicar_brilho(pixels, pixels_brilho, largura, altura, valor):

	for i in range(altura):
		for j in range(largura):
			r = pixels[j,i][0] + valor
			g = pixels[j,i][1] + valor
			b = pixels[j,i][2] + valor

			pixels_brilho[j,i] = (r,g,b)
	
	return pixels_brilho



print "mostrando pixels de uma imagem:"
mostra_pixels(pixels3, img3.size[0], img3.size[1])
print "\n"
print img3.mode, "  ", img3.format
print "\n"
print img3.show()
print "tamanho da imagem img_2-4 = ", img3.size[0], "X", img3.size[1]


imgBrilho = Image.new('RGB', (255,255))

imgBrilho = img3
pixelsBrilho = img3.load()
pixelsBrilho = aplicar_brilho(pixels3, pixelsBrilho, img3.size[0], img3.size[1], -255)
mostra_pixels(pixelsBrilho, imgBrilho.size[0], imgBrilho.size[1])
img3.show()
imgBrilho.show()
