from flask import render_template
from InfoRobot import app

@app.route('/')
def index():
	return render_template('hello.html')
