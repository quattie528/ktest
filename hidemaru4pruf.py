#!/usr/bin/python

### MODULES ###
import platform
import os
from datetime import datetime as dt
#import pprint
#
#import attrdict
#
from datsun import *
#import xz
#import kbench
#
#1:battery,2:pip,3:mygen,4:myopus

### VARIABLES ###
debug = True
debug = False

#

##################
### DATEI META ###
##################
def dateimeta(x):
	(mode, inode, dev, nlink, uid, gid, size, atime, mtime, ctime) = os.stat(x)
	#
	if debug == True:
		print( mode )   # file mode (file type and bit of file mode)
		print( inode )
		print( dev )    # identifier of device
		print( nlink )  # number of hardlink
		print( uid )
		print( gid )
		print( size )
		print( atime )
		print( mtime )
		print( ctime )

	### WINDOWS ###
	if platform.system() == 'Windows':
		mtime = os.path.getmtime(x)
		ctime = os.path.getctime(x)
		atime = os.path.getatime(x)
		#
		mtime = mtime // 1
		ctime = ctime // 1
		atime = atime // 1

	### ORDNER ###
	ordner = os.path.abspath(x)
	ordner = ordner.replace(x,'')
	ordner = ordner.replace('\\','/')

	### GROS ###
	byte = size
	kbyte = byte / 1024
	mbyte = byte / 1024 / 1024
	
	### ZEIT ###
	atime = dt.fromtimestamp(atime)
	mtime = dt.fromtimestamp(mtime)
	ctime = dt.fromtimestamp(ctime)
	
	### AUSGABE 
	res = [
		'#' * 30,
		'NAME   : ' + x,
		'ORDNER : ' + ordner,
		'#',
		'BYTE   : %s B' % commify(byte),
		'KBYTE  : %0.3f KB' % kbyte,
		'MBYTE  : %0.3f MB' % mbyte,
		'#',
		'CTIME  : %s' % ctime,
		'MTIME  : %s' % mtime,
		'ATIME  : %s' % atime,
		'#' * 30,
	]
	#
	res = "\n".join(res)
	return res

####################
### N von ASSERT ###
####################
def n8assert(datei):
	import re
	
	fh = open(datei, 'r',encoding='utf-8')
	lis1 = fh.readlines()
	lis2 = []
	i1 = 0
	i2 = 0
	
	for x in lis1:
		if re.search('^#*\t*assert',x):
			i1 += 1
			lis2.append(x)
		elif re.search('^#*\t*try',x):
			i1 += 1
			lis2.append(x)
	#
	for x in lis2:
		y = re.findall('# TOR-?([\d\.]+)',x)
		if y == []: continue
		y = y[0]
		y = re.sub('.+\.','',y)
		y = int(y)
		if i2 < y: i2 = y
	#
	x = ''
	if i1 < i2:
		i1 = i2
		x = "* Nicht 'count' Aber Kommentar (TOR-%02d)\n" % i2
	x += "* Nummer von 'assert' ist %d\n" % i1
	print( x )
	return i1

#

##### DIREKT ###############
if __name__=='__main__':
#	print( dateimeta(x) )
	kbench.enfin(True,'')
