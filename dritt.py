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
import kbench
#
#1:battery,2:pip,3:mygen,4:myopus

### VARIABLES ###
DEBUG = True
DEBUG = False
#

###############################
### TEMPORÄRER ORDNER SUCHE ###
###############################
def tempordnersuche():
	if os.name == 'posix': return '/tmp/'
	import subprocess
	mitte = 'a.txt'
	befehl = 'echo %TEMP% > '+mitte
	subprocess.call(befehl,shell=True)
#	subprocess.Popen(befehl,shell=True)
	with open(mitte, 'r',encoding='utf-8') as fh:
		pfad = fh.read()
	os.remove(mitte)
	#
	pfad = pfad.strip()
	pfad = pfad.replace('\\','/')
	if not pfad[-1] == '/':
		pfad += '/'
	return pfad

#

#######################
### WELCHER BROWSER ###
#######################
def which_browser():
	pfad1 = 'C:/Program Files/'
	pfad2 = 'C:/Program Files (x86)/'
	ausgabe = EINGRIFF + 'browser.bin'

	if os.path.exists(ausgabe):
		res = xz.bin2obj(ausgabe)
#		print( 111 ) #d
		if ['heute'] == xt.heute():
			return True

	res = {}
	res['heute'] = xt.heute()
	for pfad in [pfad1,pfad2]:
		ds = xf.get_all_files(pfad)
		for d in ds:
#			print( '-'*40 )
#			print( d )
#			print( d[-11:] )
			if d[-10:] == 'chrome.exe':
#				print( d )
				res['chrome'] = d
				break
			elif d[-11:] == 'firefox.exe':
#				print( d )
				res['firefox'] = d
				break
	xz.obj2bin(res,ausgabe)

#

################
### KONSTANT ###
################
EINGRIFF = tempordnersuche() + 'labomi/'

#

##### DIREKT ###############
if __name__=='__main__':
	kbench.enfin(False,'')
