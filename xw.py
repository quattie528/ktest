#!/usr/bin/python

# Name als Huldigung zu Wes McKinney, das ist für laden
# name as homage to Wes McKinney

### MODULES ###
import pandas as pd
import matplotlib.pyplot as plt
import xz


###################################
### ZWISCHEN DATEIEN und PANDAS ###
###################################
def tbl2pds(tbl,kopfer=True):
	cols = tbl.pop(0)
	df = pd.DataFrame(tbl,columns=cols)
	return df

def ldic2pds(ldic,header=[]):
	if header == []: header = ldic[0].keys()
	df = pd.DataFrame(ldic,columns=header)
	df.index.name = 'idx'
	#
	datei = 'a.tmp'
	df.to_csv(datei,sep="\t",encoding="utf8")
	df = pd.read_csv(datei,sep="\t",index_col='idx')
	return df

def tbl2bins(tbl,weg):
	assert weg[-4] == '.'
	#
	xz.notice = False
	#
	weg2 = weg[:-4] + '.tsv'
	xz.tbl2txt(tbl,weg2)
	#
	weg2 = weg[:-4] + '.bin'
	xz.obj2bin(tbl,weg2)
	#
	tbl = tbl2pds(tbl)
	weg2 = weg[:-4] + '.pds'
	xz.obj2bin(tbl,weg2)
	#
	xz.notice = True
	print( "\tAusgabe als res/iudicata/CRM.pds et al." )


def pds2ldic(df):
	return df.to_dict(orient='records')

def pds2tbl(df,index=True):
	index = df.columns.tolist()
	tbl = df.values.tolist()
	tbl.insert(0,index)
#	xz.tbl2txt(tbl,'a.tsv')
	return tbl

def sicher(df,datei,tsvtoo=True):
	if datei[-4:] == '.bin':
		tsv = datei.replace('bin','tsv')
		bin = datei
	elif datei[-4:] == '.tsv':
		tsv = datei
		bin = datei.replace('tsv','pds')
	elif datei[-4:] == '.pds':
		tsv = datei.replace('pds','tsv')
		bin = datei
	else:
		print( 'Name muss bin/tsv/pds sein' )
		exit()

	xz.obj2bin(df,bin)
	if tsvtoo == True:
		xz.tbl2txt(pds2tbl(df),tsv)

#

##### DIREKT ###############
if __name__=='__main__':
	pass
	import xz
	tbl = xz.txt2tbl('res/PH.tsv')
	df = tbl2pds(tbl)
#	df.info()
	save(df,'a.bin')

