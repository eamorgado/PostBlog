from flask import Blueprint, render_template,url_for, flash, redirect, request, session, abort
from flask_login import login_user, logout_user, current_user, login_required
from flaskblog import db, bcrypt
from flaskblog.models import User, Post
from flaskblog.users.forms import (RegistrationForm, LoginForm, UpdateAccountForm, 
                                RequestResetForm, ResetPasswordForm)
from flaskblog.users.utils import save_picture, send_reset_email

users = Blueprint('users', __name__)

'''-----------------------------------------------------------------------------
                                Register Route
-----------------------------------------------------------------------------'''
@users.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        #hashing password
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')

        #Creating user
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        
        #Adding user to session and commit
        db.session.add(user)
        db.session.commit()

        #Success message
        flash('Account created!', 'success')
        return redirect(url_for('users.login'))
    #Fail-stay on page--display errors
    return render_template('register.html', title='Register', form=form)


'''-----------------------------------------------------------------------------
                                Login Route
-----------------------------------------------------------------------------'''
@users.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():
        #Query for user
        user = User.query.filter_by(email=form.email.data).first()
        
        if user and bcrypt.check_password_hash(user.password,form.password.data):
            #Pass checks
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            flash('You have been logged in!', 'success')
            return redirect(next_page) if next_page else redirect(url_for('main.home'))
        else:
            #Pass fails
            flash('Login Unsuccessful. Check email or password', 'danger')
    #Error on login
    return render_template('login.html', title='Login', form=form)


'''-----------------------------------------------------------------------------
                                Log Out Route
-----------------------------------------------------------------------------'''
@users.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('main.home'))


'''-----------------------------------------------------------------------------
                            Account Route
-----------------------------------------------------------------------------'''
@users.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('users.account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title='Account', image_file=image_file, form=form)


'''-----------------------------------------------------------------------------
                        Personal Posts Route
-----------------------------------------------------------------------------'''
@users.route("/user/<string:username>")
def user_posts(username):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(author=user).order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template('user_posts.html', posts=posts, user=user)


'''-----------------------------------------------------------------------------
                                Reset Pass
-----------------------------------------------------------------------------'''
@users.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent with instructions to reset your password.', 'info')
        return redirect(url_for('main.login'))
    return render_template('reset_request.html', title='Reset Password', form=form)

@users.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('That is an invalid/expired token', 'warning')
        return redirect(url_for('users.reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash('Your password has been updated! You are now able to log in', 'success')
        return redirect(url_for('users.login'))
    return render_template('reset_token.html', title='Reset Password', form=form)


'''-----------------------------------------------------------------------------
                                Delete Account
-----------------------------------------------------------------------------'''
@users.route("/account/delete", methods=['POST'])
@login_required
def delete_account():
    user = User.query.filter_by(username=current_user.username).first()
    logout_user()
    db.session.delete(user)
    db.session.commit()
    flash("Account deleted. Sad to see you go :(", 'success')
    return redirect(url_for('main.home'))