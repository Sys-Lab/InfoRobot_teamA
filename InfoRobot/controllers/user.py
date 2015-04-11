from mongoengine import *
from InfoRobot.config import *
from InfoRobot.controllers.mail import *
from InfoRobot.models.user import *
from InfoRobot.models.registertoken import *
from InfoRobot.models.accesstoken import *
from InfoRobot.models.passwordresettoken import *
from InfoRobot.shortcuts import *
from flask import jsonify, request
from urllib import quote, unquote
import random
from validate_email import validate_email
import re
from flask import render_template
import json
import time

def user_parse_action():
	action = request.args.get('action')
	if (action=='checkemail'):
		return check_email()
	elif (action=='register'):
		return register_account()
	elif (action=='login'):
		return login_account()
	elif (action=='logout'):
		return logout_account()
	elif (action=='update'):
		return update_account()
	elif (action=='getinfo'):
		return get_account_info()
	elif (action=='admin_list'):
		return list_account_admin()
	elif (action=='admin_update'):
		return update_account_admin()
	elif (action=='admin_delete'):
		return delete_account_admin()
	elif (action=='requestpasswordreset'):
		return request_password_reset()
	elif (action=='resetpassword'):
		return reset_password()
	else:
		return jsonify({'status':-1,'message':'Action not specified.'})

def register_account():
	#required params
	email = request.form.get('email')
	password = request.form.get('password')
	nickname = request.form.get('nickname')
	authority = 0
	registerTime = long(time.time())
	status = 0
	print('debug')
	#Validate optional params
	if (request.form.get('avatar') != None and request.form.get('avatar') != ''):
		avatar = request.form.get('avatar')
	else:
		avatar = 'static/images/default_avatar.png'
	if (request.form.get('phone') != None and request.form.get('phone') != ''):
		phone = request.form.get('phone')
		if (re.match('^[0-9]+$',phone)==None):
			return jsonify({'status':1,'message':'Invalid phone number.'})
	else:
		phone = ''
	if (email==None or email=='' or password==None or password=='' or nickname==None or nickname==''):
		print('Invalid input')
		return jsonify({'status':-1,'message':'Invalid input.'})
	#Validate Email address
	if (not validate_email(email)):
		return jsonify({'status':0, 'message': 'Invalid email address.'})
	if (User.objects(email=email).count()!=0):
		return jsonify({'status':2,'message':'E-mail already exists.'})
	registerToken = str_md5(str(long(time.time())) + str(random.randint(100000,999999)))
	#Save Data
	user_db = User()
	user_db.email = email
	user_db.password = str_md5(password)
	user_db.nickname = quote(nickname)
	user_db.phone = phone
	user_db.authority = authority
	user_db.registerTime = registerTime
	user_db.status = status
	user_db.avatar = avatar
	user_db.save()
	registerToken_db = RegisterToken()
	registerToken_db.registerToken = registerToken
	registerToken_db.email = email
	registerToken_db.expires = long(time.time()) + TOKEN_EXPIRES
	registerToken_db.save()
	#Send confirmation Email
	send_email([email],CONFIRMATION_EMAIL_SUBJECT, CONFIRMATION_EMAIL_CONTENT_BEFORE + HTTP_METHOD + DOMAIN + '/confirmemail?registertoken='+registerToken + CONFIRMATION_EMAIL_CONTENT_AFTER)
	return jsonify({'status':200, 'message':'Success. Confirmation email sent.'})

def activate_account():
	registerToken = request.args.get('registertoken')
	if (registerToken==None or registerToken==''):
		statusCode = -1
		return render_template('email_confirmation_page.html',status=statusCode)
	RegisterToken_db = RegisterToken.objects(registerToken=registerToken)
	if (RegisterToken_db.count() == 0):
		statusCode = 0
		return render_template('email_confirmation_page.html',status=statusCode)
	if (RegisterToken_db.first().expires < long(time.time())):
		statusCode = 1
	else:
		User.objects(email=RegisterToken_db.first().email).update(set__status=1)
		statusCode = 200
	RegisterToken_db.delete()
	return render_template('email_confirmation_page.html',status=statusCode)

