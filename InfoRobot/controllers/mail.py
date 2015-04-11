from InfoRobot.config import *
import smtplib
from email.MIMEText import MIMEText

def send_email(to_list,sub,content):
	me = EMAIL_ME_NAME + '<' + EMAIL_USER_NAME + '@' + EMAIL_POSTFIX + '>'
	msg = MIMEText(content, _subtype='html',_charset='utf-8')
	msg['Subject'] = sub
	msg['From'] = me
	msg['To'] = ';'.join(to_list)
	try:
		s = smtplib.SMTP()
		s.connect(EMAIL_HOST)
		s.login(EMAIL_USER_NAME + '@' + EMAIL_POSTFIX, EMAIL_PASSWORD)
		s.sendmail(me, to_list, msg.as_string())
		s.close()
	except Exception, e:
		print(str(e))
