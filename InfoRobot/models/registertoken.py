from mongoengine import *

class RegisterToken(Document):
	registerToken = StringField()
	email = EmailField()
	expires = LongField()
