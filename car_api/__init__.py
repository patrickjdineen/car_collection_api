#makes this a Flask program
from flask import Flask

#imports Config class defined in config.py takes information, secret key, etc 
from config import Config

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

#imports flask login loginManager class which does a lootttt
from flask_login import LoginManager

#imports OAuth class from the authentication library
from authlib.integrations.flask_client import OAuth

#import of masrhmallow
from flask_marshmallow import Marshmallow

#create the application from class type Flask
app = Flask(__name__)
app.config.from_object(Config)
#danmes db as a instance of class SQLAlchemy
db = SQLAlchemy(app)
#names migrate as a insance of class Migrate, referencing SQL Alchemy class insteance and the whole application
migrate = Migrate(app, db)
#creates instance of LoginManager class for the app
login_manager  =LoginManager(app)
#specifies which page to load for non-logged in users
login_manager.login_view = 'signin'

#creates instance of oauth class for use within the app
oauth = OAuth(app)

#instantiates marshmallow for use in app
ma = Marshmallow(app)

#bringing in routes.py and models.py
from car_api import routes, models