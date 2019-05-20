#!/usr/bin/python

### MODULES ###
#import datetime
#import os
#import pprint
#
#import attrdict
#
from datsun import *
import xz
#import kbench
#
#1:battery,2:pip,3:mygen,4:myopus

### VARIABLES ###
debug = True
debug = False

#

###########
### ERB ###
###########
def erb(kennwort,wert=None):
	dic = 'ex/cache/xb_erb.dic'
	try:
		res = xz.bin2obj(dic)
	except FileNotFoundError:
		res = {}
	if wert == None:
		res = res.get(kennwort,None)
		return res
	else:
		res[kennwort] = wert
		xz.obj2bin(res,dic)

def dateien4erb(dateien,letzt):
	res = []
	geh = False
	for datei in dateien:
		if datei == letzt:
			geh = True
			continue
		if geh == False:
			continue
		res.append(datei)
	return res

###########
###  ###
###########
def erstezeile(txt,er=1):
#	fh = open(txt)
	fh = open(txt, 'r',encoding='utf-8')
	zahl = 0
	while 1:
		x = fh.readline()
		zahl += 1
		if zahl == er: break	
	fh.close()
	print( repr(x) )
	return x

def letztzeile(txt):
#	fh = open(txt)
	fh = open(txt, 'r',encoding='utf-8')
	zahl = 0
	while 1:
		x = fh.readline()
		if not x: break
		zahl += 1
		x = x.strip()
		y = x
	fh.close()
	#
	x = 'Das ist die Antwort'
	x = rahmen(x)
	zahl = commify(zahl)
	print( x )
	print( '* Zusammen %s Linie' % zahl )
	print( repr(y) )
	print( '' )
	return y

#

##### DIREKT ###############
if __name__=='__main__':
	letztzeile(txt)
	kbench.jetzt()
