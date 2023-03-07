from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
import os
from sqlalchemy import create_engine, text


app = Flask(__name__)
app.config['SECRET_KEY'] = '75e7dae5b5f9ee81336b1a190b46c71c'
#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://2naahj3wjte7sag4lgll:pscale_pw_aHoiZ6aD6S7rZCyYDAlUAXxjie1DrD5oxLxXDTaBCqh@ap-southeast.connect.psdb.cloud/sportsgowhere_db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://2naahj3wjte7sag4lgll:pscale_pw_aHoiZ6aD6S7rZCyYDAlUAXxjie1DrD5oxLxXDTaBCqh@ap-southeast.connect.psdb.cloud/sportsgowhere_db?ssl=None'

#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
# 'sqlite:///site.db'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'
app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ.get('EMAIL_USER')
app.config['MAIL_PASSWORD'] = os.environ.get('EMAIL_PASS')
mail = Mail(app)


from flaskblog import routes