import re
import xz

############
### TRIM ###
############
def trim(txt):
	"""
	1st line : begin using
	2nd line : end using
	3rd line : exception
	blank line : begin reading the data
	"""
	mode = False
	des = ''
	aux = ''
	res = []
	exs = ['<URL>']
	lis = xz.txt2lis(txt)
	#
	des = lis.pop(0)
	aux = lis.pop(0)
	while 1:
		if lis[0] == '': break
		exs.append( lis.pop(0) )
	#
	for x in lis:
		if mode == True:
			if re.match(aux,x):
				mode = False
			res.append(x)
		elif mode == False:
			if re.match(des,x):
				mode = True
				res.append(x)
			for rg in exs:
				if re.match(rg,x):
					res.append(x)
					break
	res = "\n".join(res)
	return res

##### DIREKT ###############
if __name__=='__main__':
	pass
