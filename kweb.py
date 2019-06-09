#!/usr/bin/python

### MODULES ###
import requests
import sys
import re
import time
import random
#import kbench
import platform
import urllib.parse
#
import webbrowser as wb
import pyautogui as pgui
#
import xz
import xu
from datsun import *
#
""" DEFINITION ###
(1) url2html
(2) url2datei
(3) url2txt
"""

#pgui.FAILSAFE = True

wart_min = 3
wart_max = 20
wart_min = 10 # EDGAR @ 2018-08-09
wart_max = 30

NACHLADEN = 'C:/Users/Katsushi/Downloads/'

#

###################
### URL to HTML ###
###################
def url2html(addr):
	html = requests.get(addr)
	html = html.text
	#
	"""
	html = html.replace('="http', '="ttp' )
	html = html.replace("='http", "='ttp" )
	html = html.replace('=http', '=ttp' )
	html = html.replace('"JavaScript"','"avaScript"')
	html = html.replace("'JavaScript"',"'avaScript"')
	html = html.replace('/JavaScript','/avaScript')
	"""
	html = html.replace('http', 'hhttp' )
	return html

def urls2html(datei,ex='a.html'):
	import datetime
	#
	lis = xz.txt2lis(datei)
	print( 'GEHEN ZU HANDEL ... "%s" ' % datei )
#	w = len(lis) * wart_max # 2016-07-10
	w = len(lis) * (wart_max+wart_min) / 2
	wv = str(datetime.timedelta(seconds=w))
	print( 'DAS NIMMT : %s sec = %s" ' % (w,wv) )
	print( '*' * 30 )
	#
	with open(ex, 'w',encoding='utf-8') as gh:
		for i,addr in enumerate(lis):
			gh.write("<URL>%s\n\n" % addr)
			gh.write( url2html(addr) )
			print( '[%d] Acquired ... || %s' % (i+1,addr) )
			#
			m = random.randrange(wart_min,wart_max)
			print( "\t\tSleeping... (_ _)~~~ for %d sec.... " %m )
			xu.sleep(m)
	sys.stdout.write('Ausgabe als %s\n' % ex)

def urls2htmls(datei,pfad4ex):
	import datetime
	import random
	#
	if os.name == 'nt':
		assert ':' in pfad4ex
	elif os.name == 'posix':
		assert pfad4ex[0] == '/'
	pfad4ex = pfad4ex.replace('\\','/')
	if not os.path.exists(pfad4ex):
		os.mkdir(pfad4ex)
	#
	tbl = xz.txt2tbl(datei)
	print( 'GEHEN ZU HANDEL ... "%s" ' % datei )
	w = len(tbl) * (wart_max+wart_min) / 2
	wv = str(datetime.timedelta(seconds=w))
	print( 'DAS NIMMT : %s sec = %s" ' % (w,wv) )
	print( '*' * 30 )
	#
	for i,lis in enumerate(tbl):
#		print( lis ) #d
		addr = lis.pop(0)
		dest = lis.pop(0)
		dest= pfad4ex + dest
		#
		if os.path.exists(dest): continue
		#
		x = "<URL>%s\n\n" % addr
		x += url2html(addr)
		xz.str2txt(x,dest)
		print( '[%d] Acquired ... || %s' % (i+1,addr) )
		#
		m = random.randrange(wart_min,wart_max)
		print( "\t\tSleeping... (_ _)~~~ for %d sec.... " %m )
#		xu.sleep(m) # 2018-11-23
		time.sleep(m) # ob nicht durch Browser, nuzten time.sleep

#

####################
### URL to DATEI ###
####################
def url2datei(url,ausgabe):

	### MODUL ###
	import shutil

	### KONSTANT ###
	datei = re.sub('.+/','',url)
	datei = NACHLADEN + datei
	teil = datei + '.part'
	ausgabe2 = NACHLADEN + ausgabe
	if os.path.exists(datei):
		shutil.move(datei,ausgabe2)
		x = 'Bewegt %s...' % ausgabe
		print( x )
		return True
	#
	wb.open(url)
#	wb.open_new_tab(url)
	#
	xu.sleep(2)
