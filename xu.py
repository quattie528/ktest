#!/usr/bin/python

### MODULES ###
import os
import time
import clipboard
import pyautogui as pgui
#
import xz

pgui.FAILSAFE = True

"""
if os.name == 'nt':
	import ctypes
	user32 = ctypes.windll.user32
	BildschirmX = user32.GetSystemMetrics(0) - 100
	BildschirmY = user32.GetSystemMetrics(1) - 100
#	print( BildschirmX ) #d
#	print( BildschirmY ) #d
elif os.name == 'posix':
	BildschirmX = pgui.size().width
	BildschirmY = pgui.size().height
"""

#-------------------------------------------------
##################
### MAUSKATZE  ###
##################
class mauskatze(dict):
	def __init__(my,wert):
		if isinstance(wert, str):
			ddic = xz.txt2ddic(wert,'KEY')
		elif isinstance(wert, dict):
			ddic = wert
		else:
			assert isinstance(wert, dict)

		for k,dic in ddic.items():
			my[k] = {}
			my[k]['X'] = int( dic['X'] )
			my[k]['Y'] = int( dic['Y'] )

	def klick(my,ref,schau=False):
		x = my[ref]['X']
		y = my[ref]['Y']
		click(x,y)
		if schau == True:
			x = '# Klicken, X:%d, Y:%d' % (x,y)
			print( x )

	def rklick(my,ref,schau=False):
		x = my[ref]['X']
		y = my[ref]['Y']
		click(x,y,'right')
		if schau == True:
			x = '# Klicken, X:%d, Y:%d' % (x,y)
			print( x )

	def gleit(my,ref,wieviel,xy='X',sprung=10):
		assert isinstance(wieviel, int)
		assert xy in 'XY'
		assert isinstance(sprung, int)
		for i in range(wieviel):
			x = my[ref]['X']
			y = my[ref]['Y']
			if xy == 'X':
				x += i * sprung
			elif xy == 'Y':
				y += i * sprung
			click(x,y,lr)
	def xgleit(my,ref,n,sprung): gleit(ref,n,'X',sprung)
	def ygleit(my,ref,n,sprung): gleit(ref,n,'Y',sprung)
"""
[BEISPIEL für MAUSKATZE]
KEY	X	Y
NUL	025	300
PLA	263	100
BSA	364	100
ANN	534	100
QTR	592	100
"""
#-------------------------------------------------

#

### FEW BUTTON ###
def fewbutton(times,key,press=''):
	if not press == '': pgui.keyDown(press)
	for i in range(times): pgui.press(key)
	if not press == '': pgui.keyUp(press)

### KEY ###
def key(key):
	pgui.press(key)

### ALT KEY ###
def akey(key):
	pgui.keyDown('alt')
	pgui.press(key)
	pgui.keyUp('alt')

### CTRL KEY ###
def ckey(key):
	pgui.keyDown('ctrl')
	pgui.press(key)
	pgui.keyUp('ctrl')

### SHIFT KEY ###
def skey(key):
	pgui.keyDown('shift')
	pgui.press(key)
	pgui.keyUp('shift')

### COMMAND KEY ###
def mkey(key):
	pgui.keyDown('command')
	pgui.press(key)
	pgui.keyUp('command')

### CTRL-SHIFT KEY ###
def cskey(key):
	pgui.keyDown('ctrl')
	pgui.keyDown('shift')
	pgui.press(key)
	pgui.keyUp('shift')
	pgui.keyUp('ctrl')

### SIGH ###
def sigh():
	sleep(1)

### PASTE ###
def paste(v):
	clipboard.copy(v)
	ckey('v')

### PASTE ###
def copyall():
	pgui.keyDown('ctrl')
	ckey('a')
	ckey('c')
	pgui.keyUp('ctrl')

### SLEEP ###
def sleep(sek):
#	print( BildschirmX ) #d
#	print( BildschirmY ) #d
	x = pgui.size().width  - 50
	y = pgui.size().height - 50
#	pgui.moveTo(BildschirmX,BildschirmY)
	pgui.moveTo(x,y)
	if sek < 8:
#		pgui.moveTo(200,200)
		pgui.moveTo(2,2,sek)
		pass
	else:
		pgui.moveTo(2,2,8)
		pgui.moveTo(2,2,sek-8)

### CLICK ###
def click(x,y,lr='left'):
	pgui.moveTo(x,y)
	try:
		pgui.click(button=lr)
	except PermissionError:
		pass

def clickhere():
	x, y = pgui.position()
	click(x,y)

### FEW CLICK ###
def fewclick(times,x,y):
	for i in range(times):
		pgui.moveTo(x,y)
		try:
			pgui.click()
		except PermissionError:
			pass

def max2left():
	pgui.hotkey('alt','space')
	pgui.press('x')
	pgui.hotkey('win','left')

#

######################
### VIDEOAUFLÖSUNG ###
######################
def auflosung():
#	from win32api import GetSystemMetrics
	x = pgui.size().width
	y = pgui.size().height
	return (x,y)
