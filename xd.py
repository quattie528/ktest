#!/usr/bin/python

### MODULES ###
#import datetime
#import os
import pprint
#
import pickle
import pandas as pd
#
from datsun import *
import xz
#import kbench
#
#1:battery,2:pip,3:mygen,4:myopus

### VARIABLES ###
debug = True
debug = False

#

####################
### TEXT zu LIST ###
####################
def txt2lis(txt):
	fh = open(txt, 'r',encoding='utf-8')
	res = []
	zahl = 0
	while 1:
		x = fh.readline()
		if not x: break
		zahl += 1
		x = x.strip()
		res.append(x)
		print( repr(x) ) #d
	print( '* Das ist %d Linie' % zahl )
	return res

#

#################
### DICT-DICT ###
#################
def ddic2pd(ddic):
	xs = list(ddic.keys())
	ys = []
	for x,dic in ddic.items():
		for k in dic.keys():
			if k in ys: continue
			ys.append(k)
	xs.sort()
	ys.sort()
	tbl = xz.ddic2tbl(ddic,xs,ys)
	xs = tbl.pop(0)
	xs.pop(0)
	ys = [ lis[0] for lis in tbl ]
	for lis in tbl: lis.pop(0)
	df = pd.DataFrame(tbl,columns=xs,index=ys)
	return df

def ddic2db(pk):
	pass

########################
### PANDAS-DATAFRAME ###
########################
def pd2ldic(pd):
	ldic = []
	keys = pd.columns
	print( pd )
	for i,vec in pd.iteritems():
		dic = {}
		print( i )
		exit()
		print( vec )
		for k in keys:
			dic[k] = vec[k]
		print( dic )
	print( pd )
	
	pass
def pd2db(pd):
	pass
def pd2txt(pd,ausgabe):
	pass

def db2pk(db):
	pass
def db2pd(db):
	pass
def db2txt(db):
	pass

def txt2pd(eingabe):
	pass
def txt2db(eingabe):
	pass

def ldic2sqlite(ldic,dbdatei,tafelname):
	import sqlite3
	conn = sqlite3.connect(dbdatei)
	#
	kopfer = list(ldic[0].keys())
	sql1 = ','.join(kopfer)
	sql2 = [ '?' for x in range(len(kopfer)) ]
	sql2 = ','.join(sql2)
	sql = 'INSERT INTO %s(%s) VALUES(%s)'
	sql = sql % (tafelname,sql1,sql2)
	#
	ldic2db(ldic,sql,conn)
	conn.close()

def ldic2mysql(ldic,dbdatei,tafelname):
	import mysql.connector
	conn = mysql.connector.connect(
	    host = '192.168.1.1',
	    port = 3306,
	    user = 'user',
	    password = 'password',
	    database = 'dbname'
	)
	#
	kopfer = list(ldic[0].keys())
	sql1 = ','.join(kopfer)
	sql2 = [ '?' for x in range(len(kopfer)) ]
	sql2 = ','.join(sql2)
	sql = 'INSERT INTO %s(%s) VALUES(%s)'
	sql = sql % (tafelname,sql1,sql2)
	#
	ldic2db(ldic,sql,conn)
	conn.close()


def ldic2db(ldic,sql,conn):
	cur = conn.cursor()
	tmp = []
	zahl = 0
	for dic in ldic:
		werten = [ dic[x] for x in kopfer ]
		werten = tuple(werten)
		tmp.append(werten)
		zahl += 1
		if zahl == 10000:
			cur.executemany(sql,tmp)
			conn.commit()
			tmp = []
			zahl = 0


#

##### DIREKT ###############
if __name__=='__main__':
	pass
