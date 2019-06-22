#!/usr/bin/python

"""
[ACHTUNG!!!] Verwenden niemals meine eigenen externen Module
"""

### MODULES ###
import datetime as dt
import io
import os
#import csv
import re
import sys
import time
#
import attrdict
from collections import OrderedDict
import yaml
from loch import *   # Ausnahme für die Achtung
from datsun import * # Ausnahme für die Achtung
from .xzplus import * # Ausnahme für die Achtung

#

### VARIABLES ###
notice = True
binary = True
binary = False # 2016-12-18

##### VALUE ###############
debug = True
debug = False
if debug == True:
	import pprint

#str int float datetime date time
#list dict

#import pdb
#import pdb; pdb.set_trace

#

#############
### BLESS ###
#############
def subbless(v):

	## str ##
	if not isinstance(v, str):
		v = str(v)
	v = v.rstrip()
	v = v.lstrip()

#	if v == '': return '' # 2016-12-17

	## int ##
	if re.match('^[△\-]?[\d,]+$',v):
		if v == ',': return v
		if v == '△': return v
		v = v.replace('△','-')
		v = v.replace(',','')
		return int(v)

	## float ##
	elif re.match('^[△\-]?[\d,]+\.[\d]+$',v):
		v = v.replace('△','-')
		v = v.replace(',','')
		return float(v)

	## date ##
	elif re.match('^\d{4}-\d{2}-\d{2}$',v):
		if v[-2:] == '00': return v
		v = dt.datetime.strptime(v,"%Y-%m-%d")
		return dt.date(v.year, v.month, v.day)
	elif re.match('^\d{4}/\d{2}/\d{2}$',v):
		v = dt.datetime.strptime(v,"%Y/%m/%d")
		return dt.date(v.year, v.month, v.day)

	## time ##
	elif re.match('^\d{2}:\d{2}:\d{2}$',v):
		v = dt.datetime.strptime(v,"%H:%M:%S")
		return dt.time(v.hour, v.minute, v.second)

	## datetime ##
	elif re.match('^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}$',v):
		return dt.datetime.strptime(v,"%Y-%m-%d %H:%M:%S")
	elif re.match('^\d{4}/\d{2}/\d{2} \d{2}:\d{2}:\d{2}$',v):
		return dt.datetime.strptime(v,"%Y/%m/%d %H:%M:%S")

	## str ##
	else:
		return v

def bless(v):
	f = False
	if isinstance(v, list): f = True
	if isinstance(v, dict): f = True
	if f == False: return subbless(v)
	#
	if isinstance(v, list):
		res = []
		if not isinstance(v[0], list):
			if not isinstance(v[0], dict):
				res = [ subbless(x) for x in v ]
				return res
		if isinstance(v[0], list):
			for x in v:
				subs = []
				for y in x:
					subs.append( subbless(y) )
				res.append(subs)
		elif isinstance(v[0], dict):
			for x in v:
				subs = {}
				for k,y in x.items():
					subs[k] = subbless(y)
				res.append(subs)
	elif isinstance(v, dict):
		res = {}
		for k,y in v.items():
			k = subbless(k)
			y = subbless(y)
			res[k] = y
	return res

def bless4dlis(dlis,hyphen2zero=False):
	# hyphen2zero, for adil/z7png.py @ 2018-01-03
	for k,lis in dlis.items():
		lis = [ subbless(x) for x in lis ]
		#
		# begin hyphen2zero, for adil/z7png.py @ 2018-01-03
		if hyphen2zero == True:
			tmp = []
			for x in lis:
				if x == '-':
					tmp.append(0)
				else:
					tmp.append(x)
			lis = tmp
		#
		dlis[k] = lis
	return dlis

def strall(v):
	if isinstance(v, list):
		return [ str(x) for x in v ]
	elif isinstance(v, dict):
		res = {}
		for k,x in v.items(): res[ str(k) ] = str(x)
		return res
	else:
		return str(v)

def pp(v):
	if isinstance(v, list):
		if not isinstance(v[0], list):
			for x in v: print(x,type(x))
		elif isinstance(v[0], list):
			for x in v:
				for y in x: print(y,type(y))
				print('-'*20)
	else:
		print(v,type(v))

