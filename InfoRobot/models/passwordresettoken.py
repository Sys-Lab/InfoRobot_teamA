from mongoengine import *

class PasswordResetToken(Document):
	token = StringField()
	email = EmailField()
	expires = LongField()
