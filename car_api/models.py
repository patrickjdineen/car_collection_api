#bring the whole flask app and database into models
from car_api import app, db, login_manager
#brining in uuid for security and user authentication
import uuid
#brining in datetime for timestamps
from datetime import datetime

#creating secure hashes for receiving and storing secure passwords
from werkzeug.security import generate_password_hash, check_password_hash

import secrets

from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

#creating the user table in the sql server
class User(db.Model, UserMixin):
    #creating PK and user ID number
    id = db.Column(db.String, primary_key = True)
    first_name = db.Column(db.String(150), nullable = True, default = "")
    last_name = db.Column(db.String(150), nullable=True, default = "")
    email = db.Column(db.String(150), nullable = False)
    #password string has no limit to allow for complex password hasing from werkzeug
    password = db.Column(db.String, nullable=True, default = "")
    #creates True/False to tie account with google authentication
    g_auth_verify = db.Column(db.Boolean, default = False)
    #token allows persistent login based on timeing - logic to follow
    token = db.Column(db.String , default = "")
    #create automatic timestamp when account is first created
    date_created = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)

    #creates method for class
    def __init__(self,email, first_name = "", last_name = "", id="", password = "",token = "",g_auth_verify = False):
        self.id = self.set_id()
        self.first_name = first_name
        self.last_name = last_name
        self.password = self.set_password(password)
        self.email = email
        self.token = self.set_token(24)
        self.g_auth_verify = g_auth_verify

    def set_token(self,length):
        return secrets.token_hex(length)

    #creates method for self.id used in __init__
    def set_id(self):
        #makes a string with uuid
        return str(uuid.uuid4())

    def set_password(self, password):
        #uses werkzeug to create password has for method defined in __init__
        self.pw_hash = generate_password_hash(password)
        return self.pw_hash

    def __repr__self(self):
        return f'User {self.email} has been added to the database'