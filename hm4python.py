#!/usr/bin/python

### MODULES ###
#from dateutil.parser import *
import sys
from datsun import *
import xz
#import xzplus
import re
import os

EIGENDATEI = 'a.txt'

#####################
### BASIC MODULES ###
#####################
def lookup(sache,dicfile):
	sache = sache2list(sache)
	print( dicfile ) #d
	try:
		dic = xz.txt2dic(dicfile)
	except:
		dicfile = labomi + dicfile
		dic = xz.obj2bin(dicfile)
	#
	res = []
	for x in sache:
		if x in dic:
			res.append(dic[x])
		else:
			res.append(x)
	return res

def replace(sache,listfile):
	sache = sache2list(sache)
	sache = "\n".join(sache)
	try:
		dic = xz.txt2dic(listfile)
	except:
		listfile = labomi + listfile
		dic = xz.obj2bin(listfile)
	tbl = xz.txt2tbl(listfile)
	for lis in tbl:
		vor = lis[0]
		nach = lis[1]
		sache = sache.replace(vor,nach)
	return sache
"""
#list and dict have same scores
#list : 4.46 sec. / 3.46 sec.
#dict : 4.30 sec. / 3.57 sec.
#so I chose the former one

def replaceB(sache,dicfile):
	dic = xz.txt2dic(dicfile)
	for k,v in dic.items():
		sache = sache.replace(k,v)
	return sache
"""

def sache2list(sache):
	if isinstance(sache, str):
		sache = sache.rstrip()
		sache = sache.split("\n")
		return sache
	elif isinstance(sache, list):
		return sache
	else:
		assert( isinstance(obj, list) )

#

###############################################################
### SPECIAL MODULES ###
#######################

### ID LITE ###
def idlite(sache,eigen='ID',both=False):
	sache = sache2list(sache)
	hdr = []
	dic = {}
	i = 1
	for x in sache:
		if not x in hdr:
			hdr.append(x)
			dic[x] = eigen + ('%03d' % i)
			i += 1
	res = []
	for x in sache:
		res.append( dic[x] )

	### AUSGABE ###
	if both == True:
		return zip(sache,res)
	else:
		return res

### MARUO REPACE ###
def replace4maruo(sache):
	sache = sache2list(sache)
	res = []
	for x in sache:
		y = x.split("\t")
		if len(y) == 1:
			y.append('')
		x = 'replaceallfast "%s","%s", regular;' % (y[0],y[1])
		res.append(x)
	return res

def pydateutil(sache):
	import xt
	sache = sache2list(sache)
	sache = [ parsetime(y) for y in sache ]
	sache = [ xt.z2s(y) for y in sache ]
	return sache

def thiszip(sache):
	sache = sache2list(sache)
	res = []
	tmp = []
	for x in sache:
		if re.search('^----+$',x):
			res.append(tmp)
			tmp = []
		else:
			tmp.append(x)
	res.append(tmp)
	res = transpose(res)
	#
	tmp = []
	for x in res:
		x = "\t".join(x)
		tmp.append(x)
	return tmp

### MY UNIQ ###
def thisuniq(sache):
	sache = sache2list(sache)
	t1 = len(sache)
	sache = uniq(sache)
	t2 = len(sache)
	y = '%d -> %d (%f%%)' % ( t1, t2, t2/t1*100 )
	sys.stderr.write(y)
	return sache

def thisuniq2(sache):
	import xkr

	des = sache2list(sache)
	des = [ [x] for x in des ]

	for i,x in enumerate(des):
		v = xkr.var2sha256(x[0])
		des[i].append(v)

	pruf = [ x[1] for x in des ]
	tmp = []
	for i,x in enumerate(pruf):
		if x in tmp:
			des[i].append(2)
		else:
			tmp.append(x)
			des[i].append(1)
	des[0][-2] = '<sha256>'
	des[0][-1] = '<dup?>'

	lis = [ x[2] for x in des ]
	lis = [ x for x in lis if x == 2 ]
	t1 = len(des)
	t2 = len(lis)
	y = '%d -> %d (%f%%)' % ( t1, t2, t2/t1*100 )
	sys.stderr.write(y)

	return des

### MY SORT ###
def thissort(sache):
	sache = sache2list(sache)
	sache.sort()
	return sache

### MY SORT REVERSE ###
def thissortR(sache):
	sache = sache2list(sache)
	sache.sort()
	sache.reverse()
	return sache

