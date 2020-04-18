#!/usr/bin/python

### MODULES ###
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import wm
import xp
import xz

EIGENDATEI = 'a.txt'

#####################
### BASIC MODULES ###
#####################

def sache2df(sache):
	xz.str2txt('X'+sache,EIGENDATEI)
	tbl = xz.txt2tbl(EIGENDATEI)
	idx = tbl[0][0]
	tbl = []
	return pd.read_csv(EIGENDATEI,sep="\t",index_col=idx)

def df2sache(df):
	df.to_csv(EIGENDATEI,sep="\t",encoding="utf8")
	return '/' + xz.txt2str(EIGENDATEI)

#

###############################################################
#### DIESE PANDAS ###
#####################
def diese_xsumme(sache,dicfile):
	dic = xz.txt2dic(dicfile)
	df = sache2df(sache)
	df = xp.xsumme(df,dic)
	return df2sache(df)

def diese_ysumme(sache,dicfile):
	dic = xz.txt2dic(dicfile)
	df = sache2df(sache)
	df = xp.ysumme(df,dic)
	return df2sache(df)

def diese_xysumme(sache,dicfile):
	dic1 = dicfile[0] + '.tsv'
	dic1 = xz.txt2dic(dic1)
	dic2 = dicfile[1] + '.tsv'
	dic2 = xz.txt2dic(dic2)
	df = sache2df(sache)
	df = xp.xysumme(df,dic1,dic2)
	return df2sache(df)

##### DIREKT ###############
if __name__=='__main__':
	mode = 3
