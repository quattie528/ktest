#!/usr/bin/python

### MODULES ###
#import datetime
#import os
import pprint
#
#import clipboard
#import attrdict
#
#from datsun import *
import xz
import kbench
#

# Big Data [EN], Massendaten [DE], megadonnées [FR]
# grandi dati [IT], macrodatos [ES]

### VARIABLES ###
DEBUG = True
DEBUG = False

#

###########
###  ###
###########
def comp2ddic(altddic,neuddic,sicher):

	for k,w in neuddic.items():
		print( k )
		pprint.pprint( w )
		break

	### VORBEREITUNG ###
#	if isinstance(sicher, str): sicher = [sicher]
	assert isinstance(sicher, list) or isinstance(sicher, tuple)
	#
	kopfer = [ x for x in neuddic.keys() ]

	### HAUPT ###
	res = []
	for x in kopfer:
		if altddic[x] == neuddic[x]: continue
		#
		## Sichern ##
		tmp = {}
		for y in sicher: tmp[y] = neuddic[x][y]
		res.append( tmp )

	### AUSGABE ###
	return res
