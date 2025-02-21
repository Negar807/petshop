from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField , BooleanField, FloatField, FileField
from wtforms.validators import Email, EqualTo, DataRequired, Length, ValidationError
from flask_wtf.file import FileAllowed
from app.models import User



class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=25 )])
    email = StringField('Email', validators=[DataRequired(), Email(message='Invalid email format')])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8, message='Password must be at least 8 characters long')])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password', message='Passwords do not match')])
    submit = SubmitField('SignUp')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('This email is already registered. Please log in or use another email.')



class LoginForm(FlaskForm):
    email = StringField('email', validators=[DataRequired(), Email(message='Invalid email format')])
    password = PasswordField('password', validators=[DataRequired(), Length(min=8)])
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