### STRING to IO ###
def str2io(var):
	ion = False
	if len(var) < 1000 and os.path.isfile(var):
		ion = open(var, 'r',encoding='utf-8')
	else:
		if re.match(".*\n",var): # \t is not necessary for kml # 2016-03-23
			ion = io.StringIO(var)
	if ion == False:
		msg = 'Neither STR with line nor FILE'
		raise FileNotFoundError(msg) # for ArgumentError
		raise ValueError(msg) # for ArgumentError
	return ion

### FUNCTION for LISTS ###
def fx4lst(fx,*tbl):
	res = []
	if len(tbl) == 1:
		return [ fx(x) for x in tbl[0] ]
	tbl = transpose(tbl)
	if len(tbl[0]) == 2:
		assert len(x[0]) == len(x[1])
		return [ fx(x[0],x[1]) for x in tbl ]
	elif len(tbl[0]) == 3:
		assert len(x[0]) == len(x[1])
		assert len(x[0]) == len(x[2])
		return [ fx(x[0],x[1],x[2]) for x in tbl ]
	elif len(tbl[0]) == 4:
		assert len(x[0]) == len(x[1])
		assert len(x[0]) == len(x[2])
		assert len(x[0]) == len(x[3])
		return [ fx(x[0],x[1],x[2],x[3]) for x in tbl ]
	else:
		raise ValueError

def __tell_output(ex): # gigi
	global notice
	if notice == False:
		return None
	sys.stdout.write('\tAusgabe als "%s"\n' % ex)

def __bin_output(ex,feile):
	global notice, binary
	if binary == False: return True
	m = re.search('(.+)\.',feile)
	ausgabe = m.group(1) + '.bin'
	notice = False
	obj2bin(ex,ausgabe)
	notice = True

##### HEADER ###############

### GET HEADER ###
def getheader(var):
	assert( isinstance(var, str) )
	lis = []
	ion = str2io(var)
	for x in ion:
		if re.match('^\t*#+',x): continue
		if re.match('^\t*!',x): continue
		x = x.rstrip("\n")
		lis = x.split("\t")
		lis = tuple(lis)
		break
	ion.close
	return lis

#

### HEADER CONVERSION ###
def headerconvert4dic(dic,headerdic,key):
	assert key == '1u3a1duj'
	assert sorted(dic.keys()) == sorted(headerdic.keys())
	#
	res = {}
	for k,v in headerdic.items():
		dic[v] = dic[k]
		del(dic[k])
	return res

def headerconvert(var,headerdic):
	msg = 'This function is for dict or list-dict'
	assert isinstance(headerdic, dict), msg
	key = '1u3a1duj'
	#
	## Dict
	if isinstance(var, dict):
		return headerconvert4dic(dic,headerdic,key)
	## List-Dict
	elif isinstance(var, list):
		assert isinstance(var[0], dict)
		res = []
		for dic in var:
			res.append( headerconvert4dic(dic,headerdic,key) )
		return res

##### STRING to ??? ###############
def str2txt(x,ex): # gigi
	gh = open(ex,'w',encoding='utf-8')
	gh.write(x)
	gh.flush()
	gh.close
	__tell_output(ex)
	__bin_output(x,ex)

### STRING to LIST ###
def str2lis(v):
	ion = str2io(v)
	lis = []
	for i,x in enumerate(ion):
		if x == "\n" and i == 0: continue
		if re.match('^\t*#+',x): continue
		if re.match('^\t*!',x): continue
		if re.match('^<!-+ .+ -+>$',x): continue # 2017-09-16
		x = x.rstrip("\n") # = chomp
		x = x.rstrip("\r") # = chomp
		x = x.rstrip("\r\n") # = chomp
		lis.append(x)
	ion.close
	return lis

def str2tup(v):
	return tuple(txt2lis(v))

