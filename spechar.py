#!/usr/bin/python

#2019-02-17
#http://www.htmq.com/text/

### MODULES ###
import os
import xz
from datsun import *

### VARIABLES ###
DECODE = 'conf/html_decode.txt'
ENCODE = 'conf/html_encode.txt'
### DEBUG ###
debug = True

#

###################
### HTML DEKODE ###
###################
def decode(x):
	global DECODE
	if isinstance(DECODE, str):
		## Smart Methode ##
		pfad = os.path.dirname( __file__ )
		pfad = os.path.join( pfad, DECODE )
		pfad = pfad.replace('\\','/')
#		print( pfad ) #d
		DECODE = xz.txt2dic(pfad)
		#
		## Alt Methode ##
		y = os.getcwd()
		os.chdir(y)
		assert( isinstance(DECODE, dict) )

	for k,w in DECODE.items():
#		print( k,w,x )
		x = x.replace(k,w)
	return x


###################
### HTML ENKODE ###
###################
def encode(x):
	global ENCODE
	if isinstance(ENCODE, str):
		## Smart Methode ##
		pfad = os.path.dirname( __file__ )
		pfad = os.path.join( pfad, ENCODE )
		pfad = pfad.replace('\\','/')
#		print( pfad ) #d
		ENCODE = xz.txt2dic(pfad)
		#
		## Alt Methode ##
		y = os.getcwd()
		os.chdir(y)
		assert( isinstance(ENCODE, dict) )

	for k,w in ENCODE.items():
#		print( k,w,x )
		x = x.replace(k,w)
	return x


##### DIREKT ###############
if __name__=='__main__':
	x = 'unうん'
	x = len(x)
	print( x )
#	kbench.jetzt()
