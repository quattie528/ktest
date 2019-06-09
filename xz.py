#!/usr/bin/python

"""
[ACHTUNG!!!] Verwenden niemals meine eigenen externen Module
"""

### MODULES ###
import datetime as dt
import io
import os
#import csv
import pickle
import re
import sys
import time
#
import attrdict
import yaml
from loch import *   # Ausnahme für die Achtung
from datsun import * # Ausnahme für die Achtung
from xzplus import * # Ausnahme für die Achtung

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

##### GET KML HEADER ###
def getkmlheader(var):
	assert( isinstance(var, str) )
	lst = []
	ion = str2io(var)
	for x in ion:
		x = x.rstrip("\n")
		if re.match('^<(.+)>$',x):
			m = re.match('^<(.+)>$',x)
			lst.append( m.group(1) )
		elif re.match('^$',x):
			break
	lst = tuple(lst)
	ion.close
	return lst

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
		from collections import OrderedDict
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

### STRING to ATTR-DICT*ATTR-DICT ###
def str2aadic(var,key):
	import attrdict
	var = str2ddic(var,key)
	res = attrdict.AttrDict()
	for k,dic in var.items():
		res[k] = attrdict.AttrDict(dic)
	return res

#

### KML to LIST-DICT ###
def kml2ldicALL(var):
	kopfer = getkmlheader(var)

	### VARIABLES ###
	res = []
	dic = {}
	blobkey = 'abc'
	blobstr = ''
	#
	f_init = True
	f_ntag = False
	f_swmd = False
	f_blob = False

	### HAUPT ###
	if var.startswith("\n"):
		var = re.sub("^\n","",var)
	ion = str2io(var)
	for x in ion:
		if re.search('<!-.+->',x): continue
		x = x.rstrip("\n")

#d		print(x)
		## Kopfer ##
		if f_init == True:
			if x == '': f_init = False
			continue

		## Inhalt ##
		m = re.match('^<(.+?)>(.*)$',x) # 2016/03/05
		if m == None:
			k = ''
			v = ''
		else:
			k = m.group(1)
			v = m.group(2)
		#
		# flag
		f_ntag = False
		f_swmd = False
		m = re.match('^(.+)/$',k)
		if x == '': f_ntag = True
		if m: f_swmd = True
#		if f_ntag = True
		#
		# normal value
		if (not f_swmd) and (not f_blob):
			if not f_ntag:
				dic[k] = v
			else:
				for k in kopfer:
					if not k in dic:
						dic[k] = ''
				res.append(dic)
				dic = {}
			continue

		# blob value
		if f_swmd:
			k = m.group(1)
			blobkey = k
			f_blob = True
			continue
		if not k:
			blobstr += x
			blobstr += "\n"
			continue
		else:
			m = re.match('^/%s$'%blobkey,k)
			if m:
				f_blob = False
				blobstr = blobstr.rstrip("\n")
				dic[blobkey] = blobstr
				blobstr = ''

	### AUSGABE ###
	if debug == True:
		pprint.pprint( y )
	if not dic == {}: res.append(dic)
	return res

#

### KML to DICT-DICT ###
def kml2ddicALL(txt,key):
	res = {}
	ldic = kml2ldic(txt)
	for dic in ldic:
		res[ dic[key] ] = dic
	return res

##### TXT to ??? ###############

#### TXT to STRING ###
def txt2str(txt):
	with open(txt, 'r',encoding='utf-8') as f: x = f.read()
	return x.replace("\r",'')

### TXT to ETC ###
def txt2lis(txt): return str2lis(txt)
def txt2tup(txt): return str2tup(txt)
def txt2dic(txt,**opt): return str2dic(txt,**opt)
def txt2tbl(txt): return str2tbl(txt)
def txt2ldic(txt): return str2ldic(txt)
def txt2dlis(txt): return str2dlis(txt)
def txt2dlis2(txt): return str2dlis2(txt)
def txt2ddic(txt,key): return str2ddic(txt,key)
def txt2adic(txt): return str2adic(txt)
def txt2aadic(txt,key): return str2aadic(txt,key)
def kml2ldic(txt): return kml2ldicALL(txt)
def kml2ddic(txt,key): return kml2ddicALL(txt,key)

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

##### BIN to BIN ###############
def obj2bin(obj,bin):
	gh = open(bin,'wb')
	pickle.dump(obj, gh)
	gh.close()
	__tell_output(bin)

def bin2obj(bin):
#	print( bin ) #d
	gh = open(bin,'rb')
	obj = pickle.load(gh)
	gh.close()
	return obj

def binbin(f1,f2):
	if os.path.exists(f2):
		if os.path.getmtime(f1) < os.path.getmtime(f2):
			obj = bin2obj(f2)
			return obj
	obj = xz.txt2ldic(f1)
	obj2bin(obj,f2)
	return obj

