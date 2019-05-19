#!/usr/bin/python

### MODULES ###
#import datetime
#import os
import pprint
#
import mysql.connector
#import sqlalchemy as sa
#import clipboard
#
#from datsun import *
import xz
import mich.dbenv as dbdb
import kbench
#
#1:battery,2:pip,3:mygen,4:myopus

### VARIABLES ###
DEBUG = True
DEBUG = False

#

####################
### MY CONNECTOR ###
####################
def myconn(dbname,diccur=False):
	### KONSTANT ###
	conn = mysql.connector.connect(
	    host = dbdb.IP4SVR,
	    port = 3306,
	    user = dbdb.GENUTZER,
	    password = dbdb.KENNWORT,
	    connection_timeout = 1, # 2019-05-04
	    database = dbname,
#	    cursorclass=cursors.DictCursor
	)
	return conn

#

###################
### TEXT zu SQL ###
###################
def txt2sql(txt,name):
	ur = ''
	res = ''
	sym = "[%s]" % name
	with open(txt, 'r',encoding='utf-8') as f:
		ur = f.readlines()
		ur = [ x.replace("\n",'') for x in ur ]

	geh = False
	for x in ur:
		if sym == x:
			geh = True
			continue
		if geh == False: continue
		if x == '': continue
		if x[0] == '#': continue
		if x[0] == '[':
			if x[-1] == ']':
				break
		res += x
		res += "\n"

	if res == '':
		error = "The name does not exist in this text: '%s' in '%s'"
		error %= (name,txt)
		raise KeyError(error)

	return res

#

#############################
### LIST-DICT zu DATABASE ###
#############################
def ldic2db(ldic,dbname,tblname,keyid=''):
	kopfer = ldic[0].keys()
	kopfer = list(kopfer)
	kopfer.sort()
#	kopfer = kopfer[0:5]
	kopferS = ','.join(kopfer)
#	placeholder = [ '?' for x in range(len(kopfer)) ] # NG
	placeholder = [ '%s' for x in range(len(kopfer)) ]
	placeholder = ','.join(placeholder)
	#
	stmt1 = "SELECT %s FROM %s WHERE %s = '%%s' LIMIT 1"
	stmt1 = stmt1 % (keyid,tblname,keyid)
	print( stmt1 )
	stmt2 = "INSERT INTO %s (%s) \nVALUES (%s)"
	stmt2 = stmt2 % (tblname,kopferS,placeholder)
#	print( stmt2 )
#	stmt2 = 'SELECT * FROM auth_user'
	#
	dbh = myconn(dbname)
	cur = dbh.cursor()

	### HAUPT ###
	res = []
	fehler = 0
	for dic in ldic:

		## Seek ##
		if not keyid == '':
			cur.execute(stmt1 % dic[keyid])
			data = cur.fetchone()
			if data == None:
				pass
			else:
#			elif data[0] == keyid:
#				print( dic[keyid] )
				continue
		## Insert ##
		tup = []
		for k in kopfer:
			w = dic[k]
#			if isinstance(w, str):
#				w = w.replace("'","\\'")
			tup.append(w)
		tup = tuple(tup)
#		print( tup )
		try:
			cur.execute(stmt2,tup)
		except mysql.connector.errors.IntegrityError:
			print( dic['cid'],end=', ' )
		except mysql.connector.errors.DataError:
			print( '' )
			print( '%%% INSERSION FAILED ',end='' ) #d
			print( '%'*20 ) #d
			pprint.pprint( dic )
			fehler += 1
		except mysql.connector.errors.DatabaseError:
			print( '%'*40 ) #d
			pprint.pprint( tup )
			cur.execute(stmt2,tup)
			exit()
		dbh.commit()

	### BERICHT ###
	print( '[%s] Fehler ist %d !' % (tblname,fehler) )
	return True

#############################
### DATABASE zu LIST-DICT ###
#############################
def db2ldic(dbname,tblname):
	hdl = myconn(dbname)
	cur = hdl.cursor(dictionary=True)
	#
	stmt = 'SELECT * FROM ' + tblname
	#
	cur.execute(stmt)
	data = cur.fetchall()
	return data

def db2pd():
	pass
#http://thr3a.hatenablog.com/entry/20180813/1534119493

def maxid(keyid,dbname,tblname):
	hdl = myconn(dbname)
	cur = hdl.cursor()
	#
	stmt = 'SELECT MAX(%s) FROM %s'
	stmt %= (keyid,tblname)
	#
	cur.execute(stmt)
	data = cur.fetchone()
	data = data[0]
	return data

def db2sel(lis,colname,dbname,tblname):
	hdl = myconn(dbname)
	cur = hdl.cursor(dictionary=True)
	#
	stmt = "SELECT * FROM %s WHERE %s = '%%s'; "
	stmt %= (tblname,colname)
	#
	res = []
	for x in lis:
		sql = stmt % x
		cur.execute(sql)
		data = cur.fetchone()
		res.append(data)
	#
	return res
	kopfer = res[-1].keys() #d
	xz.ldic2txt(res,'a.tsv',kopfer) #d

def desctbl(dbname,tblname):
	hdl = myconn(dbname)
	cur = hdl.cursor()
	stmt = "DESC %s; " % tblname
	cur.execute(stmt)
	data = cur.fetchall()
	pprint.pprint( data )

def execmsql(stmt,dbname):
	dbh = myconn('zg')
	cur = dbh.cursor()

	for sql in stmt.split(';'):
		if sql.strip() == '': continue
		x = cur.execute(sql)
		y = dbh.commit()
		print( "\n%%% EXECUTED THIS SQL ",'%'*20 ) #d
		if sql[0] == "\n": sql = sql[1:]
		print( sql ) #d
		print( type(x),x )
		print( type(y),y )
	cur.close()
	dbh.close()
	return True

def fetch(sql,dbname,dicmode=True):
	dbh = myconn(dbname)
	cur = dbh.cursor(dictionary=dicmode)
	cur.execute(sql)
	res = cur.fetchall()
	cur.close()
	dbh.close()
	return res

def commit(sql,dbname):
	dbh = myconn(dbname)
	cur = dbh.cursor()
	cur.execute(sql)
	dbh.commit()
	cur.close()
	dbh.close()
	return True

def getheader(dbname,tblname):
	from collections import OrderedDict
	res = OrderedDict()
	dbh = myconn(dbname)
	cur = dbh.cursor(dictionary=True)
	sql = 'DESC ' + tblname
	cur.execute(sql)
	for dic in cur.fetchall():
		x = dic['Field']
		y = dic['Type']
		res[x] = y
	cur.close()
	dbh.close()
	return res

def execp(txt,name,dbname):
	sql = txt2sql(txt,name)
	dbh = myconn(dbname)
	cur = dbh.cursor()
	cur.execute(sql)
	res = cur.fetchall()
	cur.close()
	dbh.close()
	return res
