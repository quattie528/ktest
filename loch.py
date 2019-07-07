import os
import pprint
import yaml

datei = 'D:/var/conf.txt'
if os.name == 'posix':
	datei = '/Users/katsushi/vw/var/conf.txt'
if not os.path.exists(datei):
	datei = 'conf.txt'

if os.path.exists(datei):
	with open(datei) as fh:
		dic = yaml.load(fh,Loader=yaml.BaseLoader)
else:
	dic = {
		x:''
		for x in
		['labomi','inconf','mydata','myname','kbenchlog','kbenchset']
	}
	if os.name == 'posix':
		dic['labomi'] = '/tmp/labomi/'
		os.mkdir(dic['labomi'])
	elif os.name == 'nt':
		import platform
		myname = platform.uname()[1]
		myname = 'C:/Users/%s/AppData/Local/Temp/labomi/' % myname
		dic['labomi'] = myname

labomi = dic['labomi']
inconf = dic['inconf']
mydata = dic['mydata']
myname = dic['myname']
urpfad = dic['urpfad']
#
klogpfad  = dic['klogpfad']
kbenchlog = dic['kbenchlog']
kbenchset = dic['kbenchset']

dic = None
