#!/usr/bin/python

### MODULES ###
import xz
import os
#import kbench
from datsun import *
#
import mich.will2

### VARIABLES ###
debug = True
ERSTES_TESTAMENT = False

#

#################
### TESTAMENT ###
#################
def testament(x):
	### VARIABLES ###
	import atexit
	global ERSTES_TESTAMENT
	debugger = mich.will2.DATEI4DEBUGGER

	### ERST FALL ###
	if ERSTES_TESTAMENT == False:
		ERSTES_TESTAMENT = True
		fx = lambda: print(open(debugger,encoding='utf-8').read())
		gh = open(debugger,'w',encoding='utf-8')
		gh.write('%'*50)
		gh.write("\n")
		gh.write("[[ TESTAMENT ]]\n")
		gh.close()
		atexit.register(fx)
		#
		fx = lambda : kbench.jetzt()
		atexit.register(fx)
		#
		fx = lambda : print('%'*50)
		atexit.register(fx)
	
	### NORMALE ###
	gh = open(debugger,'a',encoding='utf-8')
	gh.write(str(x))
	gh.write("\n")
	gh.close()

#

##### DIREKT ###############
if __name__=='__main__':
	testament(12312)
	testament(22312)
	testament(32312)
	testament(42312)