### STRING to DICTIONARY ###
def str2dic(v,**opt):
	if 'sep' in opt:
		sep = opt['sep']
	else:
		sep = "\t"
	if 'rev' in opt:
		rev = opt['rev']
		assert rev == True
	else:
		rev = False
	if 'ord' in opt:
		ord = opt['ord']
		assert ord == True
	else:
		ord = False

	ion = str2io(v)
	if ord == True:
		dic = OrderedDict()
	else:
		dic = {}
	for i,x in enumerate(ion):
		if x == "\n" and i == 0: continue
		if re.match('^\t*#+',x): continue
		if re.match('^\t*!',x): continue
		x = x.rstrip("\n") # = chomp
		x = x.split(sep)
		if rev == True:
			dic[ x[1] ] = x[0]
		else:
			dic[ x[0] ] = x[1]
	ion.close
	return dic

### STRING to TABLE ###
def str2tbl(v):
	ion = str2io(v)
	res = []
	for i,x in enumerate(ion):
		if x == "\n" and i == 0: continue
		if re.match('^\t*#+',x): continue
		if re.match('^\t*!',x): continue

		## Tafel mit Metadaten am 2017-10-15 ##
		if re.match('^\t*%(.+) :: (.*)',x):
			if res == []:
				res.insert(0,{})
			elif not isinstance(res[0], dict):
				res.insert(0,{})
			m = re.match('^\t*%(.+) :: (.+)',x)
			k = m.group(1).lstrip().rstrip()
			w = m.group(2).lstrip().rstrip()
			res[0][k] = w
			continue

		## Normale Werte ##
		x = x.rstrip("\n") # = chomp
		x = x.split("\t")
		res.append( x )
	ion.close
	return res

### STRING to LIST-DICT ###
def str2ldic(v):

	### VARIABLES ###
	kopfer = getheader(v)
	ion = str2io(v)
	res = []
	ini = False

	### HAUPT ###
	for i,x in enumerate(ion):

		## Ini ##
		if x == "\n" and i == 0: continue
		if re.match('^\t*#+',x): continue
		if re.match('^\t*!',x): continue
		if ini == False:
			ini = True
			continue

		## Datum ##
		x = x.rstrip("\n") # = chomp
		x = x.split("\t")
		#
		i = 0
		dic = {}
		for y in kopfer:
			try:
				dic[y] = x[i]
			except IndexError:
				dic[y] = ''
			i += 1
		res.append( dic )
	ion.close
	return res

### STRING to DICT-LIST ###
def str2dlis(var,ind=0):
	tbl = str2tbl(var)
	res = {}
	for lis in tbl:
		x = lis.pop(0)
		res[x] = lis
	return res

def str2dlis2(var,ind=0):
	lis = str2lis(var)
	res = {}
	k = ''
	tmp = []
	for x in lis:
		if not x[0] == "\t":
			if not k == '':
				res[k] = tmp
				tmp = []
			k = x
		else:
			tmp.append( x[1:] )
	res[k] = tmp
	return res

### STRING to DICT-DICT ###
def str2ddic(var,key):
	res = str2ldic(var)
	res = ldic2ddic(res,key)
	return res

#

### STRING to ATTR-DICT ###
def str2adic(var):
	var = str2dic(var)
	return attrdict.AttrDict(var)

### STRING to ORDERED-DICT ###
def str2odic(var):
	var = str2dic(var)
	return OrderedDict(var)

### STRING to ATTR-DICT*ATTR-DICT ###
def str2aadic(var,key):
	import attrdict
	var = str2ddic(var,key)
	res = attrdict.AttrDict()
	for k,dic in var.items():
		res[k] = attrdict.AttrDict(dic)
	return res

#

##### TXT to ??? ###############

#### TXT to STRING ###
def txt2str(txt):
	with open(txt, 'r',encoding='utf-8') as f: x = f.read()
	return x.replace("\r",'')

### TXT to ETC ###
txt2lis = str2lis
txt2tup = str2tup
txt2dic = str2dic
txt2tbl = str2tbl
txt2ldic = str2ldic
txt2dlis = str2dlis
txt2dlis2 = str2dlis2
txt2ddic = str2ddic
txt2adic = str2adic
txt2aadic = str2aadic
txt2odic = str2odic

##### LIST to ??? ###############

