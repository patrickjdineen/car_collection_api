#makes this a Flask program
from flask import Flask

#imports Config class defined in config.py takes information, secret key, etc 
from config import Config

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

#create the application from class type Flask
app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)
migrate = Migrate(app, db)

#brining in routes.py and models.py
from car_api import routes