def bin2erb(bin,etc):
	if os.path.exists(bin):
		try:
			return bin2obj(bin)
		except EOFError:
			return etc
	else:
		return etc

##### ??? to STD ###############

### VALUE for SHOW ###
def value4show(v):

	if ( isinstance(v, int) ):
		v = commify( v )
		return v
	elif ( isinstance(v, str) ):
		if v.isdigit():
#			print( type(v),v ) #d
			v = commify( v )
			return v
		else:
			return v
	else:
		return str( v )

### SHOW TABLE ###
def showtable(var,lens):
	res = ''
	for lis in var:
		i = 0
#		res = ''
		for x in lis:
			x = value4show(x)
			if re.match('^\-?[\d\.,%]+$',x):
				res += x.rjust(lens[i],' ')
			elif x == '-':
				res += '- '.rjust(lens[i],' ')
			else:
				res += x.ljust(lens[i],' ')
			res += ' | '
			i += 1
#		print( type(res) ) #d -> str
		res += "\n"
	print( res )
	return True
	#
	import tabulate
#	fmt = 'plain'
#	fmt = 'simple'
#	fmt = 'grid'
#	fmt = 'fancy_grid'
#	fmt = 'pipe'
	fmt = 'orgtbl' # basic
#	fmt = 'rst'
#	fmt = 'mediawiki'
#	fmt = 'html'
#	fmt = 'latex'
#	fmt = 'latex_booktabs'
	res = tabulate.tabulate(var, headers="firstrow",tablefmt=fmt)
	print( type(res) ) #d -> str
	print( res )

### SHOW (basic) ###
def show(var,header=[]):

	### MODUL ###
	import japonais

	### VARIABLE ###
	mode = ''
	zelle = {}

	### MODE ###
	if isinstance(var,dict):
		mode = 'dic'
	elif isinstance(var,list):
		if var == []:
			print( '* Achtung, Leer Liste!' )
			print( var[0] ) # ich mochte ein Felher passen
#		print( len(var[0]),type(var[0]),var[0] )
		if len(var) == 1:
			if isinstance(var[0],list):
				mode = 'tbl'
			elif isinstance(var[0],dict):
				mode = 'ldic'
		elif isinstance(var[1],list):
			mode = 'tbl'
			if isinstance(var[0],dict): # 2017-10-15
				zelle = var.pop(0)
				assert( isinstance(var[-1], list) )
		elif isinstance(var[0],dict):
			mode = 'ldic'
		else:
			assert not mode == '', 'Kein Mode'

	### DICT ###
	if mode == 'dic':
		v1 = 0
		v2 = 0
		for x in var.keys():
			i = japonais.len( value4show(x) )
			if v1 < i: v1 = i
		for x in var.values():
			i = japonais.len( value4show(x) )
			if v2 < i: v2 = i

		fmt = '%s' + str(v1) + ' | %s' + str(v2)
		kys = var.keys()
		kys = list(kys)
		kys.sort()
		for k in kys:
			w = var[k]
			x = k.rjust(v1,' ')
			x += ' | '
			x += str(w).rjust(v2,' ')
			print(x)

	### TABLE ###
	elif mode == 'tbl':
		lens = []
		xs = len( var )
		ys = len( var[0] )
		for j in range( ys ):
			lens.append(0)
			for i in range( xs ):
				q = japonais.len( value4show( var[i][j] ) )
				if lens[j] < q: lens[j] = q
		showtable(var,lens)

	### LIST-DICT ###
	elif mode == 'ldic':
		res = []
		lens = []
		for x in header: res.append(x)
		res = [res]
		#
		for dic in var:
			lis = []
			for x in header: lis.append( value4show( dic[x] ) )
			res.append( lis )
		#
		var = res
		xs = len( var )
		ys = len( var[0] )
		for j in range( ys ):
			lens.append(0)
			for i in range( xs ):
				q = japonais.len( value4show( var[i][j] ) )
				if lens[j] < q: lens[j] = q
		#
		var.pop(0)
		showtable([header],lens)
		i = 0
		for x in lens:
			i += x
			i += 3
		i -= 1
		print('-'*i)
		showtable(var,lens)
		print('-'*i)
		showtable([header],lens)

	## Gegenreaktion (contrecoup/backlash) ###
	if not zelle == {}:
		var.insert(0,zelle)

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

####################
### YAML zu CONF ###
####################
def yml2cnf(txt):
	x = txt2str(txt)
	x = x.replace("\t",'  ')
	x = x.replace('<UR>',urpfad)
	x = x.replace(urpfad+'/',urpfad)

	x = str2io(x)
	dic = yaml.load(x,Loader=yaml.BaseLoader)
	dic = attrdict.AttrDict(dic)
	return dic

#

##### DIREKT ###############
if __name__=='__main__':
	import pprint
	txt = ''
	d = yml2cnf(txt)
	pprint.pprint( d )

#add flush(), from the lecture yesterday @ 2017-12-04
