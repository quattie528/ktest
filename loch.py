### MODUL ###
import os
import pprint
import yaml

### KOPFER ###
kys = [
	'labomi','inconf','mydata','myname','urpfad',
	'klogpfad','kbenchlog','kbenchset'
]

### HAUPT ###
datei = 'D:/var/conf.txt'
#datei = 'D:/var/debug.txt' #d
if os.name == 'posix':
	datei = '/Users/katsushi/vw/var/conf.txt'
if not os.path.exists(datei):
	datei = 'conf.txt'
#	datei = 'debug.txt' #d

if os.path.exists(datei):
	with open(datei) as fh:
		dic = yaml.load(fh,Loader=yaml.BaseLoader)
else:
	dic = { x:'' for x in kys }
	if os.name == 'posix':
		dic['labomi'] = '/tmp/labomi/'
		os.mkdir(dic['labomi'])
	elif os.name == 'nt':
#		import platform
#		myname = platform.uname()[1]
#		myname = 'C:/Users/%s/AppData/Local/Temp/labomi/' % myname
		import tempfile
		datei = tempfile.gettempdir()
		datei = datei.replace('\\','/')
		if not datei[-1] == '/':
			datei += '/'
		datei += 'labomi/'
		dic['labomi'] = datei
#		print( datei ) #d
		if not os.path.exists(datei):
			os.mkdir(datei)

labomi = dic['labomi']
inconf = dic['inconf']
mydata = dic['mydata']
myname = dic['myname']
urpfad = dic['urpfad'] # erinnern @ 2019-11-23, für teilen mit AG
#
klogpfad  = dic['klogpfad']
kbenchlog = dic['kbenchlog']
kbenchset = dic['kbenchset']

#

### SPEICHERBEREINIGUNG / MÜLL ###
del dic
del kys
del datei
