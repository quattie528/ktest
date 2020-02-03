#!/usr/bin/python

"""
[ACHTUNG!!!] Verwenden niemals meine eigenen externen Module
"""

### MODULES ###
import os
import pprint
import re
import sys
import clipboard
#
from loch import *
from xy import transpose
from xy import flatten
from xy import adic
from xy import commify
#
#import dritt
#import xt # NEVER USE IT
#from xz import * # NEVER USE IT

#pprint.pprint( sys.path )
#exit()
#labomi = dritt.eingriff()

#

#############
### DRITT ###
#############
"""
try:
	from datsun1 import *
except ModuleNotFoundError:
	def usage(x):
		return sys.argv[1]
	def w2m(x):
		return x
"""

"""
### USAGE ###
def usage(x):
	import sys
	if len(sys.argv) == 1:
		x = x.replace('.py','')
		w = os.path.dirname(__file__)
		w = inconf + 'usage/%s.txt' % x
		if not os.path.exists(w):
			print('no args, no usage explanation')
			exit()
		with open(w, 'r',encoding='utf-8') as f: x = f.read()
		x = '-'*50 + "\n" + x
		print(x)
		exit() # 2018-12-09
	else:
		if sys.argv[1].isdigit():
			return int( sys.argv[1] )
		else:
			return sys.argv[1]
"""

### W zu Mac ###
def w2m(x):
	import platform
	if not platform.uname()[1] == 'mac.local':
		return x
#	x = x.replace('','')
	x = x.replace('D:/onedrive/','/User/user/OneDrive/')
	return x

#

############
### UNIQ ###
############
def uniq(lis): # ver2 @ 2017-12-16, dict ist schnell!
	res = {}
	for i,x in enumerate(lis):
		try:
			res[x]
		except KeyError:
			res[x] = i
		except TypeError: # unhashable type: 'list'
			res = [ # old type returns
				y
				for x,y in enumerate(lis)
				if lis[:x+1].count(y) == 1
			]
			return res
	res = [ [v,k] for k,v in res.items() ]
	res = sorted(res,key=lambda d:d[0])
	res = [ x[1] for x in res ]
	return res
#def uniq(var): # ver1, sehr langsam ! denn ver2
#	return [y for x,y in enumerate(var) if var[:x+1].count(y) == 1]
"""
[benchmark @ 2017-12-16]
			  ver1  vs  ver2
----------------------------
10000 lines : 1.121 vs 0.625
20000 lines : 4.500 vs 0.937
"""

#

#

#

### NEXTFILE ###
def nextfile(ext):
	alphabet = "abcdefghijklmnopqrstuvwxyz"
	for x in alphabet:
		feile = '%s.%s' % (x,ext)
		if os.path.exists(feile): continue
		return feile

### MY SORT ###
def mysort(lis,crit1):
	assert( isinstance(lis, list) )
	assert( isinstance(crit1, list) )
	crit2 = [ '%02d%s_' % ( (i+1), x ) for i,x in enumerate(crit1) ]
	res = []
	for x in lis:
		flg = False
		for i,k in enumerate(crit1):
			if re.match('^'+k,x):
				x = crit2[i] + x
				flg = True
				break
		if flg == False: x = '99ZZ_' + x
		res.append(x)
	res.sort()
	res = [ re.sub('^\d\d.+?_','',x) for x in res ]
	return res

def mysort2(tbl,pos,crit):
	assert( isinstance(lis, list) )
	assert( isinstance(crit1, list) )
	
#	for lis in tbl:
#		lis[]


def compfile(des,aux):
	import xkr
	des = xkr.f2md5(des)
	aux = xkr.f2md5(aux)
	if des == aux:
		print( "IDENTICAL" )
	else:
		print( "DIFFERENT" )
	print( 'des | %s' % des )
	print( 'aux | %s' % aux )

#from dateutil.parser import *
import dateutil.parser
def parsetime(x):
	assert isinstance(x, str)
	try:
		x = dateutil.parser.parse(x)
		return x
	except ValueError:
		return x

#

##############
### MY ZIP ###
##############
def myzip(arg,delim='---'):
	if isinstance(arg, str): arg = arg.split("\n")
	res = []
	lis = []
	for x in arg:
		if x == delim:
			res.append(lis)
			lis = []
		else:
			lis.append(x)
	if not lis == []:
		res.append(lis)

	ln = 0
	msg = 'Length must be same... : %d <-> %d'
	for x in res:
		assert isinstance(x, list)
		if ln == 0:
			ln = len(x)
		else:
			y = len(x)
			assert y == ln, msg % (y,ln)

	res = transpose(res)
	return res

#

def predict(*var):
	print( 'ERROR will happen soon...' )
	for v in var:
		print( "\t---", v )

def clip(x):
	clipboard.copy(x)
	print( '* CLIPPED : ' + str(x) )

def mopen(txt):
	import subprocess
	app = '"C:\\Program Files\\Maruo\\Maruo.exe" '
	txt = txt.replace('/','\\\\')
	subprocess.call(app+txt, shell=True)

#

def dprint(x):
	try:
		print( x )
	except UnicodeEncodeError:
		print( 'qqch' )

#

# methods @ 2017-12-16
def methods(obj):
	x = [
		method_name
		for method_name in dir(obj)
		if callable( getattr(obj, method_name) )
	]
	x.sort()
	return x

#

##############
### RAHMEN ###
##############
#Bügel
def rahmen(x,sym="#",bugel=False):
	x = x.rstrip()
	x = x.lstrip()
	#
	ln = len(x)
	ln += 8
	res = ''
	if bugel == True:
		res += "\n%s\n\n" % sym
	elif bugel == False:
		pass
	else:
		assert bugel in [True,False]
	res += sym * ln
	res += "\n"
	res += sym * 3
	res += ' '
	res += x
	res += ' '
	res += sym * 3
	res += "\n"
	res += sym * ln
	return res

#

###########################
### MY TEMPORARY FOLDER ###
###########################
def mytmp():
#	import tempfile
	if os.name == 'nt':
		pfad = 'C:/Users/{}/AppData/Local/Temp/'
		pfad = pfad.format(os.getlogin())
	elif os.name == 'posix':
		pfad = '/tmp/'
	return pfad

#

##### DIREKT ###############
if __name__=='__main__':
	import sys
	mode = 3
	if mode == 1:
	#   compfile(sys.argv[1],sys.argv[2])
	#   x = letztedatei(weg)
	#   print( x )
		x = methods('')
		print( x )
	elif mode == 2:
		x = mytmp()
		print( x )
	elif mode == 3:
		x = 111111
		print( 222 )
		y = commify(x)
		print( y )
