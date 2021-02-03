#imports user operating system
import os

#creates pass to whatever os base directory os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config():
    #Creation of Secret Key required for security??
    SECRET_KEY = os.environ.get('SECRET KEY') or 'This is a warning for guessing?'
    #tells sql alchemy to look at .env for the database URL defined there
    #or statement creates backup database in case of failure
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sql:///' + os.path.join(basedir, 'app.db')
    #turns off SQL ntifications from every transaction to database
    SQLALCHEMY_TRACK_MODIFICATIONS = False