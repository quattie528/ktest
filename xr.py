#!/usr/bin/python

### ZWECK : BEFÄHIGEN RE.PY ###

### MODULES ###
#import os
import re
#import pprint
from datsun import *
#import xz
#import kbench

### VARIABLES ###
debug = True

def str3rgs(x,rgs1,rgs2):
	assert( isinstance(x, str) )
	assert( isinstance(rgs1, tuple) )
	assert( isinstance(rgs2, tuple) )
	#
	for i,rg1 in enumerate(rgs1):
		rg2 = rgs2[i]
		x = re.sub(rg1,rg2,x)
	return x

def str8rgs(x,rgs):
	assert( isinstance(x, str) )
	assert( isinstance(rgs, tuple) )
	#
	for rg in rgs:
		y = re.findall(rg,x)
		if not y == []:
			return y[0]
	return None
