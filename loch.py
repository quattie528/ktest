import os
import yaml

datei = 'D:/var/conf.txt'
if not os.path.exists(datei):
	datei = 'conf.txt'

if os.path.exists(datei):
	with open(datei) as fh:
		dic = yaml.load(fh)
else:
	dic = {
		x:''
		for x in
		['labomi','inconf','mydata','myname','kbenchlog','kbenchset']
	}

labomi = dic['labomi']
inconf = dic['inconf']
mydata = dic['mydata']
myname = dic['myname']
#
kbenchlog = dic['kbenchlog']
kbenchset = dic['kbenchset']

