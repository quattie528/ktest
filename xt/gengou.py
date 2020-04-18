### MODULES ###
import re

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
		if x < dy(2019,5,1):
			g = 'H'
			y2 = 1988
		else:
			g = 'R'
			y2 = 2018
	elif y == 1926:
		if x < dy(1926,7,31):
			g = 'T'
			y2 = 1911
		else:
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
#	print( y,y2,y3 ) #d
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

def d2sg2(x):
	x = d2sg(x)
	x = x.replace('M','明治')
	x = x.replace('T','大正')
	x = x.replace('S','昭和')
	x = x.replace('H','平成')
	x = x.replace('R','令和')
	x = x.split('.')
	x = x[0] + '年' + x[1] + '月' + x[2] + '日'
	return x

#-------------------------------------------------
#-------------------------------------------------
#-------------------------------------------------

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
