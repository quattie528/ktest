#!/usr/bin/python

"""
2018-10-05
xe.py->fx.py

2018-10-07
I have to wait for this decision, because of speed to refer
When I MAKE, maybe pandas is better
When I REFER, ddic is faster
So I should reconsider it

xe(pandas) 10.688310
fx(ddic)    6.219101
"""

### MODULES ###
import os
import datetime
import pprint
#
#import attrdict
#
from datsun import *
import xt
import xz
import kbench
#
#1:battery,2:pip,3:mygen,4:myopus

### VARIABLES ###
debug = True
debug = False
#
FXDB = {}
FXDB4IM = {}
TAGE = []
HEUTE = ''

### KONSTANT ###
#D:\var\lib\xe\
UR = 'D:/var/lib/xe/'
#UR = 'B:/var/db/'
UR = 'D:/onedrive/comp/mydata/fx/'
XE_DB1z = UR + 'alles2001-2007.ddic'
XE_DB1 = UR + 'alles.ddic'
XE_DB4 = UR + 'alles4im.ddic'

#cur(c) / date(d) / open(f) / low(f) / high(f) / close(f) / source(i)

#

#############
### FOREX ###
#############
def forex(preis,des='USD',aux='JPY',tag=''): # X-RATES
	### KONSTANT ###
	global FXDB
	global FXDB4IM
	global HEUTE
	global TAGE
	global UR

	### BEDIGUNG ###
	if TAGE == []:
		TAGE = xz.txt2lis( UR + 'tage.tsv' )
		TAGE = uniq(TAGE)
	if not tag in TAGE:
		tag = HEUTE

	### INTMONAT ###
	if isinstance(tag, int):
		return forex4im(preis,des,aux,tag)
	#
	if not des == 'USD':
		if not des in FXDB:
			eingang = UR + 'USD2%s.dic' % des
			FXDB[des] = xz.bin2obj(eingang)
	if not aux == 'USD':
		if not aux in FXDB:
			eingang = UR + 'USD2%s.dic' % aux
			FXDB[aux] = xz.bin2obj(eingang)
	#
	if tag == '':
		if HEUTE == '':
			tag = xz.txt2tbl( UR + 'USD2JPY.tsv' )
			HEUTE = tag[-1][0]
			tag = HEUTE
#			print( tag ) #d
		else:
			tag = HEUTE
#		tag = '2018-10-01'

	### AUSGABE ###
	if des == 'USD':
#		print( '[AUX]',aux,'[TAG]',tag,'[PREIS]',preis ) #d
		preis = float(FXDB[aux][tag]) * preis
	elif aux == 'USD':
		preis = preis / float(FXDB[des][tag])
	else:
		des = float(FXDB[des][tag])
		aux = float(FXDB[aux][tag])
		preis = preis / des * aux
	#
#	return tag,preis #d
	return preis

def forex4im(preis,des='USD',aux='JPY',tag=''): # X-RATES
	global FXDB4IM
	if FXDB4IM == {}:
		FXDB4IM = xz.bin2obj(XE_DB4)
	if des == 'USD':
		preis = FXDB4IM[aux][tag] * preis
	elif aux == 'USD':
		preis = preis / FXDB4IM[des][tag]
	else:
		des = FXDB4IM[des][tag]
		aux = FXDB4IM[aux][tag]
		preis = preis / des * aux
	#
#	return tag,preis #d
	return preis

#-------------------------------------------------

def jpy2usd(preis,tag=''):
	return forex(preis,'JPY','USD',tag)
def usd2jpy(preis,tag=''):
	return forex(preis,'USD','JPY',tag)
def fx2d(preis,wahrung,tag=''):
	return forex(preis,wahrung,'USD',tag)
def d2fx(preis,wahrung,tag=''):
	return forex(preis,'USD',wahrung,tag)

#

##### DIREKT ###############
if __name__=='__main__':
	mode = 3
	if mode == 1:
		import sammel
		sammel.xrates2alles() # er nimmt 02:58.889941 -> 00:11.500978
#		sammel.xrates2jedes() # er nimmt 00:09.547921
	elif mode == 2:
		x = 10000
		for i in range(1000000):
			x += 1
			y = forex(x,'EUR','JPY',201212)
			print( y )
	elif mode == 3:
		x = 10000
		print( forex(x,'JPY','USD') )
		print( forex(x,'USD','JPY') )
		print( forex(x,'JPY','EUR') )
		print( forex(x,'EUR','JPY') )
		print( usd2jpy(10000) )
		print( fx2d(10000,'GBP') )
		print( d2fx(10000,'GBP') )
		print( forex(x,'EUR','JPY',201212) )
	elif mode == 4:
		dsy = 33.475  # BN (market capitalization)
		ora = 193.560 # BN (market capitalization)
		res = forex(dsy,'EUR','USD')
		print( res )
	kbench.jetzt()

"""
[BENCHMARK]
2018-09-23	xrates2fxdb()	Das Programme nimmt 00:12.516436
"""
