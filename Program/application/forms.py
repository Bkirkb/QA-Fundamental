from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, DecimalField, BooleanField
from wtforms.validators import DataRequired

class LogForm(FlaskForm):
    username = StringField('Please Enter a Username', validators=[DataRequired()])
    userpassword = StringField('Please Enter a Password', validators=[DataRequired()])
    forename = StringField('Please Enter your First Name', validators=[DataRequired()])
    surname = StringField('Please Enter your Surname', validators=[DataRequired()])
    email = StringField('Please Enter an Email Address')
    gear = StringField('Care to enter your gear?')
    submit = SubmitField('Log In or Register')


