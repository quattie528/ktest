#!/usr/bin/python

### MODULES ###
from bs4 import BeautifulSoup as soup
import re
#
import xz
#import kbench
from datsun import *

#

######################
### LINK EXTRACTOR ###
######################
def linkextractor(src):
	src = xz.txt2str(src)
	doc = soup(src,'lxml') # recommended
	links = [ element.get('href') for element in doc.find_all('a') ]
	return links

#

#####################
### HTML to TABLE ###
#####################
def html2tbl(src,index):
	src = xz.txt2str(src)
	doc = soup(src,'lxml') # recommended
	res = []
	for element in doc.find_all('table')[index]:
		try:
			lis = [ x.text for x in element ]
		except AttributeError:
			x = str(element)
			x = re.sub("<br/?>",'',x)
			x = re.sub(">[\s\n\r]+",'>',x)
			x = re.sub("[\s\n\r]+<",'<',x)
			#
			x = re.sub("<t[drh] .+?>",'',x)
			x = re.sub("</?t[drh]>","\t",x)
			x = re.sub("</?(span|a|sup|thead|tbody)>",'',x)
			#
			x = re.sub("<a href.+?>",'',x)
			x = re.sub("<img .+?>",'',x)
			x = re.sub("<span .+?>",'',x)
#			print( x )
			lis = x.split("\t")
		res.append(lis)
	return res

#

#####################
### HTML to TABLE ###
#####################
def html2values(src):
	src = xz.txt2str(src)
	doc = soup(src,'lxml') # recommended
	res = []
	for element in doc.find_all('li'):
		res.append( element.text )
	return res

#

######################
### HTML to TABLES ###
######################
def html2tbls(src):
	res = []
	i = 0
	while 1:
		try:
			tbl = html2tbl(src,i)
		except IndexError:
			break
		res.append(tbl)
		i += 1
	return res
