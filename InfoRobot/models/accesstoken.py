from mongoengine import *

class AccessToken(Document):
	accessToken = StringField()
	email = EmailField()
	expires = LongField()
