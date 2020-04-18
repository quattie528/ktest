from datsun import *
import xz

#

######################
### VALUE for SHOW ###
######################
def value4show(v):

	if ( isinstance(v, int) ):
		if   v is True:  return 'True'
		elif v is False: return 'False'
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

#

##################
### SHOW TABLE ###
##################
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

####################
### SHOW (basic) ###
####################
def show(var,header=[]):

	### MODUL ###
	import japonais
	import pandas

	### VARIABLE ###
	mode = ''
	zelle = {}

	### MODE ###
	if isinstance(var,dict):
		mode = 'dic'
	elif isinstance(var,pandas.core.frame.DataFrame):
		mode = 'pds'
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

	### PANDAS ###
	elif mode == 'pds':
		for x in var.columns:
			typ = var[x].dtype
			if typ == 'float64':
				var[x] = var[x].astype('int64')
		tmp = labomi+'x.tsv'
		var.to_csv(tmp,sep="\t")
		tbl = xz.txt2tbl(tmp)
		show(tbl)

	## Gegenreaktion (contrecoup/backlash) ###
	if not zelle == {}:
		var.insert(0,zelle)

#

#####################
### SHOW (reborn) ###
#####################
def show2(res,fmt='psql'):
	import tabulate
	"""
	https://pypi.org/project/tabulate/
	plain/simple/github/grid/fancy_grid/pipe/
	orgtbl/jira/presto/psql/rst/mediawiki/moinmoin/
	youtrack/html/
	latex/latex_raw/latex_booktabs/textile/

	orgtbl is the basic
	"""

	for i in range(len(res)):
		for j in range(len(res[0])):
			x = res[i][j]
			x = xz.bless(x)
			x = value4show(x)
			res[i][j] = x

	fmt = 'github'
	fmt = 'psql' # Das ist das hochst @ 2020-02-09
	res = tabulate.tabulate(res,headers="firstrow",tablefmt=fmt)
#	print( type(res) ) #d -> str

	if fmt == 'psql':
		res = res.split("\n")
		res.append(res[1])
		res.append(res[0])
		res = "\n".join(res)
	print( res )
