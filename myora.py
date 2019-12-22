#!/usr/bin/python

### MODULES ###
import cx_Oracle

### VARIABLES ###
#kbench.KBDEBUG = True
DEBUG = True
DEBUG = False

#

##############
### CONFIG ###
##############
def myconn(username,password,tnsname):
	dbh = cx_Oracle.connect(username, password, tnsname)
	return dbh

##### DIREKT ###############
if __name__=='__main__':
	username='yourname'
	password = 'password'
	tnsname = 'db2019mmdd_low'
	dbh = myora.myconn(username,password,tnsname)

#

"""
##################
### 2019-12-22 ###
##################

### INSTRUCTION (non-Pythonic one) ###
* Here the description is rough

(A1) Create an account of Always Free from this weblink
https://www.oracle.com/cloud/free/

(A2) Create Autonomous Database instance

(A3) Download "instance wallet" through pressing the "database connection" button, then you can download the set of access information

(A4) Create any database, the easiest way is to go "Tool" -> "Oracle Application Express"

### INSTRUCTION (Pythonic one) ###
* Here I tried to write the description is more detailed

(B1) Install "cx_Oracle" with pip command of Python.
pip install cx_Oracle

(B2) Install Microsoft Visual C++ to use, because the module "cx_Oracle" requires it.
https://oracle.github.io/odpi/doc/installation.html#windows
Here is the weblink to install.
https://support.microsoft.com/en-us/help/2977003/the-latest-supported-visual-c-downloads

(B3) Download "instantclient_xx_x" from the weblink and unzip it.
(the current version is "instantclient_19_5")
https://www.oracle.com/database/technologies/instant-client/downloads.html

(B4) "instantclient_xx_x" is necessary to be set as PATH of system folder.

(B5) mkdir network\admin under "instantclient_xx_x"
https://docs.oracle.com/en/cloud/paas/autonomous-data-warehouse-cloud/user/connecting-nodejs.html#GUID-AB1E323A-65B9-47C4-840B-EC3453F3AD53

(B6) copy the unzipped files of wallet to "instantclient_19_5\network\admin"

(B7) open "tnsnames.ora" and remember any of access type such as "db2019xx_low"

(B8) run this program, with username, password and tnsname (which you chose at B7)

### COMMAND-LIKE SETTING ###
set oracli="C:/usr/ora/instantclient_19_5/"
set oracliconf="C:/usr/ora/instantclient_19_5/network/admin/"

download "instantclient_19_5.zip" from the website
unzip "instantclient_19_5.zip"
put the unzipped folder to %oracli%
set the path of environmental of %oracli%
mkdir %oracliconf%
unzip wallet_DB20191206.zip
move wallet_DB20191206/* %oracliconf%
"""
