import itertools
from .xzbase import *

#

########################
### LISTE zu PRODUKT ###
########################
def lis2prd(lis1,lis2):
	res = itertools.product(lis1,lis2)
	res = list(res)
	return res

def txt2sieb2lis(txt,sieb):
	ion = str2io(txt)
	lis = []
	for i,x in enumerate(ion):
		if sieb in x:
			x = x.replace(sieb,'')
			x = x.strip()
			lis.append(x)
	return lis