def check_email():
	email = request.args.get('email')
	if (not validate_email(email)):
		return jsonify({'status':-1,'message':'Invalid Email.'})
	if (User.objects(email=email).count()>0):
		return jsonify({'status':0,'message':'Email exists.'})
	else:
		return jsonify({'status':1,'message':'Email available'})

def login_account():
	email = request.form.get('email')
	password = request.form.get('password')
	if (email==None or email=='' or password==None or password==''):
		return jsonify({'status':-1,'message':'Invalid input.'})
	if (User.objects(email=email, password=str_md5(password)).count()==0):
		return jsonify({'status':0,'message':'E-mail or password incorrect.'})
	if (User.objects(email=email).first().status==0):
		return jsonify({'status':1,'message':'Pending user. Please confirm your email.'})
	if (AccessToken.objects(email=email).count()!=0):
		AccessToken.objects(email=email).delete()
	accessToken = str_md5(str(long(time.time())) + str(random.randint(100000,999999)))
	accessToken_db = AccessToken()
	accessToken_db.email = email
	accessToken_db.accessToken = accessToken
	accessToken_db.expires = long(time.time()) + TOKEN_EXPIRES
	accessToken_db.save()
	return jsonify({'status':200,'accesstoken':accessToken,'message':'Success.'})

def logout_account():
	accessToken = request.args.get('accesstoken')
	if (not authenticate_access_token(accessToken)):
		return jsonify({'status':0,'message':'Access-token invalid.'})
	AccessToken.objects(accessToken = accessToken).delete()
	return jsonify({'status':200,'message':'Success.'})

def request_password_reset():
	email = request.args.get('email')
	if (email==None or email==''):
		return jsonify({'status':-1,'message':'Invalid input.'})
	if (User.objects(email=email).count()==0):
		return jsonify({'status':0,'message':'Email not found.'})
	token = str_md5(str(long(time.time())) + str(random.randint(100000,999999)))
	passwordResetToken_db = PasswordResetToken()
	passwordResetToken_db.email = email
	passwordResetToken_db.token = token
	passwordResetToken_db.expires = long(time.time()) + PASSWORD_RESET_TOKEN_EXPIRES
	passwordResetToken_db.save()
	send_email([email],PASSWORD_RESET_EMAIL_SUBJECT, PASSWORD_RESET_EMAIL_CONTENT_BEFORE + HTTP_METHOD + DOMAIN + '/resetpassword?token=' + token + PASSWORD_RESET_EMAIL_CONTENT_AFTER)
	return jsonify({'status':200,'message':'Success. Password reset email sent.'})

def reset_password():
	token = request.args.get('token')
	password = request.form.get('password')
	if (token==None or token=='' or password==None or password==''):
		return jsonify({'status':-1,'message':'Invalid input'})
	passwordResetToken_db = PasswordResetToken.objects(token=token)
	if (passwordResetToken_db.count()==0):
		return jsonify({'status':0,'message':'Invalid token'})
	if (passwordResetToken_db.first().expires < long(time.time())):
		return jsonify({'status':1,'message':'Token expired.'})
	email = passwordResetToken_db.first().email
	User.objects(email=email).update(set__password=str_md5(password))
	passwordResetToken_db.delete()
	return jsonify({'status':200,'message':'Success.'})

def update_account():
	accessToken = request.args.get('accesstoken')
	if (not authenticate_access_token(accessToken)):
		return jsonify({'status':0,'message':'Access-token invalid.'})
	email = get_email_by_token(accessToken)
	userInfo = {}
	if (request.form.get('nickname')!=None and request.form.get('nickname')!=''):
		userInfo['nickname'] = request.form.get('nickname')
	if (request.form.get('phone')!=None and request.form.get('phone')!=''):
		userInfo['phone'] = request.form.get('phone')
	if (request.form.get('avatar')!=None and request.form.get('avatar')!=''):
		userInfo['avatar'] = request.form.get('avatar')
	update_user_info(email,userInfo)
	return jsonify({'status':200,'message':'Success.'})

