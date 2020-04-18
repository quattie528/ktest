
#

#######################
### LDIC zu FILTERN ###
#######################
def ldic2filter(ldic,kopfer):
	res = []
	for dic in ldic:
		lis = []
		for k in kopfer:
			lis.append( dic[k] )
		res.append(dic)
	return res

#

#######################
### DIC zu ERFÜLLEN ###
#######################
def dic2fill(dic,kopfer):
	for x in kopfer:
		if x in dic: continue
		dic[x] = ''
	if '' in dic: dic.pop('')
	return dic
#
def ldic2fill(ldic,kopfer):
	for dic in ldic:
		dic = dic2fill(dic,kopfer)
	return ldic
#
dic2erfull = dic2fill
ldic2erfullen = ldic2fill


#######################
### RENAME KEY NAME ###
#######################
def rekey4dic(dic,keys):
	res = {}
	for k1,w in dic.items():
		try:
			k2 = keys[k1]
			res[k2] = w
		except KeyError:
			res[k1] = w
	return res
#
def rekey4ldic(ldic,keys):
	res = []
	for dic in ldic:
		dic = rekey4dic(dic,keys)
		res.append(dic)
	return res
#
def rekey(obj,keys):
	if isinstance(obj, dict):
		return rekey4dic(obj,keys)
	elif isinstance(obj, list):
		return rekey4ldic(obj,keys)
	assert isinstance(obj, dict)
