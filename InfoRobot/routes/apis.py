from InfoRobot import app
from flask import jsonify
from InfoRobot.controllers.user import *

@app.route('/api/test')
def test():
	return jsonify({"status":200,"message":"test"})

@app.route('/api/user',methods=['POST','GET'])
def user():
	return user_parse_action()
