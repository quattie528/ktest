#!/usr/bin/python

#############################
### ERKLÄRUNG IN ENGLISCH ###
#############################
"""
[ERKLÄRUNG]
Hier, ich nutze Englisch für Symbols als {d:date, t.time, y:year}

[ACHTUNG!!!]
Verwenden niemals meine eigenen externen Module
"""

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

#print(d.today())
#print(dt.today())
#print(dt.now())

N2QTABLE = {}
N2QBIN = os.path.dirname(__file__) + '/'
N2QBIN += 'conf/im2q.bin'
M2STABLE = {}

"""
obj
	timedelta
	tzinfo
	time
	date
		datetime

[ABBREVIATION]
s : string
d : date
t : time
p : datetime
z : any
-
u : unixtime
x : exceltime
-
y : year
m : month
d : day
h : hour
m : month
s : second
-
a : weekday (Mon-Sun)
b : month in language (Jan-Dec)
- MY DEFINITION
q : quarter
n : month in 6 digits (ex. 198005, 201610)
e : date in 4 digits (ex. 0122, 1107, 0528)
k : delta
w : week
----------
g  : gengou (明治|大正|昭和|平成)
sc : string in dot -> 1980.05.28
sh : string in hyphen -> 1980-05-28
sl : string in slash -> 1980/05/28
sj : string in Japanese Gengou ->
sg : string in Japanese alphabetical Gengou -> S55.5.28
sf : string in full mode -> 1980-05-27 23:57:33
"""

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

### STRING(JPN) zu XXX ###
def g2y(x):
	if x == '明治':
		return 1867
	elif x == '大正':
		return 1911
	elif x == '昭和':
		return 1925
	elif x == '平成':
		return 1988
	elif x == '令和':
		return 2018
	elif x == '民國':
		return 1911
	elif x == 'M':
		return 1867
	elif x == 'T':
		return 1911
	elif x == 'S':
		return 1925
	elif x == 'H':
		return 1988
	elif x == 'R':
		return 2018
	else:
		return x

def d2sg(x):
	g = ''
	y2 = 0
	y = x.year
	m = x.month
	d = x.day
	#
	## Transitional ##
	if y == 2019:
		g = 'H'
		y2 = 1988
		if x >= dy(2019,5,1):
			g = 'R'
			y2 = 2018
	elif y == 1926:
		g = 'T'
		y2 = 1911
		if x >= dy(1926,7,30):
			g = 'S'
			y2 = 1925
	#
	# Simple
	else:
		if   y > 2018: g = 'R'; y2 = 2018
		elif y > 1988: g = 'H'; y2 = 1988
		elif y > 1925: g = 'S'; y2 = 1925
		elif y > 1911: g = 'T'; y2 = 1911
		elif y > 1868: g = 'M'; y2 = 1868
	y3 = y - y2
	z = '%s%d.%d.%d' % (g,y3,m,d)
	return z

def sj2d(x):
	gengou = '(明治|大正|昭和|平成|令和|民國)'
	jmt = '\s*(\d{1,3})年\s*(\d{1,3})月\s*(\d{1,3})日'
	m = re.findall(gengou+jmt,x)
	if len(m) == 0:
		gengou = ''
		jmt = '()(\d{4})年(\d{1,3})月(\d{1,3})日'
		m = re.findall(gengou+jmt,x)
		if len(m) == 0:
			return x
	res = []
	for n in m:
		if gengou == '':
			jr = int(n[1])
		else:
			jr = g2y(n[0])
			jr = jr + int(n[1])
		mn = int(n[2])
		tg = int(n[3])
		tg = dy(jr,mn,tg)
		res.append(tg)
	if len(res) == 1:
		return res[0]
	else:
		return res

def sj2n(x):
	res = sj2d(x)
	if not isinstance(res, list):
		res = [res]
	res = [ d2n(x) for x in res ]
	if len(res) == 1:
		return res[0]
	else:
		return res

def is_sg(x):
	if re.match('^[MTSHR]\d{1,2}\.1?\d\.[1-3]?\d$',x):
		return True
	else:
		return False

