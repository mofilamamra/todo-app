# auth.py

from flask import Blueprint, render_template, redirect, url_for, request, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required
from app.models.Model import User, ACCESS
from app.models import db
from app.forms.user import LoginForm , RegisterForm
from app.utils.utils import requires_access_level

auth = Blueprint('auth', __name__)


@auth.route('/identifier', methods=['GET', 'POST'])
def login():
    title = 'identifier'
    form = LoginForm()
    if request.method == 'GET':
      return render_template('auth/login.html', title=title, form=form)
    
    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    user = User.query.filter_by(email=email).first()

    # check if user actually exists
    # take the user supplied password, hash it, and compare it to the hashed password in DB
    if not user or not check_password_hash(user.password, password):
        flash('Please check your login details and try again.')
        return redirect(url_for('auth.login'))

    # if the above check passes, then we know the user has the right credentials
    login_user(user, remember=remember)
    session['email'] = email
    return redirect(url_for('home.index'))


@auth.route('/inscrire', methods=['GET','POST'])
@login_required
@requires_access_level(ACCESS['admin'])
def register():
    title = 'inscrire'
    form = RegisterForm()
    if request.method == 'GET':
        return render_template('auth/register.html', title=title, form=form)

    email = request.form.get('email')
    username = request.form.get('username')
    password = request.form.get('password')
    hashed_password = generate_password_hash(password,method="sha256")
    category_id = request.form.get("category")

    # if this returns a user, then the email already exists in database
    user = User.query.filter_by(email=email).first()

    if user:  # if a user is found, we want to redirect back to signup page so user can try again
        flash("L'adresse mail existe déjà")
        return redirect(url_for('auth.register'))

    if form.validate_on_submit():
      new_user = User(username,email,hashed_password,category_id)
      # add the new user to DB.
      db.session.add(new_user)
      db.session.commit()

      flash("Merci pour l'inscription")
      return redirect(url_for('home.index'))
    else:
      return render_template("auth/register.html", title=title, form=form)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    session.pop('email', None)
    return redirect(url_for('home.index'))
