#!/usr/bin/python

### MODULES ###
#import pandas as pd
import xz
from datsun import *

def crosstable(xs,ys,zs=[]):
	xs = pd.DataFrame([xs],[ys])
	ys = pd.DataFrame(ys)

def crosstable(xs,ys,zs=[]):
	ddic = {}
#	zs = [ int(v) for v in zs ]
	
	for x in xs:
		ddic[x] = {}
		for y in ys:
			ddic[x][y] = 0
	
	if zs == []:
		for x in range(len(xs)):
			zs.append(1)
	
	for i,x in enumerate(xs):
		y = ys[i]
		z = zs[i]
		ddic[x][y] += z
	
	res = [['/']]
	xks = sorted(ddic.keys())
	yks = sorted(list(set(ys)))
	#
	for x in xks:
		res[0].append(x)
	for y in yks:
		lis = [y]
		for x in xks:
			lis.append(ddic[x][y])
		res.append(lis)
	return res

#

#######################
### CROSS DICT-DICT ###
#######################
class xdic(dict):
	xs = []
	ys = []
	def __init__(my,xs,ys,ini=0):
		my.xs = []
		my.ys = []
		for x in xs:
			my[x] = {}
			if not x in my.xs:
				my.xs.append(x)
			for y in ys:
				if not y in my.ys:
					my.ys.append(y)
				my[x][y] = ini
	
	### AGGREGATE ###
	def aggr(my,xbelt={},ybelt={}):

		## Prufung ##
		assert( isinstance(xbelt, dict) )
		assert( isinstance(ybelt, dict) )
		# xs #
		if xbelt == {}:
			for x in my.xs:
				xbelt[x] = x
		else:
			xs2 = xbelt.keys()
			for x in my.xs:
				assert x in xs2, 'Kein >>%s<<' % x
		# ys #
		if ybelt == {}:
			for y in my.ys:
				ybelt[y] = y
		else:
			ys2 = ybelt.keys()
			for y in my.ys:
				assert y in ys2, 'Kein >>%s<<' % y
		
		## Haupt ##
		xvec = list( xbelt.values() )
		yvec = list(ybelt.values() )
		xvec.sort()
		yvec.sort()
		res = xdic(xvec,yvec)
		#
		for x1 in my.xs:
			x2 = xbelt[x1]
			for y1 in my.ys:
				y2 = ybelt[y1]
				res[x2][y2] += my[x1][y1]
		
		## ausgabe ##
		return res

#

	### AGGREGATE typus ###
	def aggrtyp(my,sym='m2j'):
		xbelt = {}
#		sym = 'm2q'
#		sym = 'm2oq'
		if sym == 'm2j':
			for x in my.xs:
				xbelt[x] = x // 100
		elif sym == 'm2q':
			for x in my.xs:
				j = x // 100
				m = x % 100
				if m in range(1,4):
					m = 'Q1'
				elif m in range(4,7):
					m = 'Q2'
				elif m in range(7,9):
					m = 'Q3'
				elif m in range(9,13):
					m = 'Q4'
				xbelt[x] = str(j) + m
		elif sym == 'm2oj':
			for x in my.xs:
				j = x // 100
				m = x % 100
				if m > 5: j += 1
				xbelt[x] = j
		elif sym == 'm2oq':
			for x in my.xs:
				j = x // 100
				m = x % 100
				if m in range(6,9):
					m = 'Q1'
				elif m in range(9,12):
					m = 'Q2'
				elif m in range(11,13):
					m = 'Q3'
				elif m in range(1,3):
					m = 'Q3'
				elif m in range(3,6):
					m = 'Q4'
				xbelt[x] = str(j) + m
		return my.aggr(xbelt)
	
	### SUM ###
	def sum(my):
		res = 0
		for x,d in my.items():
			for y,w in d.items():
				res += w
		return res
	
	def xsum(my):
		res = {}
		for x,d in my.items():
			res[x] = 0
			for y,w in d.items():
				res[x] += w
		return res
	
	def ysum(my):
		res = { y:0 for y in my.ys }
		for x,d in my.items():
			for y,w in d.items():
				res[y] += w
		return res

	### SHOW ###
	def to_tbl(my):
		tbl = []
		tbl.append( my.xs.copy() )
		tbl[0].insert(0,'/')
		for y in my.ys:
			lis = [y]
			for x in my.xs:
				lis.append( my[x][y] )
			tbl.append(lis)
		return tbl
	
	def show(my):
		xz.show(my.to_tbl())
	
	def to_txt(my,ausgabe):
		xz.tbl2txt(my.to_tbl(),ausgabe)

#

###########################
### TABLE to CROSS-DICT ###
###########################
def tbl2xdic(tbl):
	xs = tbl.pop(0)
	xs.pop(0)
	ys = [ y[0] for y in tbl ]
	res = xdic(xs,ys)

	### PRUF ###
	for i, lis in enumerate([xs,ys]):
		pruf = lis.copy()
		pruf.sort()
		gegen = uniq(pruf)
		for x in gegen:
			if pruf.count(x) >= 2:
				if i == 0:
					y = '* [XS] '
				elif i == 1:
					y = '* [YS] '
				y += 'Doppel Kopfer als >>%s<<' % x
				print( y )
		assert gegen == pruf

	### HAUPT ###
	for lis in tbl:
		y = lis.pop(0)
		for i,x in enumerate(xs):
			w = lis[i]
			res[x][y] = w
	return res

def txt2xdic(txt):
	tbl = xz.txt2tbl(txt)
	tbl = tbl2xdic(tbl)
	return tbl

"""
def ddic2xdic(ddic):
	xs = list(ddic.keys())
	ys = ddic[ xs[0] ].keys()
	#
	for x,d in ddic.items():
		assert ys == d.keys()
	ys = list(ys)
	#
	print( '*'*50 )
	print( xs )
	res = xdic(xs,ys)
	print( '*'*50 )
	print( res.xs )
	exit()
	for x,dic in ddic.items():
		for y,w in dic.items():
			res[x][y] = w
	print( '*'*50 )
	print( res.xs )
	print( res.ys )
	print( '*'*50 )
	return res
"""

#

##### DIREKT ###############
if __name__=='__main__':
	mode = 2
	if mode == 1:
		txt = 'a.tsv'
		tbl = xz.txt2tbl(txt)
		tbl = transpose(tbl)
		tbl = xz.bless(tbl)
		tbl = crosstable(tbl[0],tbl[1],tbl[2])
	#	tbl = crosstable(tbl[0],tbl[1],[])
		xz.show(tbl)
		xz.tbl2txt(tbl,'b.tsv')
	#
	elif mode == 2:
		tbl = xz.txt2tbl('a.tsv')
		tbl = xz.bless(tbl)
		tbl = tbl2xdic(tbl)
		#
		sym = 'm2oq'
		sym = 'm2oj'
		tbl = tbl.aggrtyp(sym)
		tbl.to_txt('b.tsv')
		print( tbl.sum() )

	elif mode == 3:
		x = xdic([1,2,3],[4,5,6])
		y = xdic([4,5,6],[7,8,9])
		print( x )
		print( y )
