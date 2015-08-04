def to_int(num):
	"""Convert decimal to integer for storage in DB"""
	return int(num * 100)

def to_dec(num):
	"""Convert to decimal after being retrieved from DB"""
	return "%.2f" % (float(num) / 100)