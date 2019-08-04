import pickle

def obj2bin(obj,bin):
	gh = open(bin,'wb')
	pickle.dump(obj, gh)
	gh.close()
#	__tell_output(bin)

def bin2obj(bin):
#	print( bin ) #d
	gh = open(bin,'rb')
	obj = pickle.load(gh)
	gh.close()
	return obj

def binbin(f1,f2):
	if os.path.exists(f2):
		if os.path.getmtime(f1) < os.path.getmtime(f2):
			obj = bin2obj(f2)
			return obj
	obj = xz.txt2ldic(f1)
	obj2bin(obj,f2)
	return obj

def bin2erb(bin,etc):
	if os.path.exists(bin):
		try:
			return bin2obj(bin)
		except EOFError:
			return etc
	else:
		return etc
