from InfoRobot import app

@app.route('/api/test')
def test():
	return '{"status":200,"message":"test"}'

