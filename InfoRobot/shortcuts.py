import md5

def str_md5(src):
	m = md5.new()
	m.update(src)
	return m.hexdigest()

