#imports general forms for use in flask
from flask_wtf import FlaskForm
#makes the components needed for the input form
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email

#creates a class to share with routes from the above imports
class UserLoginForm(FlaskForm):
    #instantiates strinfield class named email label "Email" that requires data and confirms as email type
    email = StringField('Email',validators=[ DataRequired(), Email() ])
    #instantiates passwordfield class named  password(which i beleive then gets used by uuid?) label is password and requires data)
    password = PasswordField('Password',validators = [ DataRequired() ])
    #instantiates strinfield class named submit_button from SubmitFiled
    submit_button = SubmitField()