def lis2str(lis):
	x = ''
	for y in lis: x += str(y) + "\n"
	return x

def lis2txt(lis,ex):
	x = lis2str(lis)
	with open(ex, 'w',encoding='utf-8') as f:
		f.write(x)
		f.flush()
	__tell_output(ex)
	__bin_output(lis,ex)

def tbl2str(tbl):
	res = ''
	for lis in tbl:
		lis = [ str(y) for y in lis ]
		lis = "\t".join(lis)
		lis += "\n"
		res += lis
	return res

##### DICT to ??? ###############

#

##### TABLE to ??? ###############

### TABLE to LIST-DICT ###
def tbl2ldic(tbl):
	assert( isinstance(tbl, list) )
	assert( isinstance(tbl[0], list) )

	tbl = bless(tbl)

	kopfer = []
	res = tbl.pop(0)
	for x in res:
		if isinstance(x, str):
			x = x.replace("\n",' ')
		kopfer.append(x)

	res = []
	for lis in tbl:
		dic = {}
#		print( kopfer )
#		print( len(kopfer) )
		for i,x in enumerate(kopfer):
			dic[x] = lis[i]
		res.append(dic)
	return res

### IST-DICT to TABLE ###
def ldic2tbl(ldic,kopfer=[],schaukopfer=True):
	if kopfer == []:
		kopfer = list( ldic[0].keys() )
	tbl = []
	for dic in ldic:
		lis = [ dic[k] for k in kopfer ]
		tbl.append(lis)
	if schaukopfer == True:
		tbl.insert(0,kopfer)
	return tbl

def tbl2ddic(tbl,key):
	ldic = tbl2ldic(tbl)
	return ldic2ddic(ldic,key)

def tbl2dlis(tbl):
	res = {}
	for lis in tbl:
		k = lis.pop(0)
		res[k] = lis
	return res

##### LIST-DICT to ??? ###############

### LIST-DICT to LIST ###
def ldic2lis(ldic,k):
	res = []
	for dic in ldic:
		res.append(dic[k])
	return res

### LIST-DICT to DICT ###
def ldic2dic(ldic,k,v):
	res = {}
	for dic in ldic:
		c = dic[k]
		res[c] = dic[v]
	return res

### LIST-DICT to DICT-DICT ###
def ldic2ddic(ldic,k,**opt):
	res = {}
	for dic in ldic: res[ dic[k] ] = dic
	if opt.get('delkey') == True:
		for key,dic in res.items():
			del dic[k]
	return res

#

##### ??? to STD ###############

### DICT to TXT ###
def dic2txt(dic,ex):
	gh = open(ex, 'w',encoding='utf-8')
	kys = dic.keys()
	kys = list(kys)
	kys.sort()
	for k in kys:
		w = dic[k]
		x = ( str(k), "\t", str(w), "\n" )
		x = ''.join(x)
		gh.write( x )
		gh.flush()
	gh.close
	__tell_output(ex)
	__bin_output(dic,ex)

### TABLE to TXT ###
def tbl2txt(tbl,ex):
	gh = open(ex, 'w',encoding='utf-8')
	for lis in tbl:
		arr = []
		for x in lis:
			if isinstance(x, str):
				arr.append( x )
			else:
				arr.append( str(x) )
		gh.write( "\t".join( arr ) + "\n" )
		gh.flush()
	gh.close
	__tell_output(ex) # gigi
	__bin_output(tbl,ex)

### LIST-DICT to TXT ###
def ldic2txt(ldic,ex,header):
	gh = open(ex, 'w',encoding='utf-8')
	arr = []
	for x in header: arr.append( str(x) )
	gh.write( "\t".join( arr ) + "\n" )
	gh.flush()
	#
	for dic in ldic:
		arr = []
#		print( dic['itm_top_事件番号'] ) #d
		for x in header:
			arr.append( str(dic[x]) )
		gh.write( "\t".join( arr ) + "\n" )
		gh.flush()
	gh.close
	__tell_output(ex)
	__bin_output(ldic,ex)

##### ??? to KML ###############