### MY REVERSE ###
def thisreverse(sache):
	sache = sache2list(sache)
	sache.reverse()
	return sache

### MY TRANSPOSE ###
def thistranspose(sache):
	sache = xz.str2tbl(sache)
	sache = transpose(sache)
	sache = [ "\t".join(lis) for lis in sache ]
	return sache

### MY RANDOM ###
def thisrandom(sache):
	import random
	sache = sache2list(sache)
	res = [ [x,random.random()] for x in sache ]
	res = sorted(res,key=lambda d:d[1])
	res = [ x[0] for x in res ]
	#
	assert not res == sache
	assert sorted(res) == sorted(sache)
	return res

### 37) MY LOOKUP ###
def thislookup(sache,dicfile):
	sache = sache2list(sache)
	if not os.path.exists(dicfile):
		dicfile = labomi + dicfile
#	print( os.getcwd() ) #d
#	print( dicfile ) #d
	dic = xz.txt2dic(dicfile)
	res = []
	for x in sache:
		if x in dic:
			res.append(dic[x])
#			print( dic[x] ) #d
		else:
			res.append(x)
	return res

def thislookup1v1(sache,dicfile):
	sache = sache2list(sache)
	assert len(sache) == len(uniq(sache))
	tbl = xz.txt2tbl(dicfile)
	dic = { lis[0]:"\t".join(lis[1:]) for lis in tbl }
	res = []
	for x in sache:
		if x in dic:
			res.append(dic[x])
		else:
			res.append(x)
	return res

### 38) COUNT VALUE ###
def countvalue(sache):
	sache = sache2list(sache)
	dic = {}
	res = []
	for x in sache:
		if x in dic:
			dic[x] += 1
		else:
			dic[x] = 1
		res.append(str(dic[x]))
	return res

### 39) UNIXTIME to DATETIME ###
def unixtime2datetime(sache):
	import xt
	sache = sache2list(sache)
	res = []
	for y in sache:
		if y.isdigit():
			y = int(y)
			y = xt.u2p(y)
		res.append(str(y))
	return res

#

### 2017-10-10) LIST to EVAL ###
def lis2eval(sache):
	sache = sache2list(sache)
	res = []
	for x in xz.txt2lis('a.txt'):
		try:
			y = eval(x)
		except SyntaxError:
			y = x
		except NameError:
			y = x
		y = str(y)
		res.append(y)
	return res

#

###############################################################
### TEIL MODULES ###
####################

### 121) MAKE TITLE for FUNCTION ###
def maketitle4function(sache,feile):
	k = feile[-3:-1]
	if k == '.mac': k = '/'
	elif k == '.tex': k = '%'
	else: k = '#'
	#
	sache = sache.rstrip()
	sache = sache.lstrip()
	n = len(sache)
	#
	y = k * 1
	y += "\n\n"
	y += k * (n+8)
	y += "\n"
	y += k * 3
	y += " "
	y += sache
	y += " "
	y += k * 3
	y += "\n"
	y += k * (n+8)
	print( y ) #d
	return y

###############################################################
### NO-OUTPUT MODULES ###
#########################

def lis2cnt(sache):
	sache = sache2list(sache)
	dic = {}
	res = []
	for x in sache:
		if x in dic:
			dic[x] += 1
		else:
			dic[x] = 1
	kys = list( dic.keys() )
	kys.sort()
	res = [ '%s\t%s' % (k,dic[k]) for k in kys ]
	return res

def belt2sum(sache):
	sache = xz.str2tbl(sache)
	sache = xz.bless(sache)
	res = {}
	for lis in sache:
		k = lis[0]
		v = int(lis[1])
		if not k in res: res[k] = 0
		res[k] += v
	#
	sache = ''
	for k in sorted(res.keys()):
		sache += "%s\t%d\n" % (k,res[k])
	#
	sache += "<SUM>\t%d\n" % sum(res.values())
	return sache

### MY CROSSTABLE ###
def thiscrosstable(sache):
	import crosstable
	sache = xz.str2tbl(sache)
	sache = xz.bless(sache)
	sache = transpose(sache)
	sache = crosstable.crosstable(sache[0],sache[1],sache[2])
	tmp = []
	for lis in sache:
		lis = [ str(x) for x in lis ]
		tmp.append(lis)
	sache = tmp
	sache = transpose(sache)
	sache = [ "\t".join(lis) for lis in sache ]
	return sache

