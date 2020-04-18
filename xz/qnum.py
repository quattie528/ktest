
def sym2int(x,sym):
	assert sym in 'KMBTPA'
	if sym == 'A':
		sym = 1
	elif sym == 'K':
		sym = 1000
	elif sym == 'M':
		sym = 1000 ** 2
	elif sym == 'B':
		sym = 1000 ** 3
	elif sym == 'T':
		sym = 1000 ** 4
	else:
		sym = 0
	x = x * sym
	return x

