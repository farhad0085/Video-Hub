from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)
app.config['SECRET_KEY'] = '16fqe212d26d32be23e608ac5a5d828db0as4f3a4'
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///videodb.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# bcrypt for encript password and verify
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)

# set login view when a logged out user tried to access logged in contents
login_manager.login_view = 'login'
# text bootstrap class
login_manager.login_message_category = 'warning'

db = SQLAlchemy(app)

from app import routes # imported here, because we can't import this in the beginning
