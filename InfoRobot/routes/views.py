from flask import render_template
from InfoRobot import app
from InfoRobot.controllers.user import activate_account

@app.route('/')
def index():
	return render_template('hello.html')

@app.route('/confirmemail')
def confirm_email():
	return activate_account()

@app.route('/resetpassword')
def reset_password():
	return render_template('password_reset_page.html')
