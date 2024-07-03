from flask import Blueprint, render_template, url_for, flash, redirect, request
from flask_login import login_user, current_user, logout_user, login_required
from app.auth.forms import RegistrationForm, LoginForm
from app.models.user import User
from app import bcrypt, login_manager

auth_bp = Blueprint('auth_bp', __name__)

@auth_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('home_bp.form'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password_hash=hashed_password)
        user.save_to_db()
        login_user(user)
        flash('Your account has been created! You are now able to log in', 'success')
        #return redirect(url_for('auth_bp.login'))
        return redirect(url_for('home_bp.home'))
    return render_template('signup.html', title='Sign Up', form=form)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home_bp.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.find_by_email(form.email.data)
        if user and User.verify_password(user.password_hash, form.password.data):
            login_user(user, remember=False)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home_bp.home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)

@auth_bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home_bp.home'))

@login_manager.user_loader
def load_user(username):
    return User.find_by_username(username)

