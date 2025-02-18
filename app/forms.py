from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField , BooleanField, FloatField, FileField
from wtforms.validators import Email, EqualTo, DataRequired, Length
from flask_wtf.file import FileAllowed



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



class EditProfileForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=25)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    profile_image = FileField('Profile Image', validators=[FileAllowed(['jpg', 'png', 'jpeg'])])
    submit = SubmitField('Update Profile')


class ChangePasswordForm(FlaskForm):
    old_password = PasswordField('Current Password', validators=[DataRequired()])
    new_password = PasswordField('New Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm New Password', validators=[DataRequired(), EqualTo('new_password')])
    submit = SubmitField('Change Password')
