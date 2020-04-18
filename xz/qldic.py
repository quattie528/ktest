def merge2dic(dic1,dic2):
	kopfer =  list( dic1.keys() )
	kopfer += list( dic2.keys() )
	kopfer = uniq(kopfer)
	
	dic3 = {}
	for k in kopfer:
		w1 = dic1[k]
		w2 = dic2[k]
		if w1 == '' and w2 == '':
			dic3[k] = ''
		elif w1 == '' and not w2 == '':
			dic3[k] = w1
		elif not w1 == '' and w2 == '':
			dic3[k] = w2
		elif not w1 == '' and not w2 == '':
			dic3[k] = w1 + ' / ' + w2
			print( '* SICHERN : ' + dic3[k] )
	return dic3
