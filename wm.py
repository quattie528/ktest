#!/usr/bin/python

# Name als Huldigung zu Wes McKinney, das ist für zahlen
# name as homage to Wes McKinney

### MODULES ###
import pandas as pd
import matplotlib.pyplot as plt
import xi
import datetime

#A

############################
### COMPLETE TIME SERIES ###
############################
def complete_ts(tsdf):
	index = pd.date_range(tsdf.index[1],tsdf.index.max())

	values = [ x for x in range(len(index)) ]
	tsdf2 = pd.DataFrame(values,index=index)

	tsdf = tsdf.combine_first(tsdf2).fillna(method='ffill')
	del tsdf[0]
	return tsdf


def ts4pd(tsdf):
	lis = list(tsdf)
	res = []
	seh = int(lis[0])
	
	if isinstance(seh, int):
		if seh < 10000 and seh >= 1980:
			for x in lis:
				assert x < 10000
				assert x >= 1980
		elif seh < 400000 and seh >= 198001:
			for x in lis:
				assert x < 400000
				assert x >= 198001
				j = x // 100
				m = x % 100
				x = datetime.date(j,m,1)
				res.append(x)
		else:
			raise ValueError
	else:
		print( lis )
	
	return res

#

###################
### CAST SERIES ###
###################
def cast_series(ser,dtype):
#	assert( isinstance(ser, pandas.core.series.Series) )
	typ = str( ser.dtype )
	if dtype == typ:
		return ser
	elif typ == 'object':
		if dtype == 'string':
			return ser
	if dtype == 'datetime64':
#		print( ser )
		return pd.to_datetime(ser)
#	print( typ, dtype ) #d
#	print( list(ser) ) #d
	return ser.astype(dtype)

#

#################
### SET DTYPE ###
#################
def set_dtype(df,dic):
	kys = tuple( df.columns )
	for k in dic.keys(): assert k in kys
	#
#	df.info()
	for k in kys:
		dtype = str( df[k].dtype )
		signal = dic[k]
		if dtype == 'object' and signal == 's':
			continue
		elif 'int' in dtype and signal == 'i':
			continue
		elif 'float' in dtype and signal == 'f':
			continue
		#
		if signal == 's':
			df[k] = df[k].astype('object')
		elif signal == 'i':
			df[k] = df[k].astype('int8')
		elif signal == 'f':
			df[k] = df[k].astype('float64')
		elif signal == 'd':
			vars = list( df[k] )
			df[k] = pd.to_datetime(vars)
	return df

def saveimg(ph,weg,negate=True):
	fig = ph.get_figure()
	fig.savefig(weg)
	#
	fig = xi.negate(weg)
	fig.save(weg)

#

"""
mx = my.index.max() + 1
list( range( mx, mx+len(ldic), 1 ) )

Wes says html2table, in his book, p182
"""

##### DIREKT ###############
if __name__=='__main__':
	pass
	pass # this might be deleted
