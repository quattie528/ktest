#!/usr/bin/python

#A : Adobe

### MODULES ###
import re
import sys
import pdfkit
import xz

opt = {
    'page-size': 'A4',
    'margin-top': '0.75in',
    'margin-right': '0.75in',
    'margin-bottom': '0.75in',
    'margin-left': '0.75in',
    'encoding': "UTF-8",
    'no-outline': None
}
### path is needed to set ###
#cfg = pdfkit.configuration(wkhtmltopdf='/opt/bin/wkhtmltopdf'))
#cfg = pdfkit.configuration(wkhtmltopdf='C:/Program Files (x86)/wkhtmltopdf/bin'))

### STRING to PDF ###
def str2pdf(x,ex):
	pdfkit.from_string(x,ex)

#

##################
### TXT to PDF ###
##################
def txt2a4pdf(txt,ex):
	opt = { 'page-size': 'A4' }
	pdfkit.from_file(txt,ex,opt)

def txt2a5pdf(txt,ex):
	opt = { 'page-size': 'A5' }
	pdfkit.from_file(txt,ex,opt)

def txt2pdf(txt,ex):
	txt2a4pdf(txt,ex)
#

### TXTs to PDF ###
def txts2pdf(txts,ex):
	pdfkit.from_file(x,ex)

#

### URL to PDF ###
def url2pdf(x,ex):
	pdfkit.from_url(x,ex)

#

### MERGE PDF ###
def mergepdf(ex,*pdfs):
	import PyPDF2
	merger = PyPDF2.PdfFileMerger()
	if isinstance(pdfs[0], list):
		pdfs = pdfs[0]
	for x in pdfs:
		fh = open(x, 'rb')
		merger.append(fh)
		fh.close
	merger.write( open(ex, 'wb') )

#

#####################
### IMAGEs to PDF ###
#####################
def imgs2pdf(weg,ex='a.pdf',fmt='png'): # 2016-05-21
	from fpdf import FPDF
	import os
	#
	pdf = FPDF()
	x,y,w,h = 0,0,210,294 # 0,0
	"""
	x,y = position coordinate
	w,h = weight and height, it seems cm is the unit
	"""
	#
	fmt2 = fmt + '$'
	if not re.search('\.',fmt):
		fmt = '.' + fmt
	#
	feilen = os.listdir(weg)
	for bild in feilen:
		if not re.search(fmt2,bild): continue
		pdf.add_page()
		pdf.image(weg+bild,x,y,w,h)
#		pdf.image(bild,x,y,w,h)
	pdf.output(ex, "F")
	print( 'Ausgabe als %s' % ex )

#

##### DIREKT ###############
if __name__=='__main__':
	pass