### LIST-DICT to KML ###
def ldic2kml(ldic,ex='',header=[]):

	## Variables ##
	if header == []: header = list( ldic[0].keys() )
	dach = '*'*49
	dach = "<!--%s-->\n" % dach
	#
	res = [ "<%s>" % x for x in header ]
	res = "\n".join(res)
	res += "\n\n"
	#
	till = len(ldic) - 1
	for index, dic in enumerate(ldic):
		res += dach
		for x in header:
			if x in dic:
				y = str( dic[x] )
			else:
				y = ''
			if not re.search( "\n", y ):
				res += ( '<'+x+'>'+y )
				res += ("\n")
			else:
#				res += ('<!--'+'*'*40+'-->'+"\n")
				res += ( '<'+x+'/>' )
				res += ("\n")
				res += ( y.rstrip() )
				res += ("\n")
				res += ( '</'+x+'>' )
				res += ("\n")
		if index < till:
			res += ("\n")

	## Ausgabe ##
	if not ex == '':
		str2txt(res,ex)
	return res

#


##### ??? to STD ###############

#

##### ETC #####

### LOOKUP ###
def lookup(des,aux,ex='a.txt'):
	lis = txt2lis(des) #
	dic = txt2dic(aux) # mediator
	gh = open(ex, 'w',encoding='utf-8')
	for x in lis:
		if x in dic:
			gh.write( dic[x] )
			gh.write("\n")
			gh.flush()
		else:
			gh.write(x)
			gh.write("\n")
			gh.flush()
	gh.close
	__tell_output(ex)
#	__bin_output(ex,x)

#

##############################
### Xs and Ys to DICT-DICT ###
##############################
def xys2ddic(xs,ys,default=0):
	assert( isinstance(xs, list) )
	assert( isinstance(ys, list) )

	res = {}
	for x in xs:
		res[x] = {}
		for y in ys:
			res[x][y] = default
	return res

#

##################
### CSV to TSV ###
##################
def csv2tbl(datei,ausgabe='a.tsv'):
	import csv
	import codecs
	import chardet
	res = []
	koda = 'utf-8'
	#
	fh = open(datei,'rb')
	x = fh.read()
	tmp = chardet.detect(x)
	if tmp['encoding'] == 'SHIFT_JIS':
		koda = 'sjis'
	elif tmp['encoding'] == 'ISO-8859-1': # opn.py
		koda = 'latin1'
	#
	with codecs.open(datei,encoding=koda) as csvfile:
		spamreader = csv.reader(csvfile)
		for i, reihe in enumerate(spamreader):
			if reihe == []:
				res.append(reihe)
				continue
			if not reihe[0] == '': # 2018-05-27
				if reihe[0][0] == '\ufeff': #== BOM
					reihe[0] = reihe[0].replace('\ufeff','')# DEL
			res.append(reihe)
#	xz.tbl2txt(res,ausgabe)
	return res

def tbl2csv(tbl,ausgabe):
	import csv
	gh = open(ausgabe, 'w',encoding='utf-8')
	gh2 = csv.writer(gh, lineterminator='\n')
	for lis in tbl:
		gh2.writerow(lis)
#		try: #d
#			print( lis ) #d
#		except UnicodeEncodeError: #d
#			pass #d
	gh.close()

#

##########################
### DICT-DICT to TABLE ###
##########################
def ddic2tbl(ddic,xs,ys,default=None):
	res = []
	xheader = xs.copy()
	yheader = ys.copy()
	#
	if default != None:
		for x in xs:
			if not x in ddic:
				ddic[x] = {}
			for y in ys:
				if not y in ddic[x]:
					ddic[x][y] = default
	#
	for x in xheader:
		lis = []
		for y in yheader:
#			print( x,y )
			lis.append( ddic[x][y] )
		res.append(lis)
	#
	res.insert(0,yheader)
	for i,lis in  enumerate(res):
		if i == 0:
			lis.insert(0,'')
		else:
			lis.insert(0,xheader[i-1])
	return res

#

def tbl4next(tbl,ex):
	tsv = ''
	bin = ''
	if ex[-4:] == '.tsv':
		tsv = ex
		bin = ex.replace('.tsv','.bin')
	elif ex[-4:] == '.bin':
		bin = ex
		tsv = ex.replace('.bin','.tsv')
	#
	obj2bin(tbl,bin)
	tbl2txt(tbl,tsv)

