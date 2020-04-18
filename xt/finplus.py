#!/usr/bin/python

### MODULES ###
#from datetime import date as d
#from datetime import time as t
from datetime import date as dy # ein Alphabet ist gefehr
from datetime import time as tm # ein Alphabet ist gefehr
from datetime import datetime as dt
from datetime import timedelta as dl
import time
#import re
import os
#import calendar
#
from .xtbase import *
from .intmonth import *

### KONSTANT ###
N2QTABLE = {}
N2QBIN = os.path.dirname(__file__) + '/'
N2QBIN += 'im2q.bin'

#

###########################
### INTMONAT zu QUARTEL ###
###########################
#alt version als "../vetus/xt_teil_2020-03-08.py"
def n2qtafel():
#	if os.path.exists(N2QBIN): return True
	res = {}
	qq = [1,1,1,2,2,2,3,3,3,4,4,4]
	for fy in range(1,13):
		qq.insert(0,qq.pop())
		m = 1
		res[fy] = {}
		for i in range(12):
			q = qq[i]
#			print( fy,m,q ) #d
			res[fy][m] = q
			m += 1
#		if fy == 2: break
#		print( fy,qq )
	#
	import xz
	f = xz.notice
	xz.notice = False
	xz.obj2bin(res,N2QBIN)
	xz.notice = f
	return res

#


##############
### VEKTOR ###
##############

### INTMONAT VEKTOR ###
def nvec(ini,fin=0,interval=1):
	assert is_n(ini)
	if not fin == 0: assert is_n(fin)
	assert interval in [1,2,3,4,6]

	if fin == 0:
		fin = dy.today()
		fin = fin.year * 100 + fin.month
	initmonth = ini % 100
	while 1:
		initmonth += interval
#		print( initmonth ) #d
		if initmonth > 12:
			initmonth = initmonth - 12
			break
	#
	res = [ini]
	i = ini + 0
#	print( i ) #d
	while 1:
		i += interval
#		if i % 100 >= 13:
#			i -= interval
#			i -= 11
#			i += 100
		if i % 100 >= 13:
			i = i // 100
			i += 1
			i *= 100
			i += initmonth
		if i > fin:
			break
		res.append(i)
	return res

## Alias ##
imvec = nvec
intmonths = nvec

### QUARTAL VEKTOR ###
def qvec(ini,fin):
	assert is_q(ini)
	assert is_q(fin)
	res = []
	inij,iniq = ini.split('Q')
	finj,finq = fin.split('Q')
	inij = int(inij)
	iniq = int(iniq)
	finj = int(finj)
	finq = int(finq)

	### HAUPT ###
	q = '%dQ%d' % (inij,iniq)
	res.append(q)
	while 1:
		iniq += 1
		if iniq == 5:
			inij += 1
			iniq = 1
		#
		q = '%dQ%d' % (inij,iniq)
		res.append(q)
		#
		if inij == finj:
			if iniq == finq:
				break
	return res

#-------------------------------------------------

#############################
### MONAT zu QUARTAL DICT ###
#############################
def n2qdic(ini,fin,fy=12):
	ims = imvec(ini,fin)
	fys = [ n2q(x,fy) for x in ims ]
	res = {}
	for i,im in enumerate(ims):
		fy = fys[i]
		res[im] = fy
	return res

def n2ydic(ini,fin,fy=12):
	res = n2qdic(ini,fin,fy)
	for k in res.keys():
		w = res[k]
		assert w[-2] == 'Q'
		assert w[-1] in '1234'
		w = w[:-2]
		w = int(w)
		res[k] = w
	return res

#-------------------------------------------------

#

###########################
### INTMONAT zu QUARTAL ###
###########################
def n2q(x,fy=12,mode='EUR'):
	"""
	REF: Beispiel in "xt4finplus.tsv"
	---------------------------------
	Euro (like Oracle) :
		201705 -> FY17Q4
		201706 -> FY18Q1
	Non-Euro :
		201605 -> FY16Q4
		201706 -> FY17Q1
	ETC :
		Japan begins from April
		USA begins from October
		Europe begins from Jan
		https://ja.wikipedia.org/wiki/%E5%B9%B4%E5%BA%A6#.E5.B9.B4.E5.BA.A6.E3.81.AE.E4.B8.80.E8.A6.A7
		https://ja.wikipedia.org/wiki/%E4%BC%9A%E8%A8%88%E5%B9%B4%E5%BA%A6
	"""
	assert is_n(x)
	assert mode in ['EUR','JPN','USA']
	global N2QTABLE
	if N2QTABLE == {}:
		N2QTABLE = n2qtafel()
	j = x // 100
	m = x % 100
	q = N2QTABLE[fy][m]
	#
#	mode = 'USA' #d
#	mode = 'JPN' #d
#	mode = 'EUR' #d
	if mode == 'EUR':
		if fy == 12:
			qq = '%dQ%d' % (j,q)
		else:
			if m <= fy:
				qq = '%dQ%d' % (j,q)
			else:
				qq = '%dQ%d' % (j+1,q)
	elif mode == 'JPN':
		if m <= 3:
			qq = '%dQ%d' % (j-1,q)
		else:
			qq = '%dQ%d' % (j,q)
#	print( fy,x,qq ) #d
	return qq

#########################
### INTMONAT zu JAHRE ###
#########################
def n2y(x,fy=12):
	assert is_n(x)
	assert 1 <= fy <= 12
	#
	y = x // 100
	m = x % 100
	if fy == 12: return y
	y = n2q(x,fy)
	y = y[0:4]
	y = int(y)
	return y

#

####################
### QUARTAL zu X ###
####################
def q2d(w,fy=12):
	assert fy in range(1,13)
	if not is_q(w): return w
	j = int(w[0:4])
	m = int(w[-1])
	qm = m * 3 + fy
	qm = qm % 12
	if qm == 0: qm = 12
	t = calendar.monthrange(j,qm)[1]
	return dy(j,qm,t)

def q2n(w,fy=12):
	d = q2d(w,fy)
	im = d.year * 100 + d.month
	return im

def q2y(w,fy=12):
	d = q2d(w,fy)
	return d.year

#

####################
### X zu QUARTAL ###
####################
def d2q(x,fy):
	im = d2n(x)
	q = n2q(im,fy)
	return q

def s2q(x,fy):
	x = s2z(x)
	q = d2q(x,fy)
	return q

#-------------------------------------------------

###########
### Q+- ###
###########
def qplus(w):
	if not is_q(w): return w
	j,q = w.split('Q')
	j = int(j)
	q = int(q)
	if q == 4:
		j += 1
		q = 1
	else:
		q += 1
	w = '%dQ%d' % (j,q)
	return w

def qminus(w):
	if not is_q(w): return w
	j,q = w.split('Q')
	j = int(j)
	q = int(q)
	if q == 1:
		j -= 1
		q = 4
	else:
		q -= 1
	w = '%dQ%d' % (j,q)
	return w

def qdiff(w1,w2):
	if not is_q(w1): return (w1,w2)
	if not is_q(w2): return (w1,w2)
	j1,q1 = w1.split('Q')
	j2,q2 = w2.split('Q')
	j1 = int(j1)
	q1 = int(q1)
	j2 = int(j2)
	q2 = int(q2)
	#
	i1 = j1 * 100 + (q1-1) * 25
	i2 = j2 * 100 + (q2-1) * 25
	res = i1 - i2
	res = res // 25
	return res


#

##### DIREKT ###############
if __name__ == '__main__':
	x = 200112
	y = n2y(x)
	print( y )
