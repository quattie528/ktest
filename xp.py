#!/usr/bin/python

### MODULES ###
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import xz
import os
from datsun import *

### VARIABLES ###
debug = True

##########
### IO ###
##########
def txt2pd(txt):
	fh = open(txt, 'r')
	idx = fh.readline().split("\t")[0]
	chk = fh.readline().split("\t")[0]
	fh.close()
	#
#	df = pd.read_csv(txt,sep="\t")
	df = pd.read_csv(txt,sep="\t",index_col=idx)
	return df

def pd2txt(df,ausgabe):
	df.to_csv(ausgabe,sep="\t")
	ausgabe = ausgabe.replace('.tsv','.bin')
	xz.obj2bin(df,ausgabe)

def dffig2mono(fig,ausgabe='a.png'):
	import xi
	tmp = 'b.png'
	if ausgabe == 'b.png':
		tmp = 'a.png'
	fig.savefig(tmp)
	fig = xi.negate(tmp)
	fig.save(ausgabe)
	xz.__tell_output(ausgabe)

###################
### PIVOT TABLE ###
###################
def xsumme(df,dic):
	assert isinstance(df, pd.core.frame.DataFrame)
	assert isinstance(dic, dict)
	return df.groupby(dic).sum()

def ysumme(df,dic):
	assert isinstance(df, pd.core.frame.DataFrame)
	assert isinstance(dic, dict)
	return df.groupby(dic,axis=1).sum()

def xysumme(df,xdic,ydic):
	assert isinstance(df, pd.core.frame.DataFrame)
	assert isinstance(xdic, dict)
	assert isinstance(ydic, dict)
	return df.groupby(xdic).sum().groupby(ydic,axis=1).sum()

def summe(df):
	assert isinstance(df, pd.core.frame.DataFrame)
	return df.sum().sum()

################
### DIAGRAMM ###
################
def diagramm(df,ex='a.png',gattung='line'):
	p = df.plot(
		kind=gattung,
		figsize=(19.2,10.8),
		title='GEROP'
#		secondary_y = True,
	)
	return p

def line(df,ex='a.png'):
	p = diagramm(df,ex,'line')
	fig = p.get_figure()
	plt.close()
	pd2png(fig)

def bar(df,ex='a.png'):
	p = diagramm(df,ex,'bar')
	fig = p.get_figure()
	plt.close()
	pd2png(fig)

def barh(df,ex='a.png'):
	p = diagramm(df,ex,'barh')
	fig = p.get_figure()
	plt.close()
	pd2png(fig)

def area(df,ex='a.png'):
	p = diagramm(df,ex,'area')
	fig = p.get_figure()
	plt.close()
	pd2png(fig)

def bars(df,ex='a.png'):
	p = df.plot(
		kind='bar',
		figsize=(19.2,10.8),
		stacked=True,
#		secondary_y = True,
	)
	fig = p.get_figure()
	plt.close()
	pd2png(fig)

##### DIREKT ###############
if __name__=='__main__':
	df = txt2pd('c.tsv')
	df.info()
#	dic = xz.txt2dic('c.txt')
#	d = ysumme(df,dic)
#	print( d )
	line(df)

#base is from df1zs.py

"""
How to access to rows or columns by pandas
http://akiyoko.hatenablog.jp/entry/2017/04/03/081630
"""
