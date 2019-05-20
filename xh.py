#!/usr/bin/python

### MODULES ###
#import os
#import pprint
#
#import attrdict
#
#from datsun import *
import xz
#import kbench
#
#1:battery,2:pip,3:mygen,4:myopus

### VARIABLES ###
debug = True
debug = False


#

#####################
### TAFEL zu HTML ###
#####################
def tbl2html(tbl,kopfer=False,bilan=True):
	assert( isinstance(tbl, list) )
	assert( isinstance(tbl[0], list) )
	res = []
	for lis in tbl:
		w = '</td><td>'.join(lis)
		w = '<tr><td>%s</td></tr>' % w
		res.append(w)
	#
	if kopfer == True:
		res[0] = res[0].replace('td>','th>')
	res.insert(0,th)
	#
	wert = '<table class="tableau_bilan">'
	res.insert(0,wert)
	wert = '</table>'
	res.append(wert)
	#
	res = "\n".join(res)
	return res

#

##### DIREKT ###############
if __name__=='__main__':
	txt = 'b.tsv'
	tbl = xz.txt2tbl(txt)
	html = tbl2html(tbl)
	print( html )
	kbench.jetzt()
