from flask import Blueprint, render_template
from flask_login import current_user, login_required
from app.models.Model import User, Task

home = Blueprint('home', __name__)

@home.route('/')
def index():
    title = "page d'accueil"

    if current_user.is_authenticated:
      tasks = Task.query.filter_by(user_id=current_user.id).order_by(Task.date.asc()).all()
      return render_template('home/index.html', title=title, tasks=tasks)

    return render_template('home/index.html', title=title)

@home.route('/profile')
def profile():
    return render_template('profile.html', user=current_user.username)
