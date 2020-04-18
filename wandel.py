import urllib.parse

def url2encode(url):
	# e.g.
	x = urllib.parse.quote(url)
	return x

def url2decode(url):
	x = urllib.parse.unquote(url)
	return x
	#
	# beispiel
	x = '/%7Eguido/'
	y = url2decode(x)
	print( y ) #-> '/~guido/'
