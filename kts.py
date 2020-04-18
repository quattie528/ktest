#!/usr/bin/python

### MODULES ###
import datetime
#import os
#import pprint
#
#import clipboard
#import attrdict
#
from datsun import *
from loch import *
import xt
import xz
import kbench
#
#1:battery,2:pip,3:mygen,4:myopus

### VARIABLES ###
kbench.KBDEBUG = True
DEBUG = True
DEBUG = False
# SEH AUCH "zr_2017-10-23.py"
# SEH AUCH "zr.py"

#

###################
### TIME SERIES ###
###################
class timeseriesKK(dict): # dict-dict
	ini = 1980
	fin = 2000
	u = 'd' # d n q j
	header = []

	def __init__(my,ur,key,ein):
		my.header = ur.header
		for d in ur:
			if ein == 'd':
				d[key] = xt.s2d(d[key])
			elif ein == 'n':
				d[key] = int(d[key])
				assert xt.is_n(d[key])
			elif ein == 'q':
				d[key] = xt.s2q(d[key])
			elif ein == 'j':
				d[key] = int(d[key])
				assert d[key] < 10000
			#
			ref = d[key]
			my[ref] = d

	### MERGE ###
	def merge(db1,db2):
		assert db1.u == db2.u

		ts1 = db1.keys()
		ts2 = db2.keys()
		ts = [ min(ts1), min(ts2), max(ts1), max(ts2) ]
		ts.sort()
		db1.ini = ts[0]
		db1.fin = ts[-1]
		keys = list(db1.header) + list(db2.header)
		keys = uniq(keys)

		ini = db1.ini
		while 1:
			if not ini in db1:
				db1[ini] = {}
			for k in keys:
				if k in db1[ini]: continue
				try:
					db1[ini][k] = db2[ini][k]
				except KeyError:
					db1[ini][k] = None
			#
			tmp = [ db1[ini][k] for k in keys ]
			tmp = uniq(tmp)
			if tmp == [None]:
				db1.pop(ini)
			#
			if db1.u == 'd':
				ini += datetime.timedelta(days=1)
			elif db1.u == 'n':
				ini = xt.nplus(ini)
			elif db1.u == 'q':
				ini = xt.qplus(ini)
			elif db1.u == 'j':
				ini += 1
			if ini > db1.fin: break

###########
###  ###
###########
def txt2kts(txt,key='tag',ein='d'):
	ldic = xz.txt2ldic(txt)
	res = timeseriesKK(ldic,key,ein)
	return res

#

##### DIREKT ###############
if __name__=='__main__':
	for i in range(1):
		txt = labomi+'a.tsv'
		x = txt2kts(txt)
		txt = labomi+'b.tsv'
		y = txt2kts(txt)
		x.merge(y)
	kbench.enfin()

"""
[MATCH] pickle (python native) vs pandas
[RESULT] pandas is 5 times faster than pickle

[pickle]
Das Programme nimmt 00:00:51
	INI : 2020-02-09 18:53:37.726328
	FIN : 2020-02-09 18:54:29.693855

[pandas]
Das Programme nimmt 00:00:09
	INI : 2020-02-09 18:53:23.258570
	FIN : 2020-02-09 18:53:33.063062

"""
