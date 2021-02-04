#brings the Flask app created in __init__
from car_api import app, db, oauth
#from flask, use the jinja templates, redirection, url replacement, message flashing, session management
from flask import render_template, request, redirect, url_for, flash, session

#from forms.py
from car_api.forms import UserLoginForm
from car_api.models import User, check_password_hash

from flask_login import login_user, logout_user, current_user, login_required

import os

#makes the homepage
@app.route('/')
def home():
    return render_template('home.html')

#creates a route for the sign up page
@app.route('/signup', methods= ['GET','POST'])
def signup():
    #instantiates a class called form which was defined in forms.py
    form = UserLoginForm()
    try:
        if request.method == 'POST' and form.validate_on_submit():
            email = form.email.data
            password = form.password.data
        #prints user input to terminal for confirmation/debug purposes
            print(email,password)
            user = User(email, password = password)
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('signin'))
    except:
        raise Exception ('Invalid Form Data: Please check your form...')
    return render_template('sign_up.html', form=form)

#creates a route for the sign in page
@app.route('/signin', methods= ['GET','POST'])
def signin():
    #instantiates a class called form which was defined in forms.py
    form = UserLoginForm()
    try:
        if request.method == "POST" and form.validate_on_submit():
            email = form.email.data
            password = form.password.data
        #prints user input to terminal for confirmation/debug purposes
            print(email,password)
            #creates an instance of the User class for the current user from the first matching email in the email column in the db.
            logged_user = User.query.filter(User.email == email).first()
            #if the logged user and the user returned from the matched passwords
            if logged_user and check_password_hash(logged_user.password,password):
                #take the method to login from flask_user and login the loggeduser defined above
                login_user(logged_user)
                print(logged_user)
                #do the flash method defined on the home.html (text to display, information for the flash parameter)
                flash('You were successfully logged in via Email/Password','auth-success')
                #redirect user to home
                return redirect(url_for('home'))
            else:
                flash('Your email/password is incorrect. Please try again','auth-failure')
                #keep them on sign in page
                return redirect(url_for('signin'))
    except:
        raise Exception ('Invalid Form Data: Please check your form...')
    return render_template('sign_in.html', form=form)   

#create logout route
@app.route('/logout')
def logout():
    #run function of logout from flask_login
    logout_user()
    #if theres a session, take the session key and remove it from the active list
    if session:
        for key in list(session.keys()):
            session.pop(key)
    return redirect(url_for('home'))

#Create Google Authentication Routes
google = oauth.register(
    name='google',
    #directs the client id to the one set up in .env
    client_id=os.getenv("GOOGLE_CLIENT_ID"),
    #directs the secret key to the .env
    client_secret=os.getenv("GOOGLE_CLIENT_SECRET"),
    access_token_url='https://accounts.google.com/o/oauth2/token',
    access_token_params=None,
    authorize_url='https://accounts.google.com/o/oauth2/auth',
    authorize_params=None,
    api_base_url='https://www.googleapis.com/oauth2/v1/',
    userinfo_endpoint='https://openidconnect.googleapis.com/v1/userinfo',  # This is only needed if using openId to fetch user info
    client_kwargs={'scope': 'openid email profile'},
)

@app.route('/google-auth')
def google_auth():
    google = oauth.create_client('google')
    redirect_uri = url_for('authorize',_external = True)
    return google.authorize_redirect(redirect_uri)

@app.route('/authorize')
def authorize():
    google = oauth.create_client('google')
    token = google.authorize_access_token()
    #requests user info from
    response = google.get('userinfo')
    #saves the information given in response as a .json file
    user_info = response.json()
    user = oauth.google.userinfo()
    session['profile'] = user_info

    #searches the db for a user wiht the same email as the one provided by google
    user = User.query.filter_by(email = user_info['email']).first()
    #if user is true
    if user:
        user.first_name = user_info['given_name']
        user.last_name = user_info['family_name']
        user.email = user_info['email']
        user.g_auth_verify = user_info['verified_email']
#if none exists, the following updates the user in the table
        db.session.add(user)
        db.session.commit()
        login_user(user)
        session.permanent = True
        return redirect(url_for('home'))
    else:
        g_first_name = user_info['given_name']
        g_last_name = user_info['family_name']
        g_email = user_info['email']
        g_verified = user_info['verified_email']

        user = User(
            first_name = g_first_name,
            last_name = g_last_name,
            email = g_email,
            g_auth_verify = g_verified
        )

        db.session.add(user)
        db.session.commit()
        login_user(user)
        session.permanent = True
        return redirect(url_for('home'))

    print(user_info)
    return redirect(url_for('home'))