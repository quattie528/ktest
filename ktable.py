#!/usr/bin/python

### MODULES ###
import xz
import re
from datsun import *

### VARIABLES ###

#

############
### TRIM ###
############
def trim(tbl,merk):
	"""
tbl[0][0] == 'X' : then not transpose
tbl[0][0] == 'Z' : then transpose
	"""
	### AUSNAHME ###
	assert( isinstance(tbl, list) )
	assert( isinstance(tbl[0], list) )
	#
	assert( isinstance(merk, str) )
	assert( len(merk) == 1 )
	assert not merk == 'X'
	assert re.match('^[A-Z]$',merk)

	### VARIABLES ###
	xs = []
	ys = []
	res = []
	neunzig = False
	if tbl[0][0] == 'Z':
		neunzig = True
	elif tbl[0][0] == 'X':
		neunzig = False
	else:
		print( 'ACHTUNG : UNECHTE WERT als %s' % tbl[0][0] )
	
	### HAUPT ###
	for i,x in enumerate(tbl[0]):
		if merk in x:
			xs.append(i)
		elif x == 'X':
			xs.append(i)
	for j,y in enumerate(tbl):
		if merk in y[0]:
			ys.append(j)
		elif y[0] == 'X':
			ys.append(j)
	#
#	print( xs, "\n", ys ) # debug
	if xs[0] == 0: xs.pop(0)
	if ys[0] == 0: ys.pop(0)

	cnt = 0
	for j in ys:
		lis = tbl[j]
		tmp = []
		for i in xs:
			tmp.append(lis[i])
		res.append(tmp)
	
	### AUSGABE ###
	if neunzig == True:
		res = transpose(res)
	return res

##### DIREKT ###############
if __name__=='__main__':
	krdb = trim(tbl,'A')
#	dbdb = trim(tbl,'Z')
