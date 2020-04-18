#!/usr/bin/python

### MODULES ###
#from datetime import date as d
#from datetime import time as t
from datetime import date as dy # ein Alphabet ist gefehr
from datetime import time as tm # ein Alphabet ist gefehr
from datetime import datetime as dt
from datetime import timedelta as dl
import time
import re
import os
import calendar
#
#from .finplus import *

#print(d.today())
#print(dt.today())
#print(dt.now())
M2STABLE = {}

#

############
### SEIN ###
############
def is_n(m):
	try:
		assert( isinstance(m, int) )
		assert m in range(190001,210000)
		assert m % 100 in range(1,12+1)
	except AssertionError:
		return False
	return True

def is_q(w):
	try:
		assert( isinstance(w, str) )
		assert len(w) == 6
		j = int(w[0:4])
		q = int(w[-1])
		assert j in range(1900,2100)
		assert q in range(1,5)
	except AssertionError:
		return False
	return True

def is_me(x): # Monatsende
	if isinstance(x, str):
		x = s2z(x)
	assert( isinstance(x, dy) )
	y = calendar.monthrange(x.year,x.month)[1]
	y = dy(x.year,x.month,y)
#	print( x ) #d
#	print( y ) #d
	if x == y:
		return True
	else:
		return False

#-------------------------------------------------

##### From STRING to XXX ###
def s2z(x,zeichnis=''):
#	assert( str, type(x) )

	### DELTA ###
	d4dl = re.match('^(\d+)D',x)
	if d4dl:
		d4dl = d4dl.group(1)
		d4dl = int(d4dl)

	# ex. 1950/09/09
	if re.match('^\d{4}/\d{2}/\d{2}$',x):
		x = dt.strptime(x, '%Y/%m/%d')
		if zeichnis == '' or zeichnis == 'd':
			return dy(x.year,x.month,x.day)
	# ex. 1955-03-07
	elif re.match('^\d{4}-\d{2}-\d{2}$',x):
		x = dt.strptime(x, '%Y-%m-%d')
		if zeichnis == '' or zeichnis == 'd':
			return dy(x.year,x.month,x.day)
	# ex. 18:39
	elif re.match('^\d{2}:\d{2}$',x):
		x = dt.strptime(x, '%H:%M')
		if zeichnis == '' or zeichnis == 't':
			return tm(x.hour,x.minute,0)
	# ex. 18:10:40
	elif re.match('^\d{2}:\d{2}:\d{2}$',x):
		x = dt.strptime(x, '%H:%M:%S')
		if zeichnis == '' or zeichnis == 't':
			return tm(x.hour,x.minute,x.second)
	# ex. 18:10.40
	elif re.match('^\d{2}:\d{2}\.\d+$',x):
		x = dt.strptime(x, '%M:%S.%f')
		return tm(0,x.minute,x.second,x.microsecond)
	# ex. 1983-01-22 18:40:15
	elif re.match('^\d{4}/\d{2}/\d{2} \d{2}:\d{2}:\d{2}$',x):
		x = dt.strptime(x, '%Y-%m-%d %H:%M:%S')
		if zeichnis == '' or zeichnis == 'p':
			return dt(x.year,x.month,x.day,x.hour,x.minute,x.second)
	# ex. 1989-11-07 18:40:15
	elif re.match('^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}$',x):
		x = dt.strptime(x, '%Y-%m-%d %H:%M:%S')
		if zeichnis == '' or zeichnis == 'p':
			return dt(x.year,x.month,x.day,x.hour,x.minute,x.second)

	### 2017-09-16 ###
	# ex. 19800528
	elif re.match('^\d{4}\d{2}\d{2}$',x):
		x = dt.strptime(x, '%Y%m%d')
		if zeichnis == '' or zeichnis == 'd':
			return dy(x.year,x.month,x.day)
	elif re.match('^\d{2}\d{2}\d{2}$',x):
		if int(x[0:2]) >= 80:
			w = '19'
		else:
			w = '20'
		x = dt.strptime(w+x, '%Y%m%d')
		if zeichnis == '' or zeichnis == 'd':
			return dy(x.year,x.month,x.day)
	# ex. 0909
	elif re.match('^[01]\d[0-3]\d$',x):
		x = dt.strptime(x, '%m%d')
		if zeichnis == '' or zeichnis == 'd':
			return dy(dy.today().year,x.month,x.day)

	### 2018-11-04 ###
	elif re.match('^\d+D \d{1,2}:\d{1,2}:\d{1,2}$',x):
		x = dt.strptime(x, '%dD %H:%M:%S')
		x = dl(days=d4dl,hours=x.hour,minutes=x.minute,seconds=x.second)
		return x
	#
	elif re.match('^\d+D \d{1,2}:\d{1,2}$',x):
		x = dt.strptime(x, '%dD %H:%M')
		x = dl(days=d4dl,hours=x.hour,minutes=x.minute)
		return x

	return x

