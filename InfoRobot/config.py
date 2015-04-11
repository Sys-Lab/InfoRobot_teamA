from mongoengine import connect

#Host Info
DOMAIN = '127.0.0.1:5000'
HTTP_METHOD = 'http://'

#Database Name
DB_NAME = 'InfoRobot'

#Email Account
EMAIL_HOST = 'smtp.163.com'
EMAIL_USER_NAME = 'inforobot123'
EMAIL_PASSWORD = 'syslab123'
EMAIL_POSTFIX = '163.com'
EMAIL_ME_NAME = 'InfoRobot'

#Token (in seconds)
TOKEN_EXPIRES = 60*60*24*30
PASSWORD_RESET_TOKEN_EXPIRES = 60*60*24

#Confirmation email
CONFIRMATION_EMAIL_SUBJECT = 'Email Confirmation - InfoRobot'
CONFIRMATION_EMAIL_CONTENT_BEFORE = 'Thank you for signing up! Please confirm your email address by clicking the link below:<br/>'
CONFIRMATION_EMAIL_CONTENT_AFTER = '<br/>InfoRobot'

#Password reset email
PASSWORD_RESET_EMAIL_SUBJECT = 'Reset Password - InfoRobot'
PASSWORD_RESET_EMAIL_CONTENT_BEFORE = 'To reset your password, please click the link below:<br/>'
PASSWORD_RESET_EMAIL_CONTENT_AFTER = '<br/>InfoRobot'
