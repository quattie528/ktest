#!/usr/bin/python

### MODULES ###
import datetime
import pprint
import os
#
#import attrdict
import pandas
#
from datsun import *
import xz
import xt
#import kbench

### VARIABLES ###
debug = True
debug = False

### BESTIMMUNG ###
"""
[Kerzenchart]
tag	ini	min	max	fin
2018-10-06	150	120	180	160
[Kerzenchart B]
tag	ini	min	max	fin	vol	src
2018-10-06	150	120	180	160	2000000	quandl
[Zeitreiche <= dict]
tag	wert(fin)
2018-10-06	150
"""

"""
tstbl
bstbl
pltbl

txt2png, tsv2png, tsv2pie, etc...
tstbl2png on pythonista
	(option, free time, (im, q, j)
	isn't there any good names for im?

bstbl2png (2 block stack)
pltbl2png (1 stack)
plttbl2png (linear)

var:titel (and country)
(example of Banque Mondial)

"""

#

######################
### IST ZEITREIHEN ###
######################
def istzr(tbl):

	mode = 'n'

	### X : ZEIT ###
	lis = tbl[0].copy()
	lis = xz.bless(lis)
	lis.pop(0)
	i = lis.pop(0)
	#
	if 'Q' in str(i):
		mode = 'q'
	elif i < 3000:
		mode = 'j'
	elif i >= 198001 and i <= 300000:
		mode = 'n'

	## Typ Jahren ##
	if mode == 'j':
		for x in lis:
			if x - i == 1:
				i = x
				continue
			return False

	## Typ Quartal ##
	elif mode == 'q':
		i = int(i[0:4])
		for x in lis:
			if not 'Q': return False
			if not len(x) == 6: return False
			if not x[4] == 'Q': return False
			#
			j = int(x[0:4])
			q = int(x[5])
			if not q in [1,2,3,4]: return False
			if q == 1:
				if not j - i == 1: return False
			else:
				if not j == i: return False
			i = j

	## Typ IntMonat ##
	elif mode == 'n':
		for x in lis:
#			print( x, x-i,x % 100 ) #d
			if x - i == 1:
				i = x
				continue
			elif x % 100 == 1 and x - i == 89:
				i = x
				continue
			return False

	### Y : KOLONNE ###
	lis = [ x[0] for x in tbl ]
	lis.pop(0)
	tmp = lis.copy()
	tmp = uniq(tmp)
	lis.sort()
	tmp.sort()
	if lis == tmp:
		return True
	else:
		return False

def shorten(tbl,ziel='q'):
	pass

#

######################################
### ZEITREIHE TAGLICH zu MONATLICH ###
######################################
"""
def zrt2zrm(zrt):

	### KONSTANT ###
	tage = []
	konv = {}
	konv1 = []
	konv2 = []

	### VORBEREITUNG ###
	if isinstance(zrt, dict):
		res = zrt.copy()
	elif isinstance(zrt, pandas.core.series.Series):
		res = { x:y for x,y in zrt.items() }
	elif isinstance(zrt[0], list):
		res = { x[0]:x[1] for x in zrt }
	else:
		print( '!!! List or Dict !!!' )
		assert( isinstance(x, dict) )
	#
	tage = zrt.keys()
	tage = list(tage)
	tage.sort()
	#
	for tag1 in tage:
		tag2 = xt.s2d(tag1)
		im = tag2.year * 100 + tag2.month
		konv[im] = tag1
	konv = { w:k for k,w in konv.items() }

	### HAUPT ###
	zrm = {}
	for tag,im in konv.items():
		wert = res[tag]
		zrm[im] = wert

	### AUSGABE ###
	return zrm
"""

#

###################################
### PANDAS zu ZEITREIHE-TAGLICH ###
###################################
def df2zrt(df):
	res = {}
	for tag,dic in df.T.iteritems():
		wert = dic['fin']
		tag = str(tag)
		wert = float(wert)
		res[tag] = wert
	return res

################################################
### ZEITREIHE-TAGLICH zu ZEITREIHE-MONATLICH ###
################################################
def zrt2zrm(zrt):
	tage = zrt.keys()
	tage = list(tage)
	tage.sort()

	subdic = {}
	for tag in tage:
		im = tag[0:4] + tag[5:7]
		im = int(im)
		subdic[im] = tag

	zrm = {}
	for im,tag in subdic.items():
		zrm[im] = zrt[tag]

	return zrm

#

##### DIREKT ###############
if __name__=='__main__':
	pass