def s2d(x):
	return s2z(x,'d')

def t2k(x):
	return dl(hours=x.hour,minutes=x.minute)

#

##### From DATETIME to XXX ###
def p2d(x):
	return dy(x.year,x.month,x.day)

def p2t(x):
	return tm(x.hour,x.minute,x.second)

def p2q(x):
	if x.minute in [0,15,30,45]: return x
	min = x.minute
	q = min // 15
	r = min % 15
	if r < 8:
		min = q * 15 + 0
	else:
		min = q * 15 + 15
	diff = min - x.minute
	y = x + dl(minutes=diff)
	return y

##### From UNIXTIME to XXX ###############
def u2p(x):
#	if not isinstance(x,int):
#		raise TypeError('THIS IS IT: '+x)
	x = dt.fromtimestamp(x)
	x = dt(x.year,x.month,x.day,x.hour,x.minute,x.second)
	return x

def u2d(x):
	x = u2p(x)
	x = dy(x.year,x.month,x.day)
	return x

def u2t(x):
	x = u2p(x)
	x = tm(x.hour,x.minute,x.second)
	return x

##### From XXX to UNIXTIME ###############
def p2u(x):
	x = x.timetuple()
	x = time.mktime(x)
	x = int(x)
	return x

### From XXX to STRING ###
def z2s(x):
	if isinstance(x,int):
		x = u2p(x)
		x = x.strftime('%Y-%m-%d %H:%M:%S')
	elif isinstance(x,dt):
		x = x.strftime('%Y-%m-%d %H:%M:%S')
	elif isinstance(x,d):
		x = x.strftime('%Y-%m-%d')
	elif isinstance(x,t):
		x = x.strftime('%H:%M:%S')
	return x

#

def k2s(x,sym='hhmmss'):
	assert( isinstance(x, dl) )
	ms = x.microseconds
	n = x.seconds
	if sym == 'hhmmss':
		h,n = divmod( n,3600 )
		m,s = divmod( n,60 )
		x = '%02d:%02d:%02d' % (h,m,s)
	elif sym == 'yymmdd':
		d = x.days
		j,n = divmod( d,365 )
		m,t = divmod( n,30 )
		x = '%02dY-%02dM-%02dD' % (j,m,t)
	else:
#		x = '%02d:%02d:%02d.%05d' % (h,m,s,ms)
#		x = '%02d:%02d.%05d' % (m,s,ms)
		x = '%02d:%02d.%03d' % (m,s,ms)
	return x

#################################################

def sec2time(x):
	h = x // 3600
	x = x - h * 3600
	m = x // 60
	s = m % 60
	x = '%dh:%dm:%s' % (h,m,s)
	return x

#

#########################
### MONAT zu SPRACHEN ###
#########################
def m2stafel():

	tbl = """
	ENG	Jan	Feb	Mar	Apr	May	Jun	Jul	Aug	Sep	Oct	Nov	Dec
	"""
	#
	res = {}
	tbl = tbl.strip()
	tbl = tbl.split("\n")
	tbl = [ x.split("\t") for x in tbl ]
	#
	for lis in tbl:
		while 1:
			if lis[0] == '':
				lis.pop(0)
			else:
				break
		k = lis.pop(0)
		res[k] = lis
	#
	global M2STABLE
	M2STABLE = res.copy()

def m2s(x,sp='ENG'):
	if not isinstance(x, int): return x
	y = x % 100
	if not y in range(1,13): return x
	#
	global M2STABLE
	if M2STABLE == {}: m2stafel()
	#
	return M2STABLE[sp][y-1]

def s2m(x,sp='ENG'):
	if not isinstance(x, str): return x
	global M2STABLE
	if M2STABLE == {}: m2stafel()
	for i,monat in enumerate(M2STABLE[sp]):
		if monat == x:
			return i + 1
	return x

#

######################
### TIME PLUS TIME ###
######################
def tplus(t1,t2):
	assert( isinstance(t1, tm) )
	assert( isinstance(t2, tm) )

	diff = dl(
		hours=t2.hour,
		minutes=t2.minute,
		seconds=t2.second,
		microseconds=t2.microsecond
	)

	z = dt.combine(dy.today(), t1)
	z += diff
	return z.time()

