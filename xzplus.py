#!/usr/bin/python

### MODULES ###
import xt
import xz

def fxs():
	fx1 = lambda x,y: x/y # per capita
	fx2 = lambda x,y: x*y # multiple
	fx3 = lambda x,y: x*y/100 # x:val,y:pctg

	delta = lambda x1,x2: x2-x1

#

#####################
### TABLE for LOG ###
#####################
def tbl4log(txt,dic,gettable=False):
	assert( isinstance(dic, dict) )
	tbl = xz.txt2tbl(txt)
	header = xz.getheader(txt)
	#
	if not 'tag' in dic:
		dic['tag'] = xt.heute()
	#
	assert sorted(header) == sorted(list(dic.keys()))
	if tbl[-1][0] == str(dic['tag']):
		tbl.pop()
	res = [ dic[k] for k in header ]
	tbl.append(res)
	#
	xz.tbl2txt(tbl,txt)
	if gettable == True:
		return tbl
	else:
		tbl = xz.txt2ldic(txt)
		tbl = xz.bless(tbl)
		return tbl,header

#

########################
### LDIC zu ERFÜLLEN ###
########################
def dic2erfullen(dic,kopfer):
	for x in kopfer:
		if x in dic: continue
		dic[x] = ''
	return dic

########################
### LDIC zu ERFÜLLEN ###
########################
def ldic2erfullen(ldic,kopfer):
	res = []
	for dic in ldic:
		for k in kopfer:
			if not k in dic:
				dic[k] = ''
#		res.append(tmp)
#	return res

#

######################
### TEXT zu STRING ###
######################
def txt2str(txt):
	"""
	[xz.py]
	with open(txt, 'r',encoding='utf-8') as f: x = f.read()
	return x.replace("\r",'')
	"""
	### 
	try:
		fh = open(txt, 'r',encoding='sjis')
		res = fh.read()
		fh.close()
		return res
	except UnicodeDecodeError:
		pass

	fh = open(txt, 'r',encoding='utf-8',errors='replace')
	res = fh.read()
	fh.close()
	return res
