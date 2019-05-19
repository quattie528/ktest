#!/usr/bin/python

### MODULES ###
import re
import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import xi
import xz
from datsun import *

### VARIABLES ###
xz.notice = True
#xz.notice = False
farben = ['red','yellow','green','blue','orange','#000000']
#plt.figure(figsize=(20,10))

#

def bless(dlis):
	for k,lis in dlis.items():
		lis = [ xz.subbless(x) for x in lis ]
		dlis[k] = lis
	return dlis

##################
### TXT to PIE ###
##################
def txt2pie(txt,ausgabe='a.png'):
	#Sample als 'res/plt_pie'
	#pl2.py
	dic = xz.txt2dlis(txt)
	dic = bless(dic)
	#
	labels = dic['labels']
	colors = dic['colors']
	explodes = dic['explodes']
	values = dic['values']
#	explodes = [ float(x) for x in dic['explodes'] ]
#	values = [ float(x) for x in dic['values'] ]
	#
	print( values )
	exit()
	plt.pie(
		values,
		explode=explodes,
		labels=labels,
		colors=colors,
		autopct='%1.1f%%',
		shadow=True,
		startangle=90
	)
	plt.axis('equal')
	#
	plt.savefig(ausgabe)
	xz.__tell_output(ausgabe)

#

########################
### TXT to BAR STACK ###
########################
def txt2bars(txt,ausgabe='a.png'):
	#Sample als 'res/plt_barstack'
	#pl3.py

	### VARIABLES 1 ###
	dic = xz.txt2dlis(txt)
	dic = bless(dic)
	cols = dic['[cols]'].copy()
	del dic['[cols]']
	kys = xz.txt2tbl(txt)
	kys = [ lis[0] for lis in kys ]
	del kys[0]

	### VARIABLES 2 ###
	n = 0
	bottoms = []
	for d,lis in dic.items():
		n = len(lis)
		bottoms = [ 0 for x in range(n) ]
		break
	ind = np.arange(n) # the x locations for the groups
	width = 0.35 # the width of the bars: can also be len(x) sequence

	### HAUPT ###
	p = []
	for i,k in enumerate(kys):
		bar = plt.bar(
			ind,
			dic[k],
			width,
			color=farben[i],
			bottom=bottoms
		)
		p.append(bar)
		#
		for j,x in enumerate(dic[k]): bottoms[j] += x

	title = 'Scores by group and gender\nfdaadfasfass'
	xlabel = 'Groups'
	ylabel = 'Scores'
	plt.title(title)
	plt.suptitle('Scores by group and genderG')
	#a.png
	plt.xlabel(xlabel)
	plt.ylabel(ylabel)
	plt.xticks(ind + width/2., cols)
	plt.yticks(np.arange(0, 81, 10))
#	plt.legend((p1[0], p2[0]), ('Men', 'Women'))

	### AUSGABE ###
#	plt.show()
	plt.savefig(ausgabe)
	xz.__tell_output(ausgabe)

#

#############################
### TXT to BAR STACK TWIN ###
#############################
def txt2bars2(txt1,txt2,ausgabe='a.png'):

	#Sample als 'res/plt_barstack'
	#pl3.py

	### VARIABLES 1 ###
	dic1 = xz.txt2dlis(txt1)
	dic1 = bless(dic1)
	dic2 = xz.txt2dlis(txt2)
	dic2 = bless(dic2)
	#
	assert dic1['[cols]'] == dic2['[cols]']
	cols = dic1['[cols]'].copy()
	del dic1['[cols]']
	del dic2['[cols]']
	#
	kys = xz.txt2tbl(txt1)
	kys = [ lis[0] for lis in kys ]
	del kys[0]

	### VARIABLES 2 ###
	n = 0
	bottoms1 = []
	bottoms2 = []
	for d,lis in dic1.items():
		n = len(lis)
		bottoms1 = [ 0 for x in range(n) ]
		bottoms2 = [ 0 for x in range(n) ]
		break
	ind = np.arange(n) # the x locations for the groups
	width = 0.35 # the width of the bars: can also be len(x) sequence
	#

	### HAUPT ###
	fig, ax = plt.subplots(figsize=(30, 20))
	p1 = []
	p2 = []
	for i,k in enumerate(kys):
		bar1 = ax.bar(ind, dic1[k], width,
			color=farben[i],
			bottom=bottoms1
		)
		bar2 = ax.bar(ind+width, dic2[k], width,
			color=farben[i],
			bottom=bottoms2
		)
		p1.append(bar1)
		p2.append(bar2)
		#
		for j,x in enumerate(dic1[k]): bottoms1[j] += x
		for j,x in enumerate(dic2[k]): bottoms2[j] += x

	# add some text for labels, title and axes ticks
	ax.set_ylabel('Scores',fontsize=48)
	ax.set_title('Scores by group and gender',fontsize=52)
	ax.set_xticks(ind + width)
	ax.set_xticklabels(cols,fontsize=36)
