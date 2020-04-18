### MODULES ###
#from datetime import date as d
#from datetime import time as t
from datetime import date as dy # ein Alphabet ist gefehr
from datetime import time as tm # ein Alphabet ist gefehr
from datetime import datetime as dt
#from datetime import timedelta as dl

def heute(typ=True): # True:string, False:Date|Time
	x = dy.today()
	if typ == True:
		return x.strftime('%Y-%m-%d')
	elif typ == False:
		return x
	assert typ in [True,False]

def heuted():
	return dy.today()

def jetzt(typ=True):
	x = dt.now()
#	print( typ ) #d
	if typ == True:
		return x.strftime('%Y-%m-%d %H:%M:%S')
	elif typ == False:
		return x
	assert typ in [True,False]

def jetzt2(typ=True):
	x = dt.now()
	if typ == True:
		return x.strftime('%Y-%m-%d_%H%M%S')
	elif typ == False:
		return x
	assert typ in [True,False]

def jetztt():
	return dt.now()

def imheute():
	return s2n(heute())
