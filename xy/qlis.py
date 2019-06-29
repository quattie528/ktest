### NEVER USE MY OWN MODULE ###

#################
### TRANSPOSE ###
#################
def transpose(var):
	return list(map(list, zip(*var)))

#

###############
### FLATTEN ###
###############
from itertools import chain
def flatten(lis):
	if not isinstance(lis, list):
		lis = [lis]
	lis = list(chain.from_iterable(lis))
	return lis

from functools import reduce
def flatten(lis):
	if not isinstance(lis, list):
		lis = [lis]
	lis = reduce(lambda a, b: a + b, lis)
	return lis
