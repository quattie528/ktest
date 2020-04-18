#!/usr/bin/python

### MODULES ###
import datetime
import os
import sys
import clipboard
import random
import pyDes
#
import xz
import kbench
from datsun import *

#

### VARIABLES ###
ABC1 = 'abcdefghijklmnopqrstuvwxyz'
ABC2 = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
NUMMER = '0123456789'
ABC1 = 'abcdefghijkmnopqrstuvwxyz' # ex. similar codes
ABC2 = 'ABCDEFGHJKLMNPQRSTUVWXYZ'  # ex. similar codes
NUMMER = '23456789' # ex. similar codes
CHARS = '!#%&' # G1
CHARS = '#'    # G2
CHARS = '#$+-/:=' # G3
#CHARS = '#$+-./:=?@[]^_`|' # mufg @ 2016-09-24

notice = True

#

####################
### GENERATE KEY ###
####################
def genkey(zehe,niveau=3):
	assert niveau <= 3
	assert niveau >= 1
	entfernung = ABC1 + ABC2
	if niveau >= 2:
		entfernung += NUMMER
	if niveau == 3:
		entfernung += CHARS
	entfernung = list(entfernung)

	res = ''
	for i in range(zehe):
		res += random.choice(entfernung)
	return res

#

################
### DES SALZ ###
################
def DESsalz(salz):
	if salz == 'now':
		salz = 'nownowno'
	else:
		n = len(salz) # 8 digits ist die Spezifikation
		if n == 1:
			salz = salz * 8
		elif n == 2:
			salz = salz * 4
		else:
			salz = salz * 4
			salz = salz[0:8]
		assert len(salz) == 8 # Das ist die Spezifikation
	k = pyDes.des(salz, pyDes.CBC, "\0"*8, pad=None, padmode=pyDes.PAD_PKCS5)
	return k

#

#####################
### VERSCHLUSSELN ###
#####################
def verschlusseln(kode,salz): # encrypt
	salz = DESsalz(salz)
	x = salz.encrypt(kode)
	return x

#

#####################
### ENTSCHLUSSELN ###
#####################
def entschlusseln(kode,salz): # decrypt
	salz = DESsalz(salz)
	x = salz.decrypt(kode)
	x = str(x)
	x = x[2:-1]
	return x

#

#########################
### KODE zu CLIPBOARD ###
#########################
def kode2clipboard(kode):
	if notice == False: return True
	clipboard.copy(kode)
	#
	print( '' )
	print( '### OUTPUTTING STORED PASSWORD ###' )
	print( '* memo : # for lousy depository' )
	print( '* E:/meemaa/eigen.bin' )
	print( '* %d chars' % len(kode) )
	print( '' )
	print( kode )

#

##### DIREKT ###############
if __name__=='__main__':
	pass
