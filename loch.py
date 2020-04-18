### MODUL ###
import os
#import pprint
import yaml

### KOPFER ###
#kys = [
#	'labomi','inconf','mydata','myname','urpfad',
#	'klogpfad','kbenchlog','kbenchset'
#]
kys = [
	'labomi','myhost',
	'mywkpl','mydwld',
	#
	'mymart','myderi','mylogg','mymeta',
	'mylang','myhow2','mysymb','mycols',
	#
	'kbenchlog','kbenchset',
]

### HAUPT ###
datei = 'C:/usr/proc/conf.yml'
#datei = 'D:/var/debug.txt' #d
if os.name == 'posix':
	datei = '~/.maconf.txt'
if not os.path.exists(datei):
	datei = 'conf.yml'
#	datei = 'debug.txt' #d

if os.path.exists(datei):
	with open(datei) as fh:
		dic = yaml.load(fh,Loader=yaml.BaseLoader)
else:
	dic = { x:'' for x in kys }
	if os.name == 'posix':
		dic['labomi'] = '/tmp/labomi/'
		if not os.path.exists( dic['labomi'] ):
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

#

### KONSTANT-IEREN ###
labomi = dic['labomi']
myhost = dic['myhost'] # erinnern Weber "Ruf, Ruk, Beruf" @ 2020-04-05
#
mywkpl = dic['mywkpl'] # erinnern @ 2019-11-23, für teilen mit AG
mydwld = dic['mydwld'] # My Workplace and Download
#
mymart = dic['mymart']
myderi = dic['myderi']
mylogg = dic['mylogg']
mymeta = dic['mymeta']
mylang = dic['mylang']
myhow2 = dic['myhow2']
mysymb = dic['mysymb']
mycols = dic['mycols']
#
kbenchlog = dic['kbenchlog']
kbenchset = dic['kbenchset']

#

### SPEICHERBEREINIGUNG / MÜLL ###
del dic
del kys
del datei
