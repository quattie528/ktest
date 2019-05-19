#!/usr/bin/python

### MODULES ###
import os
#import pprint
#
#import attrdict
#
#from datsun import *
#import xz
#import kbench
#
#1:battery,2:pip,3:mygen,4:myopus

### VARIABLES ###
debug = True

#

#################
### DIR /B /S ###
#################
# suchen dateien einschließlich Subordners
def dirbs(pfad): # dir /b /s (Windows Batch Command)
	if pfad == './': pfad = '.'
	assert os.path.isdir(pfad)
	res = []
	for tp in os.walk(pfad):
		eigen = tp[0] + '/'
		dateien = tp[2]
		for datei in dateien:
			datei = eigen + datei
			datei = datei.replace('\\','/')
			if pfad == '.': datei = datei[2:]
			res.append(datei)
	res = [ x.replace('//','/') for x in res ]
	return res

def folders(eigen):
	d = os.walk(eigen)
	res = []
	for tp in d:
		tmp = adic()
		tmp.base = tp[0]
		tmp.dirs = tp[1]
		tmp.files = tp[2]
		#
		tmp.base += '/'
		tmp.base = tmp.base.replace('\\','/')
		tmp.base = tmp.base.replace('//','/')
		res.append(tmp)
	return res

def latest(pfad,datei):
	assert os.path.exists(pfad)
	drs = os.listdir(pfad)
	base = re.sub('\..+?$','',datei)
	#
	res = ''
	for x in sorted(drs):
		if not re.search(base,x): continue
		res = x
	return x

def filetoday(datei):
	m = re.search('(.+)\.(.+?)$',datei)
	datei = m.group(1)
	datei += '_'
	datei += xt.heute()
	datei += '.'
	datei += m.group(2)
	return datei

### LETZTEDATEI ###
def letztedatei(pfad):
	assert '/' in pfad
	assert( isinstance(pfad, str) )
	#
	if '*' in pfad:
		datei = re.search('(.+/)(.+)\*(.+)',pfad)
		pfad = datei.group(1)
		zweck1 = datei.group(2)
		zweck2 = datei.group(3)
		#
		lis = os.listdir(pfad)
		lis = [ x for x in lis if zweck1 in x ]
		lis = [ x for x in lis if zweck2 in x ]
	else:
		datei = re.search('(.+)/(.+)',pfad)
		pfad = datei.group(1) + '/'
		zweck = datei.group(2)
		#
		lis = os.listdir(pfad)
		lis = [ x for x in lis if re.search(zweck,x) ]
		lis = [ x for x in lis if not '~' in x ]
	#
	if lis == []: return ''
	lis.sort()
	return pfad+lis[-1]

def mkdir(pfad):
	while 1:
		try:
			os.mkdir(pfad)
			break
		except PermissionError:
			continue

def time4file(x):
	assert( isinstance(x, str) )
	if not os.path.exists(x):
		return x
	m = re.search('(.+)(\..+)',x)
	x1 = m.group(1)
	x2 = m.group(2)
	#
	zt = xt.jetzt()
	zt = zt.replace(' ','_')
	zt = zt.replace(':','')
	#
	return ''.join([x1,'_',zt,x2])

#

###################
### ORDNERGRÖßE ###
###################
def ordnergrose(pfad):
	ds = dirbs(pfad)
	res = 0
	for d in ds:
		res += os.path.getsize(d)
	return res

def b2k(x): return x // ( 1024 ** 1 )
def b2m(x): return x // ( 1024 ** 2 )
def b2g(x): return x // ( 1024 ** 3 )
def b2t(x): return x // ( 1024 ** 4 )

#

##### DIREKT ###############
if __name__=='__main__':
	import pprint
	import kbench
	dd = ordnergrose('D:/')
	print( dd )
	ee = b2m(dd)
	print( ee )
	kbench.jetzt()
