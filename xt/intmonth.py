#!/usr/bin/python

### MODULES ###
#from datetime import date as d
#from datetime import time as t
from datetime import date as dy # ein Alphabet ist gefehr
from datetime import time as tm # ein Alphabet ist gefehr
from datetime import datetime as dt
from datetime import timedelta as dl
import calendar

###############################################
### N = INTMONTH = INTEGER MONTH = INTMONAT ###
###############################################
def n2d(m,ende=True):
	assert is_n(m)
	j = m // 100
	m = m % 100
	if ende == True:
		t = calendar.monthrange(j,m)[1]
	elif ende == False:
		t = 1
	return dy(j,m,t)

def n2me(im):
	assert is_n(im)
	return n2d(im,True)

def s2n(x):
	assert( isinstance(x, str) )
	if re.search('[a-zA-Z]',x): return x

	x = re.sub(' \d\d:\d\d:\d\d$','',x)
	x = re.sub('-\d\d$','',x)
	x = x.replace('-','')
	x = int(x)
	is_n(x)

	return x

def d2n(x):
	assert( isinstance(x, dy) )
	return x.year * 100 + x.month

#-------------------------------------------------

###########
### N+- ###
###########
def nplus(x):
	rev = False
	if not is_n(x):
		if is_n(200000+x):
			rev = True
			x = 200000 + x
		else:
			return x
	x += 1
	if x % 100 == 13:
		x += 88
	assert is_n(x)
	if rev == True:
		x = x - 200000
	return x

def nminus(x):
	rev = False
	if not is_n(x):
		if is_n(200000+x):
			rev = True
			x = 200000 + x
		else:
			return x
	x -= 1
	if x % 100 == 0:
		x -= 88
	assert is_n(x)
	if rev == True:
		x = x - 200000
	return x

#

##################
### GESCHICHTE ###
##################

### MOVED from xd.py ###
"""
[Comment out @ 2018-10-28]
### INT MONTH ###
class intmonth(int):
	def __myfunc__(n):
		if n % 100 <= 12:
			return True
		else:
			return False

	def __new__(cls,n):
		if cls.__myfunc__(n) == False:
			raise ValueError('not intmonth')
		return super().__new__(cls,n)

	def __iadd__(my,n):
		n = my + n
		if n % 100 > 12:
			n = n + 88
		return intmonth(n)

	def __isub__(my,n):
		n = my - n
		if n % 100 > 12:
			n = n - 88
		elif n % 100 <= 0:
			n = n - 88
		return intmonth(n)
"""
