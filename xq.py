#!/usr/bin/python

### MODULES ###
import datetime
#import os
#import pprint
import traceback
import platform
import io
import sys
#import simplecrypt
#pip install simple-crypt
#
#from datsun import *
#import xz
import xkr
import kbench

### VARIABLES ###
DEBUG = True
DEBUG = False

#

#######################
### DRITT zu FEHLER ###
#######################
#2019-01-03
#http://otiai10.hatenablog.com/entry/2013/07/25/230315
#https://vaaaaaanquish.hatenablog.com/entry/2017/12/14/183225
def dritt2fehler(ex, ms, tb):

	### KONSTANT ###
	gh = io.StringIO()
	apparat = platform.uname()[1]
	grenzer = '%' * 40
	grenzer = "\n%s\n" % grenzer
	
	### HAUPT ###
	gh.write("<APPARAT>%s" % apparat)
	gh.write("\n")
	gh.write("<ZEIT>%s" % datetime.datetime.now())
	gh.write(grenzer)
	#
	gh.write("[ex] -> \t")
	gh.write(str(type(ex)))
	gh.write("\n")
	gh.write(str(ex))
	gh.write(grenzer)
	#
	gh.write("[ms] -> \t")
	gh.write(str(type(ms)))
	gh.write("\n")
	gh.write(str(ms))
	gh.write(grenzer)
	#
	gh.write("[tb] -> \t")
	gh.write(str(type(tb)))
	gh.write("\n")
	gh.write(str(tb))
	gh.write(grenzer)
	#
	gh.write("*** [traceback.print_tb] ***")
	gh.write("\n")
	traceback.print_tb(tb,file=gh)
	gh.write("\n")
	#
	err = str(type(ms))
	err = err.replace("<class '",'')
	err = err.replace("'>",'')
	err = err + ': ' + str(ms)
	gh.write(err)
	#
	### MESSAGE ###
	gh.seek(0)
	msg = gh.read()
	gh.close()
#	print( msg ) #d
	
	### AUSGABE ###
#	print( '%'*100 ) #d
	onlyyou = True
#	onlyyou = False
	if onlyyou == False:
		pwd = 'password'
#		msg = msg.encode('utf-8')
#		pwd = 'password'.encode('utf-8')
		msg = xkr.encode2(msg,pwd)
	gh = open('error.log', 'w')
	gh.write(msg)

"""
try:
	anyfunc()
except:
	### KONSTANT ###
	ex, ms, tb = sys.exc_info()
	xq.dritt2fehler(ex, ms, tb)
"""

##### DIREKT ###############
if __name__=='__main__':
	pass
#	abc()
#	kbench.enfin(False,'')