def sg2d(x):
	if not is_sg(x): return x
	w = re.findall('^([MTSHR])(\d{1,2})\.(1?\d)\.([1-3]?\d)$',x)
	g = g2y(w[0][0])
	j = int(w[0][1])
	m = int(w[0][2])
	t = int(w[0][3])
	w = dy(g+j,m,t)
	return w

def sg2s(x):
	if not is_sg(x): return x
	return str(sg2d(x))

##### From DATETIME to XXX ###
def p2d(x):
	return dy(x.year,x.month,x.day)

def p2t(x):
	return tm(x.hour,x.minute,x.second)

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

def is_me(x): # Monatsende
	if isinstance(x, str):
		x = s2z(x)
	assert( isinstance(x, dy) )
	y = calendar.monthrange(x.year,x.month)[1]
	y = dy(x.year,x.month,y)
	print( x )
	print( y )
	if x == y:
		return True
	else:
		return False

"""
def n2q(m):
	is_n(m)

	y = m // 100
	m = m % 100
	q = (m-1) // 3
	q += 1

	q = '%dQ%d' % (y,q)
	return q
"""

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

### IM++ ###
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

### IM-- ###
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

###########################
### INTMONAT zu QUARTEL ###
###########################
"""
def n2qtafel():

	import xz
#	if os.path.exists(N2QBIN): return True

	conf1 = []
	for x in range(1,13):
		lis = []
		for i in range(4):
			lis.append(x)
			x += 3
			if x > 12: x -= 12
		conf1.append(lis)
	xz.show(conf1)
	xz.tbl2txt(conf1,'fy.tsv') #d

	res = {}
	for i,lis in enumerate(conf1):
		m = lis[0]
		dic = {}
		for j,x in enumerate(lis):
			if j == 0:
				y = 4
			else:
				y = j
			dic[x] = y
		res[m] = dic
#d	pprint.pprint( res ) #d
	xz.obj2bin(res,N2QBIN)
	return True
"""

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

def n2q(x,fy=12,mode='EUR'):
	"""
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
		"""
REAL	1	2	3	4	5	6	7	8	9	10	11	12
201701	201704	201704	201604	201703	201703	201703	201702	201702	201702	201701	201701	201701
201702	201701	201704	201604	201704	201703	201703	201703	201702	201702	201702	201701	201701
201703	201701	201801	201604	201704	201704	201703	201703	201703	201702	201702	201702	201701
201704	201801	201801	201701	201704	201704	201704	201703	201703	201703	201702	201702	201702
201705	201802	201801	201701	201801	201704	201704	201704	201703	201703	201703	201702	201702
201706	201802	201802	201701	201801	201801	201704	201704	201704	201703	201703	201703	201702
201707	201802	201802	201702	201801	201801	201801	201704	201704	201704	201703	201703	201703
201708	201803	201802	201702	201802	201801	201801	201801	201704	201704	201704	201703	201703
201709	201803	201803	201702	201802	201802	201801	201801	201801	201704	201704	201704	201703
201710	201803	201803	201703	201802	201802	201802	201801	201801	201801	201704	201704	201704
201711	201804	201803	201703	201803	201802	201802	201802	201801	201801	201801	201704	201704
201712	201804	201804	201703	201803	201803	201802	201802	201802	201801	201801	201801	201704
		"""
	elif mode == 'JPN':
		if m <= 3:
			qq = '%dQ%d' % (j-1,q)
		else:
			qq = '%dQ%d' % (j,q)
#	print( fy,x,qq ) #d
	return qq

def d2q(x,fy):
	im = d2n(x)
	q = n2q(im,fy)
	return q

def s2q(x,fy):
	x = s2z(x)
	q = d2q(x,fy)
	return q

###############
### QUARTEL ###
###############
def q2y(w):
	if not is_q(w): return w
	return int(w[0:4])

import pprint
def q2d(w,fy=12):
	assert fy in range(1,13)
	if not is_q(w): return w
	j = q2y(w)
	m = int(w[-1])
	qm = m * 3 + fy
	qm = qm % 12
	if qm == 0: qm = 12
	t = calendar.monthrange(j,qm)[1]
	return dy(j,qm,t)

### Q++ ###
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

#################################################

def is_n(m):
	try:
		assert( isinstance(m, int) )
		assert m in range(194501,210000)
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
		assert j in range(1980,2100)
		assert q in range(1,5)
	except AssertionError:
		return False
	return True

def heute(typ=True): # True:string, False:Date|Time
	x = dy.today()
	if typ == True:
		return x.strftime('%Y-%m-%d')
	elif typ == False:
		return x
	assert typ in [True,False]

def heuteD():
	return heute(False)

def jetzt(typ=True):
	x = dt.now()
	print( typ )
	if typ == True:
		return x.strftime('%Y-%m-%d %H:%M:%S')
	elif typ == False:
		return x
	assert typ in [True,False]

def jetzt2(typ=True):
	x = dt.now()
	if typ == True:
		return x.strftime('%Y-%m-%d_%H%M%S')
	elif typ == False:
		return x
	assert typ in [True,False]

def imheute():
	return s2n(heute())

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
	try:
		fh = open('conf/xt_m2s.tsv')
#		fh = open('conf/xt_m2s.tsv',encoding='utf-8')
	except FileNotFoundError:
		fh = open('conf/xt_m2s.tsv')
	tbl = fh.read()
	fh.close()
	#
	res = {}
	tbl = tbl.strip()
	tbl = tbl.split("\n")
	tbl = [ x.split("\t") for x in tbl ]
	#
	for lis in tbl:
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

##########################
### ZEIT in JAPANISHCE ###
##########################
regex4gengou = """
	^([MTSHR])(\d{1,2})
	[\./-]
	([01]?\d)
	[\./-]
	(30|31|[012]?\d)
