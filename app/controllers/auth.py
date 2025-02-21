from flask import render_template, Blueprint, redirect, flash, url_for
from flask_login import login_user , logout_user, current_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from app import db
from app.forms import RegistrationForm, LoginForm
from app.models import User


auth_bp = Blueprint('auth', __name__, url_prefix='/auth')


@auth_bp.route('/register', methods =['GET','POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home.index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data)
        user = User(email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Signup successful! Please log in.', 'success')
        return redirect(url_for('auth.login'))
    return render_template('register.html', form=form)




@auth_bp.route('/login',methods = ['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email = form.email.data).first()

        if user is None:
            flash('No account found with this email.', 'danger')
        elif not check_password_hash(user.password, form.password.data):
            flash('Incorrect password!', 'danger')
        else:
            login_user(user)
            flash('Login successful!', 'success')
            return redirect(url_for('home.index'))
        
    return render_template('login.html', form=form)
    


@auth_bp.route('/logout')
def logout():
    logout_user()
    flash('You are logged out.', 'info')
    return redirect('home.index')