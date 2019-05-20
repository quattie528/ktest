#!/usr/bin/python

### MODULES ###
#import datetime
import os
#import pprint
#
#import clipboard
#import attrdict
#
#from datsun import *
import xt
import xf
import xz
#import kbench
from mich.maj2 import MAJLOG1
from mich.maj2 import MAJLOG2
#
#1:battery,2:pip,3:mygen,4:myopus

### VARIABLES ###
DEBUG = True
DEBUG = False
#
if os.path.exists(MAJLOG2):
	MAJDIC = xz.bin2obj(MAJLOG2)
else:
	MAJDIC = {}

#

##############
### TIMBRE ###
##############
def timbre(name,feuille):
	temps = xf.ctime(feuille)
	temps = xt.u2p(temps)
	MAJDIC[name] = temps
	#
	tmp = xz.notice
	xz.notice = False
	xz.dic2txt(MAJDIC,MAJLOG1)
	xz.obj2bin(MAJDIC,MAJLOG2)
	xz.notice = tmp
	#
	x = 'Timbre a %s de %s' % (temps,name)

def timbreD(name,dossier):
	fs = os.listdir(dossier)
	feuille = fs[-1]
	return timbre(name,dossier+feuille)


##############
### ENCORE ###
##############
def encore(name,feuille):
	if not os.path.exists(feuille): return False
	print( feuille )
	temps = xf.ctime(feuille)
	temps = xt.u2p(temps)
	print( temps )
	if name in MAJDIC:
		if MAJDIC[name] == temps:
			x = 'Faite au %s de %s' % (temps,name)
			print( x ) #d
			return True
		else:
			return False
	return False

def encoreD(name,dossier):
	fs = os.listdir(dossier)
	feuille = fs[-1]
	return encore(name,feuille)

#

##### DIREKT ###############
if __name__=='__main__':
	timbre()
	kbench.enfin(False,'')
