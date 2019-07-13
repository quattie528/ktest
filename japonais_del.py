#!/usr/bin/python

### MODULES ###
import os
import xz
import cnvk
from datsun import *

### VARIABLES ###
ZEN2HAN = 'conf/zen2han.belt'
### DEBUG ###
debug = True

#

##################
### ZEN zu HAN ###
##################
def zen2han(x):
	global ZEN2HAN
	if isinstance(ZEN2HAN, str):
		## Smart Methode ##
		pfad = os.path.dirname( __file__ )
		pfad = os.path.join( pfad, ZEN2HAN )
		pfad = pfad.replace('\\','/')
#		print( pfad ) #d
		ZEN2HAN = xz.txt2dic(pfad)
		#
		## Alt Methode ##
		y = os.getcwd()
		os.chdir(y)
		assert( isinstance(ZEN2HAN, dict) )

	for k,w in ZEN2HAN.items():
#		print( k,w,x )
		x = x.replace(k,w)
	return x

def hira2kata(x):
	x = cnvk.convert(x, cnvk.Z_KATA, cnvk.HIRA2KATA)
	return x
def kata2hira(x):
	x = cnvk.convert(x, cnvk.Z_KATA, cnvk.KATA2HIRA)
	return x

"""
https://www.headboost.jp/python-check-the-length-of-strings/

F(Fullwidth)：全角文字を表す。全角英数など
H(Halfwidth）：半角文字を表す。半角カナなど
W(Wide）：漢字や仮名文字、句読点など東アジアの文字
Na(Narrow)：半角英数など
A：(Ambiguous）：ギリシア文字やキリル文字など
N(Neutral)：全角でも半角でもない。アラビア文字など
"""

def len(wert):
	import unicodedata
	assert( isinstance(wert, str) )
	res = 0
	for x in wert:
#		print( type(x),x ) #d
		if unicodedata.east_asian_width(x) in 'FWA':
			res += 2
		else:
			res += 1
	return res

##### DIREKT ###############
if __name__=='__main__':
	x = 'unkoうんこ'
	x = len(x)
	print( x )
#	kbench.jetzt()
