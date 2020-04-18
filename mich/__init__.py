#!/usr/bin/python

### MODULES ###
#import datetime
#import os
import pprint
import uuid
import netifaces

#

######################
### MY MAC ADDRESS ###
######################
def myuuid():
	macaddr = uuid.getnode()
#	print( type(macaddr), macaddr )
	return macaddr

def mymac():
#info = netifaces.ifaddresses('eth0')[netifaces.AF_LINK] # [{'addr': '08:00:27:50:f2:51', 'broadcast': 'ff:ff:ff:ff:ff:ff'}]
	ifs = netifaces.interfaces() # ['lo', 'eth0', 'tun2']
	ifs.sort()
#	pprint.pprint( ifs ) #d
	return ifs[0]

#

####################
### ICH BIN MICH ###
####################
def ich():
	mac = myuuid()
	if mac == 251408595664979: # KAKAGAMI-1
		return 'ag'
	return False

#

##### DIREKT ###############
if __name__=='__main__':
	print( myuuid() )
#	ich()
#	kbench.enfin()