def dateiheute(w):
	import os
	if os.path.exists(w):
		t = os.path.getmtime(w)
		t = u2p(t)
		t = str(dy(t.year,t.month,t.day))
		if t == heute():
			return True
	return False

#

##############
### WOCHEN ###
##############
def d2w(x): # 2018-05-20
	if isinstance(x, str):
		x = s2d(x)
	y = x.isocalendar() # ISOyear, ISOweeknumber, ISOweekday
	wochennummer = y[1]
	wochentag = y[2] - 1# Wochentag beginnt aus Montag(1), Sontag ist 7
	x = x - dl(days=wochentag)
	#
	res = x.strftime( '%4d-%02d-%02d-w' % (x.year,x.month,x.day) )
	res += str( wochennummer )
	return res

#

def d2a(x,lang='ENG'):
	w = x.weekday()
	if lang == 'DEU':
		wday = ('Mo', 'Di', 'Mi', 'Do', 'Fr', 'Sa', 'So')
	else:
		wday = ('Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun')
	w = wday[w]
	return w

#

def k2t(delta):
	x = delta
	u = x.seconds // 3600
	m = ( x.seconds % 3600 ) // 60
	x = tm(u,m)
	return x

#

#####################
### DATE in EXCEL ###
#####################
def xldate_to_date(xldate):
	temp = datetime.date(1900, 1, 1)
	delta = datetime.timedelta(days=xldate-2)
	return temp+delta

def xldate_to_datetime(xldate):
	temp = datetime.datetime(1900, 1, 1)
	delta = datetime.timedelta(days=xldate-2)
	return temp+delta

############################
### ÄLTESTE oder NEUESTE ###
############################
def aelteste_und_neueste(lis):
	assert( isinstance(lis, list) )
	lis = [ s2d(x) for x in lis ]
#	print( lis ) #d
	lis.sort()
	return lis

def aelteste(lis): # = älteste
	x = aelteste_und_neueste(lis)[0]
	x = str(x)
	return x

def neueste(lis):
	x = aelteste_und_neueste(lis)[-1]
	x = str(x)
	return x

#

##### DIREKT ###############
if __name__ == '__main__':
	x = 1
	mode = 13
	if mode == 1:
#		x = time.clock()
		x = 1462017536 # 2016-04-30 20:58:56
		#   149487390430
		x = u2p(x)
		print( x )
	elif mode == 2:
		x = '1970-01-01 09:00:17'
#		x = dt(1970,1,1,9,0,17)
#		x = int(time.mktime(x.timetuple()))
	elif mode == 3:
		for n in [330962,279458,610420]:
			print( sec2time(n) )
	elif mode == 4:
		x = '1970-01-01 09:00:17'
		x = s2n(x)
	elif mode == 5:
		for x in range(1000000):
#			x = intmonth(201801) # 3.05000 sec
			x = 201801 # 0.191127 sec
			x -= 3
	elif mode == 6:
		x = imheute()
		print( x )
	elif mode == 7:
		x = '0505'
		y = s2z(x)
		print( repr(y) )
	elif mode == 8:
		x = '12:12.123415'
		y = s2z(x)
		z = s2z(x)
		w = tplus(y,z)
		print( w )
	elif mode == 9:
		x = '会計年度(平成26年3月31日)/会計年度(平成26年4月30日)'
		print( sj2n(x) )
		x = '会計年度(平成26年3月31日)'
		print( sj2n(x) )
		x = '会計年度(2017年3月31日)'
		print( sj2d(x) )
	elif mode == 10:
		x = 201201
		for i in range(20):
			x = nplus(x)
			print( x )
		print( '%'*40 ) #d
		for i in range(20):
			x = nminus(x)
			print( x )
	elif mode == 11: # 2018-02-18
		q = '2012Q1'
		for i in range(10):
			q = qplus(q)
			print( q )
		print( '%'*40 ) #d
		for i in range(10):
			q = qminus(q)
			print( q )
	elif mode == 12: # 2018-02-18
		q1 = '2012Q4'
		q2 = '2013Q2'
		q = qdiff(q1,q2)
		print( q )
	elif mode == 13: # 2018-05-20
		d = '2018-05-20'
		e = d2w(d)
		print( e )
		print( f )
	elif mode == 14: # 2018-08-18
		lis = ['2017-08-05','2018-09-16','2015-08-17','2019-08-08']
		print( aelteste(lis) )
		print( neueste(lis) )
	import kbench
	kbench.jetzt()
