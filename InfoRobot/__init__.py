from flask import Flask
app = Flask(__name__)

from InfoRobot.config import *
from mongoengine import connect
#Init database connection
connect(DB_NAME)

from InfoRobot.config import *
from InfoRobot.routes import views
from InfoRobot.routes import apis

