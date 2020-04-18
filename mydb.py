#!/usr/bin/python

### MODULES ###
#import datetime
#import os
import time
import pprint
#
import mysql.connector
#import sqlalchemy as sa
#import clipboard
#
from datsun import *
import xz
import mich.dbenv as dbdb
#import kbench
#
#1:battery,2:pip,3:mygen,4:myopus

### VARIABLES ###
DEBUG = True
DEBUG = False
#
DBNAME = 'your_database_name'

#

####################
### MY CONNECTOR ###
####################
def myconn():
	### KONSTANT ###
	conn = mysql.connector.connect(
		host = dbdb.IP4SVR,
		port = 3306,
		user = dbdb.GENUTZER,
		password = dbdb.KENNWORT,
		connection_timeout = 1, # 2019-05-04
		database = DBNAME,
#		cursorclass=cursors.DictCursor
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

def daemon_erholung(dic,msg):
	print( msg,end='' ) #d
	print( '%'*20 ) #d
	pprint.pprint( dic )
	time.sleep(1)

### CONF ###############################################

#

#############
### MAXID ###
#############
def maxid(tblname):
	hdl = myconn()
	cur = hdl.cursor()
	#
	data = desctbl(tblname)
	prikey = ''
	for x in data:
		if x[3] == 'PRI':
			prikey = x[0]
			break
	#
	stmt = 'SELECT MAX(%s) FROM %s'
	stmt %= (prikey,tblname)
	#
	cur.execute(stmt)
	data = cur.fetchone()
	data = data[0]
	return data

#

##################
### DESC TABLE ###
##################
def desctbl(tblname):
	hdl = myconn()
	cur = hdl.cursor()
	stmt = "DESC %s; " % tblname
	cur.execute(stmt)
	data = cur.fetchall()
	return data

#

##################
### GET HEADER ###
##################
def getheader(tblname):
	from collections import OrderedDict
	res = OrderedDict()
	dbh = myconn()
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

#

### Crud #################################################

#

#############################
### LIST-DICT zu DATABASE ###
#############################
def ldic2db(ldic,tblname,keyid=''):
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
	dbh = myconn()
	cur = dbh.cursor()

	### HAUPT ###
	res = []
	fehler = 0
	i = 0
	while 1:
		try:
			dic = ldic[i]
		except IndexError:
			break
		print( i ) #d

		## Seek ##
		"""
		print( 1222 )
		if not keyid == '':
			cur.execute(stmt1 % dic[keyid])
			data = cur.fetchone()
			if data == None:
				pass
			else:
#			elif data[0] == keyid:
#				print( dic[keyid] )
				continue
		"""

		## Insert ##
		tup = []
		for k in kopfer:
			w = dic[k]
#			if isinstance(w, str):
#				w = w.replace("'","\\'")
			tup.append(w)
		tup = tuple(tup)
#		print( tup )
		if ( i + 1 ) % 500 == 0:
			print( '- Endet Nummer',i )
		try:
			cur.execute(stmt2,tup)
		except mysql.connector.errors.IntegrityError:
			# e.g. against UNIQUE RULE @2020-01-02
			daemon_erholung(dic,'%%% INTEGRITY ERROR ')
			continue
		except mysql.connector.errors.DataError:
			daemon_erholung(dic,'%%% INSERSION FAILED ')
			fehler += 1
			continue
		except mysql.connector.errors.DatabaseError:
			daemon_erholung(tup,'%%% DATABASE ERROR ')
			continue
		#
		try:
			dbh.commit()
		except mysql.connector.errors.DatabaseError:
			daemon_erholung(tup,'%%% DATABASE ERROR ')
			i += 1
			continue
		except mysql.connector.errors.OperationalError:
			daemon_erholung(tup,'%%% OPERATIONAL ERROR ')
			continue

		## Zahlen ##
		i += 1

	### BERICHT ###
	dbh.close()
	print( '[%s] Fehler ist %d !' % (tblname,fehler) )
	return True

### cRud #################################################

#############################
### DATABASE zu LIST-DICT ###
#############################
def db2ldic(tblname):
	sql = 'SELECT * FROM ' + tblname
	res = fetch(sql,True)
	return res

#

#############
### FETCH ###
#############
def fetch(sql,dicmode=True):
	dbh = myconn()
	cur = dbh.cursor(dictionary=dicmode)
	cur.execute(sql)
	res = cur.fetchall()
	cur.close()
	dbh.close()
	return res

def db2pd():
	pass
#http://thr3a.hatenablog.com/entry/20180813/1534119493

"""
def db2sel(lis,colname,tblname):
	hdl = myconn()
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
"""

### crUd #################################################

def execmsql(stmt):
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

def commit(sql):
	dbh = myconn()
	cur = dbh.cursor()
	cur.execute(sql)
	dbh.commit()
	cur.close()
	dbh.close()
	return True

"""
def execp(txt,name):
	sql = txt2sql(txt,name)
	dbh = myconn()
	cur = dbh.cursor()
	cur.execute(sql)
	res = cur.fetchall()
	cur.close()
	dbh.close()
	return res
"""

def replace(tblname,kolonne,idname,vor,nach):
	stmt = 'SELECT %s,%s FROM %s'
	stmt %= (idname,kolonne,tblname)
	data = fetch(stmt)

	dbh = myconn()
	cur = dbh.cursor()

	n = 0
	summe = 1
	stmt = "UPDATE %s SET %s = '%s' WHERE %s = %d"
	for paar in data:
		id = paar[idname]
		w1 = paar[kolonne]
		if w1 == None: continue
		w2 = w1.replace(vor,nach)
		w2 = w2.replace("'","\\'")
		#
		if w1 == w2: continue
		sql = stmt % (tblname,kolonne,w2,idname,id)
#		print( '%'*40,"\n",sql ) #d
		cur.execute(sql)
		dbh.commit()
		#
		n += 1
		summe += 1
		if n == 100:
			dbh.commit()
			n = 1
	if n == 0:
		dbh.commit()

	dbh.close()
	print( '* Summe als ',summe )

#

##########################
### DICT zu UPDATE SQL ###
##########################
def dic2update(dic,tblname,keyid):

	### TOR ###
	assert keyid in dic
	
	### VORBEREITUNG ###
	for k in dic.keys():
		w = dic[k]
		w = str(w)
		w = w.replace("'","\\'")
		dic[k] = w

	### HAUPT ###
	stmt = 'UPDATE ' + tblname
	stmt += "\nSET "
	lis = []
	for k,w in dic.items():
		if k == keyid: continue
		w = "%s = '%s' " % (k,w)
		lis.append(w)
	stmt += ",\n".join(lis)
	stmt += " \n"
	stmt += 'WHERE cid = %s ;' % dic[keyid]
	#
	return stmt

"""
[SQLAlchemy Users]
Yelp!
reddit
DropBox
The OpenStack Project
Survey Monkey
"""
