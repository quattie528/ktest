#!/usr/bin/python

### MODULES ###
import re
import os
#
import xt
import xz

def fxs():
	fx1 = lambda x,y: x/y # per capita
	fx2 = lambda x,y: x*y # multiple
	fx3 = lambda x,y: x*y/100 # x:val,y:pctg

	delta = lambda x1,x2: x2-x1

#

#####################
### TABLE for LOG ###
#####################
def tbl4log(txt,dic,gettable=False):
	assert( isinstance(dic, dict) )
	tbl = xz.txt2tbl(txt)
	header = xz.getheader(txt)
	#
	if not 'tag' in dic:
		dic['tag'] = xt.heute()
	#
	assert sorted(header) == sorted(list(dic.keys()))
	if tbl[-1][0] == str(dic['tag']):
		tbl.pop()
	res = [ dic[k] for k in header ]
	tbl.append(res)
	#
	xz.tbl2txt(tbl,txt)
	if gettable == True:
		return tbl
	else:
		tbl = xz.txt2ldic(txt)
		tbl = xz.bless(tbl)
		return tbl,header

#

########################
### LDIC zu ERFÜLLEN ###
########################
def dic2erfullen(dic,kopfer):
	for x in kopfer:
		if x in dic: continue
		dic[x] = ''
	return dic

########################
### LDIC zu ERFÜLLEN ###
########################
def ldic2erfullen(ldic,kopfer):
	res = []
	for dic in ldic:
		for k in kopfer:
			if not k in dic:
				dic[k] = ''
#		res.append(tmp)
#	return res

#

######################
### TEXT zu STRING ###
######################
def txt2str(txt):
	"""
	[xz.py]
	with open(txt, 'r',encoding='utf-8') as f: x = f.read()
	return x.replace("\r",'')
	"""
	###
	try:
		fh = open(txt, 'r',encoding='sjis')
		res = fh.read()
		fh.close()
		return res
	except UnicodeDecodeError:
		pass

	fh = open(txt, 'r',encoding='utf-8',errors='replace')
	res = fh.read()
	fh.close()
	return res

#

######################################
### CONVERSION BETWEEN TSV and KML ###
######################################

### TSV to KML ###
def tsv2kml(des,aux):
	kopfer = xz.getheader(des)
	res1 = xz.txt2ldic(des)
	res1 = tsv7kml(res1,'tsv2kml')
	xz.ldic2kml(res1,aux,kopfer)
#d	ldic2kml(res1,'w.memo',kopfer) #debug
#	time.sleep(1)
	res2 = xz.kml2ldic(aux)
	if res1 == res2:
		pass
	else:
		assert( 1 == 1 ) # bluff
		assert( 1 == 2 )

### KML to TSV ###
def kml2tsv(des,aux):
	kopfer = xz.getkmlheader(des)
	res1 = xz.kml2ldic(des)
	res1 = tsv7kml(res1,'kml2tsv')
	xz.ldic2txt(res1,aux,kopfer)
	res2 = xz.txt2ldic(aux)
	if res1 == res2:
		pass
	else:
		assert( 1 == 1 ) # bluff
		for i in range( len(res1) ):
			d1 = res1[i]
			d2 = res1[i]
			print( i )
			if d1 == d2: continue
			print( i,i,i,i )
			print( d1 )
			print( d2 )
			break
		assert( 1 == 2 )

### Choose KML or TSV ###
def tsv8kml(des,aux=''):
	TMP4KMLTSV = 'abc.def.123.txt'
	if aux == '':
		aux = TMP4KMLTSV

	### MODE ###
	with open(des, 'r',encoding='utf-8') as f:
		x = f.readline()
	mode = 'tsv2kml'

	### HAUPT ###
	if re.match(".+\t",x):
		mode = 'tsv2kml'
		tsv2kml(des,aux)
	else:
		mode = 'kml2tsv'
		kml2tsv(des,aux)

	### AUSGABE ###
	if aux == TMP4KMLTSV:
		aux = xz.txt2str(aux)
		os.remove(TMP4KMLTSV)
		return aux
	else:
		if mode == 'tsv2kml':
			return 'kml'
		elif mode == 'kml2tsv':
			return 'tsv'

### Adjust "\n" for KML and TSV ###
def tsv7kml(ldic,mode):
	for dic in ldic:
		for k,v in dic.items():
			if mode == 'tsv2kml':
				v = v.replace("////","\n")
			if mode == 'kml2tsv':
				v = v.replace("\n","////")
			dic[k] = v
	return ldic

#

#######################
### DICT KEY CHANGE ###
#######################
def dickey(dic,keys):
	res = {}
	for k1,w in dic.items():
		try:
			k2 = keys[k1]
			res[k2] = w
		except KeyError:
			res[k1] = w
	return res

def ldickey(ldic,keys):
	res = []
	for dic in ldic:
		dic = dickey(dic,keys)
		res.append(dic)
	return res

#

##### DIREKT ###############
if __name__=='__main__':
	from loch import *
	x = labomi+'a.txt'
	y = labomi+'b.txt'
	x = labomi+'b.txt'
#	y = labomi+'c.txt'
	z = tsv8kml(x)
	print( z )
#	kbench.enfin()