"""
##### ONE POINT MEMO
#"30|31|[12]?\d" instead of "[12]?\d|30|31"
#	otherwise it first matches with [12]?\d,
#	and 30 and 31 never match
#	result will be from S55.3.31 to 1980-03-03
regex4gengou = regex4gengou.replace("\t",'')
regex4gengou = regex4gengou.replace("\n",'')

class jtime():
	def to_day(y):
		#
		if not isinstance(y, str): return y
		#
		x = y.replace('明治','M')
		x = x.replace('大正','T')
		x = x.replace('昭和','S')
		x = x.replace('平成','H')
		x = x.replace('令和','R')
		x = x.replace('年','.')
		x = x.replace('月','.')
		x = x.replace('日','')
		#
		w = ''
		mt = re.match(regex4gengou,x)
		if mt:
			if mt.group(1) == 'M': w = 1867
			elif mt.group(1) == 'T': w = 1911
			elif mt.group(1) == 'S': w = 1925
			elif mt.group(1) == 'H': w = 1988
			y = int( mt.group(2) ) + w
			m = int( mt.group(3) )
			d = int( mt.group(4) )
			try:
				return datetime.date(y,m,d)
			except ValueError:
				print( 'Fehler entdicket', y,m,d )
				raise ValueError
		else:
			return x

	def to_jday(x):
		assert isinstance(x, datetime.date)
		assert x.year > 1867
		if x.year > 1867 and x.year < 1912:
			y = 'M' + str( x.year - 1867 )
		elif x.year >= 1911 and x.year < 1926:
			y = 'T' + str( x.year - 1911 )
		elif x.year >= 1925 and x.year < 1989:
			y = 'S' + str( x.year - 1925 )
		elif x.year >= 1988:
			y = 'H' + str( x.year - 1988 )
		x = y + ( '.%s.%s' % (x.month,x.day) )
		return x

#

##############
### VECTOR ###
##############
def imvec(ini,fin=0,interval=1):
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
def nvec(ini,fin=0,interval=1): return imvec(ini,fin,interval)
def intmonths(ini,fin=0,interval=1): return imvec(ini,fin,interval)

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
