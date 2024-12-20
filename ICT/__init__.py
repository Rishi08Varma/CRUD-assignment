from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'  
app.config['SECRET_KEY'] = 'your_secret_key_here'  

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = "Login"
login_manager.login_message_category = "info"

from ICT import routes
