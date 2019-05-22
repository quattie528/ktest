import os


#############
### USAGE ###
#############
def usage(x):
	import sys
	if len(sys.argv) == 1:
		x = x.replace('.py','')
		w = 'in/9/%s.txt' % x
		if not os.path.exists(w):
			w = 'D:/adel/in/9/%s.txt' % x
			if not os.path.exists(w):
				print('no args, no usage explanation')
				exit()
		with open(w, 'r',encoding='utf-8') as f: x = f.read()
		x = '-'*50 + "\n" + x
		print(x)
		exit() # 2018-12-09
	else:
		if sys.argv[1].isdigit():
			return int( sys.argv[1] )
		else:
			return sys.argv[1]

### W zu Mac ###
def w2m(x):
	import platform
	if not platform.uname()[1] == 'mac4sushis.local':
		return x
#	x = x.replace('','')
	x = x.replace('D:/onedrive/','/User/katsushi/OneDrive/')
