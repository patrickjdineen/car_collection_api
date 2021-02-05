from functools import wraps
from flask import request, jsonify
from car_api.models import Car, User
from car_api import app
import jwt
import json
from datetime import datetime

#create function to generate json web token for user validation using JWT
def get_jwt(current_user):
    #creates a jwt_token that is encoded by JWT
    jwt_token = jwt.encode(
    {
        #sets the "owner" of the car to tie tot he token
        'owner':current_user.token,
        #sets the token based off access time (to update and increment??)
        'access_time': json.dumps(datetime.utcnow(), indent=4, sort_keys=4, default =str)
    },
    #sets part of the encoding unlock key to the secret_key of this app defined in .env
    app.config['SECRET_KEY'],
    #sets the algorith for encoding
    algorithm = 'HS256')
    return jwt_token

#helper function to define the token_required decorator to be used in routes. 
#this confirms the tocken is present and accounted for when defining access for other routes
def token_required(our_flask_function):
    # @wraps was imported above. not 100% sure what this does
    @wraps(our_flask_function)
    def decorated(*args, **kwargs):
        #first sets value of token for none
        token = None
        #x-access-token to be used in later REST calls
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token'].split(" ")[1]
        if not token:
            return jsonify({'message': 'Token is missing'}),401
        try:
            #defines variable data of the decoded JWT
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithm =['HS256'])
            #defines current_user_token variable as the matching token/owner combi
            current_user_token = User.query.filter_by(token = data['owner']).first()
            #print statements confirm in debugger
            print(token)
            print(data)
        except:
            #defines variable data of the decoded JWT
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithm =['HS256'])
            #searches the databse for the matching entry for 'owner' based on get_jwt defined above
            owner = User.query.filter_by(token = data['owner']).first()
            #uses same params as above, but if it doenst match
            if data['owner'] != owner.token:
                return jsonify({'message': 'Token is invalid'})
        return our_flask_function(current_user_token, *args,**kwargs)
    return decorated

def verify_owner(current_user_token):
    #creates owner to match car table by user_id
    owner = Car.query.filter_by(user_id = current_user_token).first()
    print(current_user_token)
    print(owner)
    #this shouldnt happen, but catches errors
    if owner == None:
        return jsonify({'message':'You dont have any cars in the garage! Add your first car!'})
    #if someone tries to access a car that isnt theirs
    if owner.user_id != current_user_token:
        return jsonify({'message':'That token is invalid for this car. You are not authorized'})
    return owner, current_user_token