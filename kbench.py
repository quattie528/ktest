#!/usr/bin/python

### MODULES ###
#import os
#import pprint
#import copy
import datetime
import platform
import xz
import xt
import sys
#import time
from datsun import *
from loch import *

#../vexus/kbench_2019-06-05.py

### KONSTANT ###
Anfangszeit = datetime.datetime.now()
KBDEBUG = True
KBDEBUG = False

#

#############
### JETZT ###
#############
def jetzt(ruck=False):
	blick = datetime.datetime.now()
	delta = blick - Anfangszeit
	wert = xt.k2s(delta)
	if ruck == False:
		print( 'Das Programme nimmt ' + wert )
		print( "\tINI : %s" % Anfangszeit )
		print( "\tFIN : %s" % blick )
	return delta

#############
### ENFIN ###
#############
def enfin(befehl2=''):

	### DRITT ###
	if not myname == 'quattie528':
		jetzt()
		return False
	if KBDEBUG == True:
		jetzt()
		return False

	### KONSTANT ###
	zeitstempel = Anfangszeit
	apparat = platform.uname()[1]
	dauer = jetzt()
	#
	befehl1 = os.getcwd()
	befehl1 = befehl1.replace('\\','/')
	befehl1 += '/'
	befehl1 += sys.argv[0]
#	befehl1 = befehl1.replace(urPfad,'')
	#
	if len(sys.argv) == 1:
		arg = ''
	else:
		arg = list(sys.argv[1:])
		if sys.argv[0] == 'meemaa.py':
#			print( 11111111111 ) #d
			arg[0] = 'XXXXX'
		if arg[0] == 'MARUO':
			arg.pop(0)
			if len(arg) == 0:
				arg = ''
			else:
				arg = str(arg)
	#
	lis = [zeitstempel,apparat,dauer,befehl1,befehl2,arg]
	lis = [ str(x) for x in lis ]
	lis = "\t".join(lis)
	#
	gh = open(kbenchlog,'a',encoding='utf-8')
	gh.write(lis)
	gh.write("\n")
	gh.close()
	#
#	exit() #d
#	print( dauer ) #d
	return dauer
	return True

#

############################
### TAFEL für FUNKTIONEN ###
############################
def tafel4fx(tafel,titel,beispiel=[]):

	### DRITT ###
	if not myname == 'quattie528':
		jetzt()
		return False

	### TOR ###
	assert isinstance(titel, str)
	if not beispiel == []:
		assert isinstance(beispiel, list)
	for lis in tafel:
		assert isinstance(lis[0], int)
		assert isinstance(lis[1], str)
#		assert isinstance(lis[2], function)

	### VARIABLES ###
	res = []
	res.append(['#','HAUPT','FX','ZEIT','TAG'])
	#
	erst = datetime.datetime.now()
	tick = datetime.datetime.now()
	tag  = datetime.date.today()

	### HAUPT ###
	for lis in tafel:
		tick = datetime.datetime.now()
		nummer  = lis[0]
		wort    = lis[1]
		aufgabe = lis[2]
		#
		if not beispiel == []:
			if not nummer in beispiel:
				continue
		#
		aufgabe()
		tack = datetime.datetime.now()
		zt = tack - tick
		#
		lis = [nummer,titel,wort,zt,tag]
		res.append(lis)
		tick = tack

	### ENDLICH ###
	zt = tack - erst
	lis = [99,titel,'ΣΣ',zt,tag]
	res.append(lis)

	### VORSTELLEUNG ###
	y = 'STATISTIK / ' + titel
	print( rahmen(y,'%',True) )
	res.append( res[0] )
	xz.show(res)

	### AUSGABE ###
	res.pop(0)
	res.pop()
	gh = open(kbenchset, 'a',encoding='utf-8')
	y = "### %s @ %s ###\n" % ( titel, tag )
	gh.write( y )
	for lis in res:
		y = [ str(x) for x in lis ]
		y = "\t".join(y)
		gh.write(y)
		gh.write("\n")
	gh.write("#\n")
	gh.close()

	### PRUFUNG ###
	gh = open(kbenchset,'r',encoding='utf-8')
	lis = gh.read()
	lis = lis.split("\n")
	lis = [ x for x in lis if "###" in x ]
	#
	res = {}
	for x in lis:
		if x in res:
			res[x] += 1
		else:
			res[x] = 1
	for x,n in res.items():
		if n == 1: continue
		y = x.replace('### ','')
		y = y.replace(' ###','')
		y = y + ' / ' + str(n)
		y = 'DOPPEL HIER : '

#

##### DIREKT ###############
if __name__=='__main__':

	mode = 1
	if mode == 1:
		tbl = [
			[41,'1+1',lambda: 1+1],
			[42,'2+1',lambda: 2+1],
			[43,'1+3',lambda: 1+3],
		]
		tafel4fx(tbl,'test')
