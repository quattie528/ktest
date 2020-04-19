#!/usr/bin/python

### MODULES ###
import datetime
#import os
#import pprint
#
#import attrdict
#
from datsun import *
import xf
import xz
import xx
#import kbench
#
#1:battery,2:pip,3:mygen,4:myopus

### VARIABLES ###
DEBUG = True
DEBUG = False

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

### 2020-03-08 ###-------------------------------------------------
"""
B für Bekommen, Binary (Binärdatei), Bigdata
"""

#

###########################################
### EINGABE und AUSGABE, TUN oder NICHT ###
###########################################
def ein2aus(des,aux,msg=''):
	if msg == '': msg = aux
	#
	res = True
	if os.path.exists(aux):
		if DEBUG == True:
			print( '[UR  ]', xf.mtime(des), '||', des ) #d
			print( '[NACH]', xf.mtime(aux), '||', aux ) #d
		if xf.mtime(des) < xf.mtime(aux):
			res = False
	#
	if DEBUG == True and res == False:
		print( '[undo]',msg ) #d
	elif DEBUG == True and res == True:
		print( '[do]',msg ) #d
	return res


def ord2aus(ordner,aux,msg=''):
	dateien = os.listdir(ordner)
	res = ''
	zt = datetime.datetime(1,1,1,0,0,0)
	for datei in dateien:
		tmp = xf.mtime(ordner+datei)
		if zt < tmp:
			zt = tmp
			res = datei
	des = ordner + res
	res = ein2aus(des,aux,msg)
	return res

#

############################
### STAMM(XLS) zu OBJEKT ###
############################
def stamm2obj(xls,bin,blatt=0,**kwargs):
#def xls2obj(bin,xls,blatt=0): # 2019-11-04
	"""
	STAMM kommst aus "STAMMDATEN"
	https://de.wikipedia.org/wiki/Stammdaten
	"""

	### VORBEREITUNG ###
	erst = kwargs.get('erst',False)
	ldic = kwargs.get('ldic',False)
	ddic = kwargs.get('ddic',False)
	ddickey = kwargs.get('ddickey','')
	if ddic == True:
		ldic = True
#	print( ldic ) #d
#	print( ddic ) #d
#	print( ddickey ) #d

	### ERST ###
	if erst == True:
		os.remove(bin)

	### HAUPT 1 - WIERDERVERWERTEN ###
	if not ein2aus(xls,bin,'LAUFEN STAMM2OBJ()'):
		if DEBUG == True:
			print( '#Wierderverwerten' ) #d
		if os.path.exists(bin):
			obj = xz.bin2obj(bin)
			return obj

	### HAUPT 2 - LADEN ###
	if DEBUG == True:
		print( '#Laden' ) #d
	obj = xx.xls2tbl(xls,blatt)
	if ldic == True:
		obj = xz.tbl2ldic(obj)
		if ddic == True:
			obj = xz.ldic2ddic(obj,ddickey)
	xz.obj2bin(obj,bin)

	### AUSGABE ###
	return obj

def stamm2ldic(xls,bin,blatt=0,**kwargs):
	obj = stamm2obj(xls,bin,blatt,ldic=True)
	return obj
def stamm2ddic(xls,bin,blatt=0,**kwargs):
	kwargs['ddic'] = True
	obj = stamm2obj(xls,bin,blatt,ddic=True)
	return obj

#

################################################
### STAMM zu 3 OBJEKT (TSV,LIST-DICT,PANDAS) ###
################################################
def stamm3obj(xls,tsv,blatt=0):

	assert tsv[-4:] == '.tsv'

	import pandas as pd

	if ein2aus(xls,tsv):
		obj = stamm2obj(xls,tsv,blatt)
		xz.tbl2txt(obj,tsv)
		#
		obj = xz.tbl2ldic(obj)
		ausgabe = tsv.replace('.tsv','.ldic')
		xz.obj2bin(obj,ausgabe)
		#
		obj = pd.DataFrame(obj)
		ausgabe = tsv.replace('.tsv','.pds')
		obj.to_pickle(ausgabe)
	else:
		ausgabe = tsv.replace('.tsv','.pds')
		obj = pd.read_pickle(ausgabe)
	return obj

#

##### DIREKT ###############
if __name__=='__main__':
	ord = 'D:/var/lib/bilan3/morn/2020/jpn/'
	aux = 'D:/onedrive/zwischen/derivat/bilan2/TSEq.tsv'
	x = ord2aus(ord,aux)
	print( x )
#	stamm3obj()
	kbench.jetzt()
