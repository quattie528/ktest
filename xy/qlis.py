### MODULE ###
from itertools import chain

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
def flatten(lis):
	if not isinstance(lis, list):
		lis = [lis]
	lis = list(chain.from_iterable(lis))
	return lis
