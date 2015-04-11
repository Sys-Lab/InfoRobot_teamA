from mongoengine import *

class User(Document):
	email = EmailField()
	password = StringField()
	nickname = StringField()
	phone = StringField()
	authority = IntField()			# 0 for normal users; 1 for administrators
	registerTime = LongField()
	status = IntField()				# 0 for pending users; 1 for active users
	avatar = StringField()
