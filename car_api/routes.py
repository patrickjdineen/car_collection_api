#brings the Flask app created in __init__
from car_api import app
#from flask, use the jinja templactes
from flask import render_template, request, redirect, url_for

#from forms.py
from car_api.forms import UserLoginForm


#makes the homepage
@app.route("/")
def home():
    return render_template("home.html")

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
    except:
        raise Exception ('Invalid Form Data: Please check your form...')
    return render_template('sign_in.html', form=form)   

#creates a route for the sign up page
@app.route('/signup', methods= ['GET','POST'])
def signup():
    #instantiates a class called form which was defined in forms.py
    form = UserLoginForm()
    try:
        if request.method == "POST" and form.validate_on_submit():
            email = form.email.data
            password = form.password.data
        #prints user input to terminal for confirmation/debug purposes
            print(email,password)
    except:
        raise Exception ('Invalid Form Data: Please check your form...')
    return render_template('sign_up.html', form=form)