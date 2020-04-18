#!/usr/bin/python

### MODULES ###
#import datetime
import os
#import pprint
#
#import clipboard
#import attrdict
#
from datsun import *
from loch import *
import xf
import kbench
#
#1:battery,2:pip,3:mygen,4:myopus

### VARIABLES ###
kbench.KBDEBUG = True
DEBUG = True
DEBUG = False

#

###########
###  ###
###########
"""
def ein2aus(des,aux):
	res = False
	if os.path.exists(aux):
		if DEBUG == True:
			print( '[UR  ]', xf.mtime(des), '||', des ) #d
			print( '[NACH]', xf.mtime(aux), '||', aux ) #d
		if xf.mtime(des) <= xf.mtime(aux):
			res = True
	#
	if DEBUG == True and res == False:
		print( '[undo]',aux ) #d
	elif DEBUG == True and res == True:
		print( '[do]',aux ) #d
	return res
"""

def viel2aus(eingaben,ausgabe,pfad=''):
	if pfad == '':
		pass
	else:
		eingaben = [ pfad + d for d in eingaben ]
	eingabe = xf.aeltest(eingaben)
	res = ein2aus(eingabe,ausgabe)
	return res

##### DIREKT ###############
if __name__=='__main__':
	pass
	kbench.enfin()
