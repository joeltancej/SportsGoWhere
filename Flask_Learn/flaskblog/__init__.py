from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager


app = Flask(__name__)
app.config['SECRET_KEY'] = '75e7dae5b5f9ee81336b1a190b46c71c'
# Change <password> and <database> to your respective local database's one (without the <>)
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://root:password@localhost/sportsgowhere"
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'


from flaskblog import routes