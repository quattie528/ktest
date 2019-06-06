#!/usr/bin/python

### MODULES ###
import os
import time
import clipboard
import pyautogui as pgui

pgui.FAILSAFE = True


if os.name == 'nt':
	import ctypes
	user32 = ctypes.windll.user32
	BildschirmX = user32.GetSystemMetrics(0)
	BildschirmY = user32.GetSystemMetrics(1)
	#print( BildschirmX )
	#print( BildschirmY )
elif os.name == 'posix':
	BildschirmX = 777
	BildschirmY = 777


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
	pgui.moveTo(BildschirmX,BildschirmY)
	if sek < 8:
		pgui.moveTo(2,2,sek)
	else:
		pgui.moveTo(2,2,8)
		pgui.moveTo(2,2,sek-8)

### CLICK ###
def click(x,y):
	pgui.moveTo(x,y)
	try:
		pgui.click()
	except PermissionError:
		pass

### FEW CLICK ###
def fewclick(times,x,y):
	for i in range(times):
		pgui.moveTo(x,y)
		try:
			pgui.click()
		except PermissionError:
			pass

