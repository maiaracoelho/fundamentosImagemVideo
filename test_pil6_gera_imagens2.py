import Image

img = Image.new( 'RGB', (255,255)) # create a new black image
pixels = img.load() # create the pixel map

for i in range(img.size[0]):    # for every pixel:
    for j in range(img.size[1]):
        pixels[i,j] = (i, j, 100) # set the colour accordingly

print "Salvando 1a imagem"
img.save("c:\hame\ensino\CG_PDI\imagens\eca7.jpg")


for i in range(img.size[0]):    # for every pixel:
    for j in range(img.size[1]):
        pixels[j,i] = (i, j, 100) # set the colour accordingly

print "Salvando 2a imagem"
img.save("c:\hame\ensino\CG_PDI\imagens\eca8.jpg")
print "C'est fini"