#	ax.legend((rects1[0], rects2[0]), ('Men', 'Women'))

	### AUSGABE ###
#	plt.show()
	plt.savefig(ausgabe)
	xz.__tell_output(ausgabe)

	import xi
	x = xi.negate(ausgabe)
	x.save('d.png')

#

####################
### TEXT zu PLOT ###
####################
def txt2plt(txt,ausgabe='b.png'):

	### VARIABLES 1 ###
	df = xz.txt2tbl(txt)
	idx = df[0][0]
	df = pd.read_csv(txt,sep="\t",index_col=idx).transpose()

	### HAUPT ###
	p = plt.figure()
	p = plt.figure(figsize=(19.2,10.8))
	p = df.plot(
		kind = 'line',
		title = 'GEP',
#		subplots = True,
#		secondary_y = True,
		figsize = (19.2,10.8),
	)
	fig = p.get_figure()

	### AUSGABE ###
	fig.savefig(ausgabe)
	plt.close()
	#
	fig = xi.negate(ausgabe)
	fig.save(ausgabe)

def txt2plt2(txt,ausgabe='b.png'):

	### VARIABLES 1 ###
	dfbar = xz.txt2tbl(txt)
#	dflin = xz.txt2tbl('c.tsv')
	idx1 = dfbar[0][0]
#	idx2 = dflin[0][0]
	dfbar = pd.read_csv(txt,sep="\t",index_col=idx1).transpose()
#	dflin = pd.read_csv('c.tsv',sep="\t",index_col=idx2).transpose()

	### HAUPT ###
	pbar = dfbar.plot(
		kind='bar',
		figsize=(19.2,10.8),
		stacked=True,
	)
#	plin = dflin.plot(
#		kind='line',
#		figsize=(19.2,10.8),
#		ax=pbar,
#		secondary_y = True,
#	)
	fig = pbar.get_figure()

	### AUSGABE ###
	fig.savefig(ausgabe)
	plt.close()
	#
	fig = xi.negate(ausgabe)
	fig.save(ausgabe)

#

####################
### TEXT zu PLOT ###
####################
def txt2kinds(txt):
	#Sample als 'res/plt_barstack'
	#pl3.py

	### VARIABLES 1 ###
	df = xz.txt2tbl(txt)
	idx = df[0][0]
	df = pd.read_csv(txt,sep="\t",index_col=idx).transpose()
	df.info()
	datei = 'b.png'

	typen = ['line','bar','barh','hist','box','kde','density','area']
	typen += ['pie','scatter','hexbin']
	for x in typen:
		p = plt.figure()
		p = plt.figure(figsize=(19.2,10.8))
		try:
			p = df.plot(kind=x,figsize=(19.2,10.8))
		except ImportError:
			x = 'KEIN MODULE als %s' % x
			print( x )
			plt.close()
			continue
		except ValueError:
			x = 'KAPUT MODULE als %s' % x
			print( x )
			plt.close()
			continue
		fig = p.get_figure()
		#
		datei = 'c_%s.png' % x
		fig.savefig(datei)
		plt.close()
		#
		fig = xi.negate(datei)
		fig.save(datei)

##### DIREKT ###############
if __name__=='__main__':
	mode = 2
	if mode == 1:
		txt2pie('ad/plt_pie.tsv')
	elif mode == 2:
		txt2bars('ad/plt_barstack.tsv')
	elif mode == 3:
		txt2bars2('ad/plt_barstack.tsv','ad/plt_barstack2.tsv','e.png')
	elif mode == 4:
#		txt2plt('a.tsv')
		txt2plt2('a.tsv','c.png')
#x.png
#a.png