def get_account_info():
	accessToken = request.args.get('accesstoken')
	if (not authenticate_access_token(accessToken)):
		return jsonify({'status':0,'message':'Access-token invalid.'})
	userInfo = json.loads(User.objects(email=get_email_by_token(accessToken)).only('email','nickname','avatar','phone','status','registerTime').first().to_json())
	userInfo['nickname'] = unquote(userInfo['nickname'])
	return jsonify({'status':200,'message':'Success.','userinfo':userInfo})


def list_account_admin():
	accessToken = request.args.get('accesstoken')
	if (not authenticate_access_token(accessToken)):
		return jsonify({'status':0,'message':'Access-token invalid.'})
	if (User.objects(email=get_email_by_token(accessToken)).first().authority!=1):
		return jsonify({'status':1,'message':'Permission denied.'})
	users = json.loads(User.objects().only('email','nickname','avatar','phone','authority','status','registerTime').all().to_json())
	count = -1
	for userInfo in users:
		count = count + 1
		users[count]['nickname'] = unquote(userInfo['nickname'])
	return jsonify({'status':200,'message':'Success.','users':users})

def update_account_admin():
	accessToken = request.args.get('accesstoken')
	if (not authenticate_access_token(accessToken)):
		return jsonify({'status':0,'message':'Access-token invalid.'})
	if (User.objects(email=get_email_by_token(accessToken)).first().authority!=1):
		return jsonify({'status':1,'message':'Permission denied.'})
	email = request.form.get('email')
	if (User.objects(email=email).count()==0):
		return jsonify({'status':2,'message':'User not found'})
	userInfo = {}
	if (request.form.get('nickname')!=None and request.form.get('nickname')!=''):
		userInfo['nickname'] = request.form.get('nickname')
	if (request.form.get('phone')!=None and request.form.get('phone')!=''):
		userInfo['phone'] = request.form.get('phone')
	if (request.form.get('avatar')!=None and request.form.get('avatar')!=''):
		userInfo['avatar'] = request.form.get('avatar')
	if (request.form.get('status')!=None and request.form.get('status')!=''):
		userInfo['status'] = int(request.form.get('status'))
	if (request.form.get('authority')!=None and request.form.get('authority')!=''):
		userInfo['authority'] = int(request.form.get('authority'))
	update_user_info(email,userInfo)
	return jsonify({'status':200,'message':'Success'})

def delete_account_admin():
	accessToken = request.args.get('accesstoken')
	if (not authenticate_access_token(accessToken)):
		return jsonify({'status':0,'message':'Access-token invalid.'})
	if (User.objects(email=get_email_by_token(accessToken)).first().authority!=1):
		return jsonify({'status':1,'message':'Permission denied.'})
	email = request.args.get('email')
	if (User.objects(email=email).count()==0):
		return jsonify({'status':2,'message':'User not found'})
	User.objects(email=email).delete()
	return jsonify({'status':200,'message':'Success.'})


def authenticate_access_token(accessToken):
	accessToken_db = AccessToken.objects(accessToken = accessToken)
	if (accessToken_db.count()==0):
		return False
	if (User.objects(email=get_email_by_token(accessToken)).count()==0):
		return False
	if (accessToken_db.first().expires < long(time.time())):
		return False
	else:
		return True

def get_email_by_token(accessToken):
	return AccessToken.objects(accessToken=accessToken).first().email

def update_user_info(email, userInfo):
	if ('nickname' in userInfo):
		User.objects(email=email).update(set__nickname=userInfo['nickname'])
	if ('phone' in userInfo):
		User.objects(email=email).update(set__phone=userInfo['phone'])
	if ('avatar' in userInfo):
		User.objects(email=email).update(set__avatar=userInfo['avatar'])
	if ('password' in userInfo):
		User.objects(email=email).update(set__password =userInfo['password'])
	if ('status' in userInfo):
		User.objects(email=email).update(set__status=userInfo['status'])
	if ('authority' in userInfo):
		User.objects(email=email).update(set__authority=userInfo['authority'])