def lis2tbl(lis,tier=8):
	assert( isinstance(lis, list) )
	assert( not isinstance(lis[0], list) )
	res = []
	tmp = []
	i = 0
	while 1:
		try:
			tmp = []
			for j in range(tier):
				tmp.append(lis[i])
				i += 1
			res.append(tmp)
		except IndexError:
			break
	#
	if res == []: return [tmp]
	#
	i = len(res[0]) - len(tmp)
	if i > 0:
		for j in range(i): tmp.append('')
	res.append(tmp)
	return res

def bin2tbl(ex):
	tsv = ''
	bin = ''
	if ex[-4:] == '.tsv':
		tsv = ex
		bin = ex.replace('.tsv','.bin')
	elif ex[-4:] == '.bin':
		bin = ex
		tsv = ex.replace('.bin','.tsv')
	#
	try:
		res = bin2obj(bin)
	except FileNotFoundError:
		res = txt2tbl(tsv)
		obj2bin(res,bin)
	return res

#

##################
### TXT zu ZIP ###
##################
def txt2zip(zip,*dateien):
	import zipfile as zp
	#
	res = []
	for x in dateien:
		if isinstance(x, list):
			res += x
		elif isinstance(x, str):
			res.append(x)
	zh = zp.ZipFile(zip, "w", zp.ZIP_DEFLATED)
	for x in res:
		zh.write(x)
		zh.flush()
	zh.close()

def zip2lis(zip,datei):
	import zipfile as zp
	zh = zp.ZipFile(zip)
	roh = zh.read(datei)
	#
	res = []
	ion = io.BytesIO(roh)
	for x in ion:
		try: # TOR-01.03
			y = x.decode('sjis')
		except UnicodeDecodeError:
			y = x.decode('shift_jisx0213') # 2017-12-28
			# 1758 / 株式会社髙松コンストラクショングループ
			# '髙' ist ein besonder Charakter
		y = y.rstrip()
		res.append(y)
	ion.close()
	zh.close()
	#
	return res

def zip2txt(zip,datei):
	lis = zip2lis(zip,datei)
	res = ''
	for x in lis:
		res += x
	return res

#

###############################
### TXT zu TXTs (viel TXTs) ###
###############################
def txt2txts(txt,ln=10000):
	fh = open(txt, 'r',encoding='utf-8')
	ext = '.' + re.sub('.+\.','',txt)
	schreiber = lambda datei:open(datei, 'w',encoding='utf-8')

	n = 1
	i = 0
	ausgabe = txt.replace(ext,'') + '#%02d' % n + ext
	gh = schreiber(ausgabe)
	for x in fh:
		i += 1
		gh.write(x)
		if i == ln:
			i = 0
			n += 1
			gh.close()
			xz.__tell_output(ausgabe)
			#
			ausgabe = txt.replace(ext,'') + '#%02d' % n + ext
			gh = schreiber(ausgabe)
	gh.close()
	xz.__tell_output(ausgabe)

#

##########
### IS ###
##########
def istbl(tbl):
	if not isinstance(tbl, list): return False
	for lis in tbl:
		if not isinstance(lis, list):
			return False
	return True

def isldic(ldic):
	if not isinstance(ldic, list): return False
	for lis in ldic:
		if not isinstance(lis, dict):
			return False
	return True

#

##########################
### DICT-LIST zu TAFEL ###
##########################
def dlis2tbl(dlis,kopfer):
	menge = -1
	for lis in dlis:
		if menge == -1:
			menge = len(lis)
			continue
		assert len(lis) == menge

	res = []
	for k in kopfer:
		lis = [ x for x in dlis[k] ]
		lis.insert(0,k)
		res.append(lis)

	res = transpose(res)
	return res

#

##### DIREKT ###############
if __name__=='__main__':
	import pprint
	txt = ''
	d = yml2cnf(txt)
	pprint.pprint( d )

#add flush(), from the lecture yesterday @ 2017-12-04
