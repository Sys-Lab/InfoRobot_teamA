from flask import Flask
app = Flask(__name__)

from InfoRobot.routes import views
from InfoRobot.routes import apis
