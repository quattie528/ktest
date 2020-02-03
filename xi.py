#!/usr/bin/python

### MODULES ###
import os
from PIL import Image
import PIL.ImageOps

### KONSTANT ###
notice = True
binary = True

"""
http://hp.vector.co.jp/authors/VA032610/JPEGFormat/StructureOfJPEG.htm
SOI スタートマーカ (Start of Image) 　0xFFD8
EOI エンドマーカ 　(End of Image) 　　0xFFD9

DQT 量子化テーブル定義　　(Define Quantization Table) 0xFFDB
DHT ハフマンテーブル定義　(Define Huffman Table)　　　0xFFD4
-------------------------------------------------
'rgb' 	SGI ImgLib Files
'gif' 	GIF 87a and 89a Files
'pbm' 	Portable Bitmap Files
'pgm' 	Portable Graymap Files
'ppm' 	Portable Pixmap Files
'tiff' 	TIFF Files
'rast' 	Sun Raster Files
'xbm' 	X Bitmap Files
'jpeg' 	JPEG data in JFIF or Exif formats
'bmp' 	BMP files
'png' 	Portable Network Graphics
"""

def imageformat(img):
	return imghdr.what(img)

#

#########################
### GEGENTEILIGEFARBE ###
#########################
def gegenteiligeFarbe(s):
	"""
	反転色 : 1EB7BA -> E14845
	補色   : 1EB7BA -> BA211E
	"""
	debug = True
	debug = False
	assert s[0] == '#'
	assert len(s) == 7
	s2 = [ s[1:3], s[3:5], s[5:7] ]
	#
#	for i in range(3): print( s[i], int(s[i],16) )
	r = [ 255 - int(s2[i],16) for i in range(3) ]
	q = [ '%02x' % r[i] for i in range(3) ]
	if debug == True:
		print( '*'*40 )
		print( 'DIV :',s,'->',s2 )
		print( 'x16 :',s,'->',r )
		print( 's16 :',s,'->',q )
	res = ''.join(q)
	res = '#' + res
	res = res.upper()
	return res

#

####################
### IMAGE NEGATE ###
####################
def negate(image):
	#2017-01-06
	#http://stackoverflow.com/questions/2498875/how-to-invert-colors-of-image-with-pil-python-imaging
	inverted_image = ''
	image = Image.open(image)
	if image.mode == 'RGBA':
		r,g,b,a = image.split()
		rgb_image = Image.merge('RGB', (r,g,b))
		inverted_image = PIL.ImageOps.invert(rgb_image)
		r2,g2,b2 = inverted_image.split()
#		final_transparent_image = Image.merge('RGBA', (r2,g2,b2,a))
#		final_transparent_image.save('new_file.png')
	else:
		inverted_image = PIL.ImageOps.invert(image)
#		inverted_image.save('new_name.png')
	return inverted_image

def tmpimgs(des,aux,xaxis,yaxis):
	zupfad = "/backup/"
#	clearfolder(zupfad)
	for x in os.listdir(des):
		flg = False
		for ext in ['png','jpg','JPG']:
			ext = '.' + ext
			if ext in x:
				flg = True
				break
		if flg == False: continue
		#
		img = Image.open(des+x)
		img = img.resize((xaxis,yaxis))
		img.save(aux+x)

def tmpimgs4sony(pfad):
	tmpimgs(pfad,1200,1600) # Sony/DPT-S1

def bilds_schwinden(pfad,pctg=33):
	datei = os.listdir(pfad)[0]
	img = Image.open(pfad+datei)
	x = img.size[0] // 100 * pctg
	y = img.size[1] // 100 * pctg
	tmpimgs(pfad,x,y)
	#
	print( 'LA FIN' )

#

######################
### BILDEN zu BILD ###
######################
def bilden2bild(bilden,ausgabe='a.png',xlen=4,ylen=3):
	print( len(bilden) )
	print( xlen * ylen )
	assert len(bilden) <= xlen * ylen

	res = Image.open(bilden[0])
	xori,yori = res.size
	res = Image.new('1',(xori*xlen,yori*ylen))

	xnow = 0
	ynow = 0
	for i,bild in enumerate(bilden):
		bild = Image.open(bild)
		res.paste(bild,(xnow,ynow))
		xnow += xori
		if xnow / xori == xlen :
			ynow += yori
			xnow = 0
	print( ausgabe )
	res.save(ausgabe)

def mbilden2bild(des,ex): bilden2bild(des,ex,4,3)
def qbilden2bild(des,ex): bilden2bild(des,ex,2,2)

#

#######################
### IMAGE zu STRING ###
#######################
def img2str(datei,sprache='eng'):
	import pytesseract as ocr
	from PIL import Image

	### same drive rule, on windows ##
	#https://github.com/madmaze/pytesseract/issues/50
	hier = os.getcwd()
	os.chdir('C:')

	cmd = 'C:/Program Files (x86)/Tesseract-OCR/tesseract.exe'
	#cmd = 'C:/Program Files (x86)/Tesseract-OCR/tesseract'
	cmd = 'C:/usr/Tesseract-OCR/tesseract.exe'
	cmd = 'C:/usr/Tesseract-OCR/tesseract'
	ocr.pytesseract.tesseract_cmd = cmd

	# Simple image to string
	img = Image.open(datei)
	#x = ocr.image_to_string(img,lang='fra')
	x = ocr.image_to_string(img,lang=sprache)
	return x

def imgpfad2str(pfad,ausgabe):
	ds = os.listdir(pfad)
	gh = open(ausgabe, 'w',encoding='utf-8')
	for png in ds:
		print( png ) #d
		x = img2str(pfad+png)
		gh.write("<IMG>%s\n" % png)
		gh.write(x)
		gh.write("\n\n\n")
		gh.flush()
	gh.close()

#

##### DIREKT ###############
if __name__=='__main__':
	pass
