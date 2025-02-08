from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField , BooleanField, FloatField
from wtforms.validators import Email, EqualTo, DataRequired, Length



class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=25)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('SignUp')


class LoginForm(FlaskForm):
    email = StringField('email', validators=[DataRequired(), Email()])
    password = PasswordField('password', validators=[DataRequired()])
    submit = SubmitField('Login')



class Paymenrt(FlaskForm):
    card_number = StringField('Card Number', validators=[DataRequired(), Length(min=16,max=16)])
    card_holder = StringField('Card Holder', validators=[DataRequired(),Length(min=3,max=25)])
    amount = FloatField('Amount', validators=[DataRequired()])
    submit = SubmitField('Pay Now')