#	pgui.click(x=1000, y=500)
#	pgui.keyDown('ctrl')
#	pgui.press('w')
#	pgui.keyUp('ctrl')
	#
	key = 0
	i = 0
	kein = 0
	while True:
		i += 1
		if os.path.exists(teil):
			if not key == 1:
				print( "\nSLEEP / Teil Existert : ", end='')
			print('%d, '%i, end='')
			key = 1
			xu.sleep(1)
			continue
		#
		try:
			os.path.getsize(datei)
		except FileNotFoundError:
			kein += 1
			if kein == 5:
				print( "\n- PASS / %s : " % datei , end='')
				break
			xu.sleep(1)
		#
		if os.path.getsize(datei) == 0:
			if not key == 2:
				print( "\nSLEEP 2 / Get Size : ", end='')
			print('%d, '%i, end='')
			xu.sleep(1)
		else:
			break

	### AUSGABE ###
	xu.sleep(2)
	xu.click(797,16)
	pgui.keyDown('ctrl')
	pgui.press('w')
	pgui.keyUp('ctrl')
	#
#	print( datei ) #d
#	print( ausgabe ) #d
	shutil.move(datei,ausgabe2)
#	exit() #d

#

###################
### URL to TEXT ###
###################
def url2txt(url,ausgabe):
#	print( 'Recommend wget2.uws' )
#	exit()

	### MODUL ###
	import clipboard
	import webbrowser as wb
	import pyautogui as pgui
	import xu

	### KONSTANT ###
	print( url ) #d
	wb.open(url)
	m = random.randrange(wart_min,wart_max)
	xu.sleep(m)
	#
	xpos4sicher = 2
	ypos4sicher = 2
	#1640,20
	#797,16  # leftside
	#
	ausgabe = ausgabe.replace('/','\\')
	clipboard.copy(ausgabe)
	xu.click(xpos4sicher,ypos4sicher) # Golden Position
#	exit() #d
	pgui.keyDown('ctrl')
	pgui.press('s')
	pgui.keyUp('ctrl')
	print( "\tCtrl-S, ", end="" ) #d
	xu.sleep(3)
	#
	pgui.keyDown('ctrl')
	pgui.press('v')
	pgui.keyUp('ctrl')
	print( 'Ctrl-V, ', end="" ) #d
#	xu.sleep(3)
	xu.sleep(1) # 2018-12-12
	#
	pgui.press('enter')
	print( 'Enter, ', end="" ) #d
#	xu.sleep(1)
	xu.sleep(0.5) # 2018-12-12

	### AUSGABE ###
	xu.click(xpos4sicher,ypos4sicher) # Golden Position
	print( 'Click, ', end="" ) #d
	pgui.keyDown('ctrl')
	pgui.press('w')
	pgui.keyUp('ctrl')
	print( 'Ctrl-W', end="" ) #d
	print( '' ) #d

def urls2txts(paartxt):
	paaren = xz.txt2tbl(paartxt)
	for lis in paaren:
		url = lis[0]
		ausgabe = lis[1]
		if os.path.exists(ausgabe): continue # 2019-06-07
		url2txt(url,ausgabe)

def url2src(url,ausgabe):
	pass

def url2clip(url,xpos=1660,ypos=130,schlaf=2):
	import clipboard
	import webbrowser as wb
	import pyautogui as pgui
	import xu
	#
	wb.open(url)
#	wb.open_new_tab(url)
	xu.sleep(schlaf)
	xu.click(xpos,ypos)
	pgui.keyDown('alt')
	pgui.press('x')
	pgui.keyUp('alt')
	pgui.keyDown('ctrl')
	pgui.press('a')
	pgui.press('c')
	pgui.press('w')
	pgui.keyUp('ctrl')
	#
	wert = clipboard.paste()
	#
	pgui.keyDown('alt')
	pgui.press('tab')
	pgui.keyUp('alt')
	return wert

def url2encode(url):
	x = urllib.parse.quote(url)
	return x

def url2decode(url):
	x = urllib.parse.unquote(url)
	return x

##### DIREKT ###############
if __name__=='__main__':
	pass
