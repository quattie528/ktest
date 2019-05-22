#!/usr/bin/python

### MODULES ###
import os
import pprint
import copy
import datetime
import platform
import xz
import xt
import sys
#import time
from datsun import *

### KONSTANT ###
init = datetime.datetime.now()
try:
	import kbench1
	LOGDIC = kbench1.benchdic()
except ModuleNotFoundError:
	LOGDIC = {}
#pprint.pprint( LOGDIC ) #d

#

##############
### KBENCH ###
##############
class kbench():
	record = []
	track = 0
	title = ''

	def __init__(my):
		pass

	def tick(my,msg):
		my.title = msg
		my.track = datetime.datetime.now()

	def tack(my):
		assert not my.track == 0
		jjetzt = datetime.datetime.now()
		diff = jjetzt - my.track
		delta = xt.k2s(diff)
		#
		lis = [ my.title, delta ]
		lis.append( str(my.track)[0:19] )
		lis.append( str(jjetzt)[0:19] )
		my.record.append( lis )

	def output(my,ex):
		my.tick('')
		xz.tbl2txt(my.record,ex)

	def show(my):
		s = datetime.time()
		for x in my.record:
			s = xt.tplus( s, xt.s2z(x[1]) )
		#
		# 2017-10-08, ergänzen
#		print( type(s), ' / ',s )
		summe = '%02d:%02d.%6d' % (s.minute,s.second,s.microsecond)
		lis = ['Σ',summe,my.record[0][2],my.record[-1][-1]]
		my.record.append(lis)
		xz.show(my.record)
		my.record.pop()

class stoppuhr():
	spur = datetime.datetime.now()
	erst = copy.copy(spur)

	def tick(my,msg=''):
		delta = datetime.datetime.now() - my.erst
		s1 = delta.seconds
		ms1 = delta.microseconds
		ms1 = ms1 // 10000
		#
		delta = datetime.datetime.now() - my.spur
		s2 = delta.seconds
		ms2 = delta.microseconds
		ms2 = ms2 // 10000
		#
		delta = (s1,ms1,s2,ms2,msg)
		delta = 'TICK @ %3d:%03d & %3d:%03d || %s' % delta
		my.spur = datetime.datetime.now()
		print( delta )

#############
### JETZT ###
#############
def jetzt(ruck=False):
	blick = datetime.datetime.now()
	delta = blick - init
	wert = xt.k2s(delta)
	if ruck == False:
		print( 'Das Programme nimmt ' + wert )
		print( "\tINI : %s" % init )
		print( "\tFIN : %s" % blick )
		jetztbench(wert)
	return delta

def jetztbench(wert):
	global LOGDIC
	if LOGDIC == {}: return False
	#
	eigen = sys.argv[0]
	if len(eigen) == 4: return False
	#
	datei = LOGDIC['benchlog']
	print( datei ) #d
	fh = open(datei, 'a',encoding='utf-8')
	lis = [eigen,xt.jetzt(),wert]
	fh.write( "\t".join(lis) )
	fh.write("\n")
	fh.close()
	return True

#############
### ENFIN ###
#############
def enfin(dbg=False,befehl2=''):
	if dbg == False:
		jetzt()
		return False
	if LOGDIC == {}: return True

	### KONSTANT ###
	zeitstempel = init
	apparat = platform.uname()[1]
	dauer = jetzt()
	#
	urpfad = LOGDIC['urpfad']
	befehl1 = os.getcwd()
	befehl1 = befehl1.replace('\\','/')
	befehl1 += '/'
	befehl1 += sys.argv[0]
	befehl1 = befehl1.replace(urpfad,'')
	#
	if len(sys.argv) == 1:
		arg = ''
	else:
		arg = list(sys.argv[1:])
		if sys.argv[0] == 'meemaa.py':
			print( 11111111111 )
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
	ausgabe = LOGDIC['py4selbst']
	gh = open(ausgabe,'a',encoding='utf-8')
	gh.write(lis)
	gh.write("\n")
	gh.close()
	#
#	exit() #d
	return True

#

############################
### TAFEL für FUNKTIONEN ###
############################
def tafel4fx(tafel,titel,beispiel=[]):

	### TOR ###
	if LOGDIC == {}: return False
	#
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
	tag = datetime.date.today()

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
	ausgabe = LOGDIC['py4set']
	res.pop(0)
	res.pop()
	gh = open(ausgabe, 'a',encoding='utf-8')
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
	gh = open(ausgang,'r',encoding='utf-8')
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
#	x = kbench()
	#
#	y = stoppuhr()
#	y.tick()

	mode = 1
	if mode == 1:
		tbl = [
			[41,'1+1',lambda: 1+1],
			[42,'2+1',lambda: 2+1],
			[43,'1+3',lambda: 1+3],
		]
		tafel4fx(tbl,'test')
