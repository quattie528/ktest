#!/usr/bin/python

### MODULES ###
import hashlib # md5 is for encryption, not for hashing
import os
from functools import partial
import xz

#sha1()/sha224()/sha256()/sha384()/sha512()

#

####################
### FEILE to MD5 ###
####################
def f2md5(datei):
#	print( datei ) #d
	with open(datei, mode='rb') as f:
		d = hashlib.md5()
		for buf in iter(partial(f.read, 128), b''):
			d.update(buf)
	return d.hexdigest()

def var2kr(x,kr='md5'):
	if kr == 'md5':
		d = hashlib.md5()
	elif kr == 'sha1':
		d = hashlib.sha1()
	elif kr == 'sha224':
		d = hashlib.sha224()
	elif kr == 'sha256':
		d = hashlib.sha256()
	elif kr == 'sha384':
		d = hashlib.sha384()
	elif kr == 'sha512':
		d = hashlib.sha512()
	#
	x = str(x)
	x = x.encode('utf-8')
	d.update(x)
	return d.hexdigest()
def var2md5(v): return var2kr(v,'md5')
def var2sha1(v): return var2kr(v,'sha1')
def var2sha224(v): return var2kr(v,'sha224')
def var2sha256(v): return var2kr(v,'sha256')
def var2sha384(v): return var2kr(v,'sha384')
def var2sha512(v): return var2kr(v,'sha512')

#

###############
### COMPDIR ###
###############
def compdir(weg1,weg2,ext=''):
	datein1 = os.listdir(weg1)
	datein2 = os.listdir(weg2)
	if not ext == '':
		ext = '.' + ext
		datein1 = [ x for x in datein1 if ext in x ]
		datein2 = [ x for x in datein2 if ext in x ]
	datein = set(datein1+datein2)
	res = []
	
	for datei in sorted(datein):
		f1 = weg1 + datei
		f2 = weg2 + datei
		lis = [datei]
		if os.path.exists(f1):
			d1 = f2md5(f1)
		else:
			d1 = '-'
		#
		if os.path.exists(f2):
			d2 = f2md5(f2)
		else:
			d2 = '-'
		print( datei,d1,d2 )
		if d1 == d2: continue
		res.append([datei,d1,d2])

	res.insert(0,['FEILE','WEG1','WEG2'])
	return res

#

#http://docs.python.jp/2/library/hashlib.html
#> hashlib.sha224("Nobody inspects the spammish repetition").hexdigest()
#'a4337bc45a8fc544c03f52dc550cd6e1e87021bc896588bd79e901e2'

"""
### 2019-01-03 ###
#https://stackoverflow.com/questions/2490334/simple-way-to-encode-a-string-according-to-a-password
import base64
import pprint
def encode2(key, clear):
	enc = []
	for i in range(len(clear)):
		key_c = key[i % len(key)]
		print( clear[i],'/',key_c )
		enc_c = chr((ord(clear[i]) + ord(key_c)) % 256)
		enc.append(enc_c)
	var = base64.urlsafe_b64encode("".join(enc))
	return var

def decode2(key, enc):
	dec = []
	enc = base64.urlsafe_b64decode(enc)
	for i in range(len(enc)):
		key_c = key[i % len(key)]
		dec_c = chr((256 + ord(enc[i]) - ord(key_c)) % 256)
		dec.append(dec_c)
	return "".join(dec)
"""

##### DIREKT ###############
if __name__=='__main__':
	pass