"""
# bench at 2017-10-24
# 5.68 sec / my crosstable
# 0.99 sec / pandas
def thiscrosstable(sache):
	import pandas as pd
	sache = sache.replace(',','')
	feile = 'a.txt'
	xz.str2txt(sache,feile)
	df = pd.read_csv(feile,sep="\t")
	df.info()
	df2 = pd.pivot_table(
		df,
		index=df.im,
		columns=df.pref,
#		values=df.v,
	aggfunc='sum')
	df2 = df2.fillna(0)
	df2.to_csv(feile,sep="\t",encoding="utf8")
	return xz.txt2str(feile)
"""

### JUDGE UNIQUE OR NOT ###
def judgeuniq(vor):
	vor = sache2list(vor)
	nach = uniq(vor)
	vor.sort()
	nach.sort()
	if vor == nach:
		print( "ALL UNIQUE" )
	else:
		print( "SOME ARE DUPLICATED" )
	exit()

def checkdiff1(vor):
	vor = sache2list(vor)
	res = []
	for x in lis:
		if not x == '': last = x
		res.append(last)
	sache = "\n".join(res)
	return sache

def checkdiff2(vor):

	lis1 = xz.str2lis(x)
	lis2 = xz.txt2lis(opt)
	res1 = []
	res1.append('Exist in THIS, Does not exist in THAT')
	res2 = []
	res2.append('Exist in THAT, Does not exist in THIS')
	for x in lis1:
		if not x in lis2:
			res1.append(x)
	for x in lis2:
		if not x in lis1:
			res2.append(x)
	d1 = len(res1)
	d2 = len(res2)
	sache = "\n".join(res1)
	x += "\n------------------------------\n"
	x += "\n".join(res2)
	return x

def kmlsort(ori,key='tag'):
	ldic = xz.kml2ldic(ori)
	kopfer = xz.getkmlheader(ori)
	#
	if key in ldic[0]:
		ldic = sorted(ldic,key=lambda dic:dic[key])
	#
	kanvas = xz.ldic2kml(ldic,'',kopfer)
	kanvas += "\n"
	#
	assert xz.kml2ldic(kanvas) == ldic
	return kanvas

#

###############################################################
### DIESE PANDAS ###
####################
"""
def diese_xsumme(sache,dicfile):
	dic = xz.txt2dic(dicfile)
	df = sache2df(sache)
	df = wm2.xsumme(df,dic)
	return df2sache(df)

def diese_ysumme(sache,dicfile):
	dic = xz.txt2dic(dicfile)
	df = sache2df(sache)
	df = wm2.ysumme(df,dic)
	return df2sache(df)

def diese_xysumme(sache,dicfile):
	dic1 = dicfile[0] + '.tsv'
	dic1 = xz.txt2dic(dic1)
	dic2 = dicfile[1] + '.tsv'
	dic2 = xz.txt2dic(dic2)
	df = sache2df(sache)
	df = wm2.xysumme(df,dic1,dic2)
	return df2sache(df)
"""

#

##############################################################
### DIESE EXCEL ###
###################
def xlscountif4exist(sache,listfile):
	sache = sache2list(sache)
	lis = xz.txt2lis(listfile)
	res = []
	for x in sache:
		if x in lis:
			res.append(True)
		else:
			res.append(False)
	sache = [ str(x) for x in res ]
	return sache

def xlscountif4order(sache):
	sache = sache2list(sache)
	res = []
	dic = {}
	for x in sache:
		if x in ['','-','_']:
			res.append(0)
			continue
		elif x in dic:
			dic[x] += 1
			res.append(dic[x])
		else:
			res.append(1)
			dic[x] = 1
	sache = [ str(x) for x in res ]
	#
#	for i in range(len(sache)):
#		print( i )
#		i = -1 * i
#		"\n".join(sache[i:])
	return sache

#

##################
### REGENBODEN ###
##################
def regenbogen(sache):
	tmp = labomi + 'abc.def.123.txt'
	sicher = xz.notice
	xz.notice = False
	xz.str2txt(sache,tmp)
#	sache = xzplus.tsv8kml(tmp)
	sache = xz.tsv8kml(tmp)
	os.remove(tmp)
	xz.notice = sicher
	return sache

#

################
### BACKFILL ###
################
def backfill(sache):
	sache = sache2sachet(sache)
	assert not sache[0] == ''
	vor = lis[0]
	res = []
	for x in sache:
		if x == '':
			y = vor
		else:
			y = x
			vor = x
		res.append(y)
	return res

#

##### DIREKT ###############
if __name__=='__main__':
	pass
