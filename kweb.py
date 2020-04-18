#!/usr/bin/python

### MODULES ###
import requests
import sys
import re
import time
import random
#import kbench
import platform
#
import clipboard
import webbrowser as wb
import pyautogui as pgui
#
import xz
import xu
import dritt
from datsun import *
#
""" DEFINITION ###
(1) url2cmd2html()
(2) url2mff2html()
(3) url2mff2clp()
(4) url2mff2datei()

* mff : Mozilla FireFox
* ggc : Google Chrome
"""

#__pycache__/kweb_2020-03-29.py
#pgui.FAILSAFE = True

### KONSTANT ###
wart_min = 3
wart_max = 20
wart_min = 10 # EDGAR @ 2018-08-09
wart_max = 30
WART4BRW = 3
#
NLPFAD = 'C:/Users/Katsushi/Downloads/'
NLPFAD = 'C:/Users/katsu/Downloads/'

#

def wahlbrowser(brw='chrome'):
	### STARTEN ###
	try:
		res = xz.bin2obj(labomi + 'browser.bin')
	except FileNotFoundError:
		res = dritt.which_browser()
		res = xz.obj2bin(res,labomi + 'browser.bin')
	brw = res[brw]
	brw = wb.get(brw+' %s')
	return brw

#

##############################
### URL to KOMMAND zu HTML ###
##############################
def url2cmd2html(addr):
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

#

###############################
### URL zu FIREFOX zu DATEI ###
###############################
def url2mff2datei(url,ausgabe):

	### MODUL ###
	import shutil

	### KONSTANT ###
	datei = re.sub('.+/','',url)
	datei = NLPFAD + datei
	teil = datei + '.part'
	if '/' in ausgabe:
		ausgabe2 = ausgabe
	else:
		ausgabe2 = NLPFAD + ausgabe
#	print( datei ) #d
#	print( ausgabe2 ) #d
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
	for zt in range(30):
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
	#
	if os.path.getsize(datei) == 0:
		os.remove(datei)
		return False

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
	return True
#	exit() #d

#

#############################
### URL zu FIREFOX zu TXT ###
#############################
def url2mff2txt(url,ausgabe):
#	print( 'Recommend wget2.uws' )
#	exit()

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

#

###################################
### URL zu FIREFOX zu CLIPBOARD ###
###################################
def url2mff2clip(url,brw='firefox'):
	brw = 'firefox'
	brw = 'chrome'
	if brw == 'chrome':
		wb = wahlbrowser(brw)

	wb.open(url)
#	wb.open_new_tab(url)
	xu.sleep(WART4BRW)
	
	if brw == 'firefox':
		xu.click(155,50)
	elif brw == 'chrome':
#		xu.click(10,20)
		xu.click(65,40)
	pgui.hotkey('alt','space')
	pgui.press('x')
	for k in 'accw':
		time.sleep(0.3)
		pgui.hotkey('ctrl',k)
	#
	wert = clipboard.paste()
	return wert

##### DIREKT ###############
if __name__=='__main__':
	pass
