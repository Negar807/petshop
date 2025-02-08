from flask import render_template, Blueprint, redirect, flash, url_for
from flask_login import login_user , logout_user
from app import db
from app.forms import RegistrationForm, LoginForm
from app.models import User


auth_bp = Blueprint('auth', __name__, url_prefix='/auth')


@auth_bp.route('/register', methods = ['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username = form.username.data , email= form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Registration is Successfully', 'success')
        return redirect(url_for('auth.login'))
    return render_template('register.html', form=form)




@auth_bp.route('/login',methods = ['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email = form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            flash('Login is Successfully', 'success')
            return redirect(url_for('home.index'))
    return render_template('login.html', form=form)
    


@auth_bp.route('/logout')
def logout():
    logout_user()
    flash('You are logged out.', 'success')
    return redirect('home.index')