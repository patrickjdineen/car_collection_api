#bring the whole flask app and database into models
from car_api import app, db, login_manager, ma
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
    token = db.Column(db.String , default = "", unique = True)
    #create automatic timestamp when account is first created
    date_created = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
    car = db.relationship('Car', backref = 'owner', lazy=True)

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

#Create a class for Car to enable addition of table, data, into postgres
class Car(db.Model):
    #creates PK of ID
    id = db.Column(db.Integer, primary_key=True)
    make = db.Column(db.String(150))
    model = db.Column(db.String(150))
    color = db.Column(db.String(150))
    price = db.Column(db.Integer)
    user_id = db.Column(db.String, db.ForeignKey('user.token'), nullable = False)

    def __init__(self, make, model,color,price,user_id):
        self.make = make
        self.model = model
        self.color = color
        self.price = price
        self.user_id = user_id
    
    def __repr__(self):
        return f'The following car {self.model} has been added to {self.user_id}s garage'
    
    def to_dict(self):
        return{
            "id":self.id,
            "make":self.make,
            "model":self.model,
            "color":self.color,
            "price":self.price
        }

class CarSchema(ma.Schema):
    class Meta:
        fields = ('id','make','model','color','price')

car_schema = CarSchema()
cars_schema = CarSchema(many = True)