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
	v = list( str(w) )
	v.reverse()
	#
	w = []
	for i,x in enumerate(v):
#	   print(i,x)
		w.append(x)
		if (i+1) % 3 == 0: w.append(',')
	w.reverse()
	v = "".join(w)
	v = v.replace('-,','-')
	v = v.replace(',.','.')
	v = re.sub('^,','',v)
	return v
