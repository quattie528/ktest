#!/usr/bin/python

### MODULES ###
import io
import os
import re
import xt
import xz
#
import mich.becky2 # "mich/becky2.py"
import email
import email.policy
#import email.parser
#from email.parser import BytesParser
from datsun import *

policy = email.policy.SMTP

emails = mich.becky2.emails

#

####################
### MAIL to BODY ###
####################
def ml2body(ml):
	body = ml.get_body(preferencelist=('plain','html'))
	if not body == None:
		y = body.get_content()
	else:
		y = 'NONE'
	return y

def pureaddr(addr):
	addr = str(addr)
	addr = re.sub('.*<','',addr)
	addr = re.sub('>.*','',addr)
	return addr

#

##########################
### BECKY to LIST-DICT ###
##########################
#def becky2ldic(path,refnumber=nil):
def becky2ldic(weg):
	feilen = os.listdir(weg)
	feilen = [ x for x in feilen if '.bmf' in x ]
	#
	res = []
	for feile in feilen:
		ganz = []
		feile = weg + feile
		fh = open(feile, 'rb')
		stream = b''
		cnt = 0
		while 1:
			try:
				x = fh.readline()
				if x == b'':
					cnt += 1
					if cnt >= 10:
						break
				else:
					cnt = 0
				if x == b'.\r\n':
					ganz.append(stream)
					stream = b''
				else:
					stream += x
			except UnicodeDecodeError:
				msg = '<UnicodeDecodeError>'
				print( msg )
				stream = b''
				ganz.append(stream)

		teil = []
		for x in ganz:
#			policy = email.policy.SMTP
			ion = io.BytesIO(x)
			ml = email.message_from_binary_file(ion,policy=policy)
			"""
			print( ml['From'] )
			print( ml['To'] )
			print( ml['Date'] )
			body = ml.get_body()
			y = body.get_content()
			print( y )
#			print( x )
			exit()
			"""
			#
			res.append(ml)
			teil = []

	return res

# secondary ones
#def becky2ldic(path,refnumber=nil):
def becky2ldic2(weg,msgize=True):
	feilen = os.listdir(weg)
	feilen = [ x for x in feilen if '.bmf' in x ]
	#
	res = []
	for feile in feilen:
		lis = []
		feile = weg + feile
		fh = open(feile, 'r',encoding='utf-8')
		cnt = 0
		stream = ''
		while 1:
			try:
				x = fh.readline()
				x = x.rstrip()
				if x == '':
					cnt += 1
					if cnt >= 10:
						break
				else:
					cnt = 0
			except UnicodeDecodeError:
				x = ''
			#
			if x == '.':
				lis.append(stream)
				stream = ''
			else:
				stream += x + "\n"

		if msgize == False:
			res = lis
		else:
			for x in lis:
				msg = email.message_from_string(str(x))
				#
				## From, To, CC, BCC ##
				for k in ['from','to','cc','bcc']:
					if not k in msg: continue
					v = msg[k]
	#				v = re.sub(' \(.+','',v)
	#				v = re.sub('.+=','',v)
	#				v = re.sub('.+\n','',v)
					v = re.sub('.*<','',v)
					v = re.sub('>.*','',v)
					msg[k+'2'] = v
				#
				## Body ## ref the premier one
	#			v = email.parser.BytesParser().parse(x)
				#
				res.append(msg)

	return res

#

########################
### MAILER STATISTIK ###
########################
def mailer_statistik(weg):
	ldic = becky2ldic(weg)
	dic = {}
	for ml in ldic:
		aus = ml['From']
		aus = pureaddr(aus)
		xmailer = ml['X-Mailer']
		#
		if xmailer == None: xmailer = '<UNKNOWN>'
		#
		xmailer = xmailer.replace("\n",'')
		#
		if aus in dic:
			if xmailer in dic[aus]:
				pass
			else:
				dic[aus].append(xmailer)
		else:
			dic[aus] = []
			dic[aus].append(xmailer)
	return dic

#

#######################
### BECKY STATISTIK ###
#######################
def becky_statistik(weg):
	ldic = becky2ldic(weg)
	dic_from = {}
	dic_to = {}
	for ml in ldic:
		tag = ml['date']
		aus = ml['From']
		aus = pureaddr(aus)
		try:
			tag = parsetime(tag)
		except AssertionError:
			print( 'AssertionError HERE : %s' % tag )
			continue
		#
		v = tag.year * 100 + tag.month
		#
		if aus in emails:
			if v in dic_from:
				dic_from[v] += 1
			else:
				dic_from[v] = 0
		else:
			if v in dic_to:
				dic_to[v] += 1
			else:
				dic_to[v] = 0
	#
	m1 = min( list(dic_from.keys()) + list(dic_to.keys()) )
	m2 = max( list(dic_from.keys()) + list(dic_to.keys()) )
#	ms = xd.intmonths(m1,m2) # revolution(xd.py->xt.py)
	ms = xt.imvec(m1,m2)
	ldic = []
	for v in ms:
		dic = {}
		dic['from'] = dic_to.get(v,0)
		dic['to'] = dic_from.get(v,0)
		#
		v = str(v)
		dic['month'] = '%s_%s' % (v[0:4],v[4:6])
		ldic.append(dic)
	xz.show(ldic,['month','from','to'])

#

##### DIREKT ###############
if __name__=='__main__':
	mode = 2
	pfad4becky = mich.becky2.beckyPfad1 # Freund
#	pfad4becky = mich.becky2.beckyPfad2 # Einkauf
	if mode == 1: #1
		res = mailer_statistik(pfad4becky)
	elif mode == 2: #2
		becky_statistik(pfad4becky)
