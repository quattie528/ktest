### MODULE ###
import re

###############
### COMMIFY ###
###############
def commify(v):
	w = str(v)
	if w == 'True':  return v
	if w == 'False': return v
	if w.isdigit == False:
		return v
	#
	minus = False
	if w[0] == '-':
		minus = True
		w = w[1:]
	#
	deci = ''
	if '.' in w:
		w = re.match('^(.+)\.(.+)$',w)
		deci = w.group(2)
		w = w.group(1)

	### MAIN ###
	v = list( str(w) )
	v.reverse()
	w = []
	for i,x in enumerate(v):
#	   print(i,x)
		w.append(x)
		if (i+1) % 3 == 0: w.append(',')

	### LAST ###
	w.reverse()
	v = "".join(w)
	v = re.sub('^,','',v)
	#
	if minus == True:
		v = '-' + v
	if len(deci) > 0:
		v = v + '.' + deci

	### RETURN ###
	return v

"""
def commify(amount):
	amount = list(str(amount))
	amount.reverse()
	cnt = 0
	res = []
	for x in amount:
		cnt += 1
		res.append(x)
		if cnt == 3:
			res.append(',')
			cnt = 0
	res.reverse()
	return "".join(res)
"""

"""
x = -12327287.54123123132312
x = commify(x)
print( x )
"""
