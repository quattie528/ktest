def condlist(*lis_and_conds):
	res = lis_and_conds[0]
	conds = lis_and_conds[1:]
	#
	assert isinstance(res, list)
	for x in conds: assert callable(x)
	#
	for cond in conds:
		res = [ x for x in res if cond(x) ]
	return res

def replist(*lis_and_conds):
	res = lis_and_conds[0]
	conds = lis_and_conds[1:]
	#
	assert isinstance(res, list)
	for x in conds: assert callable(x)
	#
	for cond in conds:
		res = [ cond(x) for x in res ]
	return res

def whitelist(x,condlist):
	for cond in condlist:
		if cond in x:
			return True
	return False

def blacklist(x,condlist):
	for cond in condlist:
		if cond in x:
			return False
	return True
