#!/usr/bin/python

"""
[ACHTUNG!!!] Verwenden niemals meine eigenen externen Module
"""

### MODULES ###
import datetime
import os
#import pprint
#
#import clipboard
#import attrdict

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

	### MODULE ###
	import xf
	import xz

	pfad1 = 'C:/Program Files/'
	pfad2 = 'C:/Program Files (x86)/'
	ausgabe = eingriff() + 'browser.bin'

	if os.path.exists(ausgabe):
		res = xz.bin2obj(ausgabe)
#		print( 111 ) #d
		if ['heute'] == datetime.date.today():
			return True

	### HAUPT ###
	res = {}
	res['heute'] = datetime.date.today()
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

	### AUSGABE ###
	xz.obj2bin(res,ausgabe)

#

################
### KONSTANT ###
################
def eingriff():
	return tempordnersuche() + 'labomi/'

#

##### DIREKT ###############
if __name__=='__main__':
	print( eingriff() )
#	which_browser()
#C:\Users\kakagami\AppData\Local\Temp\labomi\
