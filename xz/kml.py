from .xzbase import *

#

######################
### GET KML HEADER ###
######################
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

#

########################
### KML to LIST-DICT ###
########################
def kml2ldic(var):
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

########################
### KML to DICT-DICT ###
########################
def kml2ddic(txt,key):
	res = {}
	ldic = kml2ldic(txt)
	for dic in ldic:
		res[ dic[key] ] = dic
	return res

#kml2ldicALL = kml2ldic
#kml2ddicALL = kml2ddic
