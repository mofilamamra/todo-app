from functools import wraps
from flask import url_for, request, redirect, session, flash
from app.models.Model import User

def requires_access_level(access_level):
  def decorator(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
      user = User.query.filter_by(email=session['email']).first()
      if not session.get('email'):
        return redirect(url_for('auth.login'))
      elif not user.allowed(access_level):
        flash("Vous n'avez pas accès à cette page. Désolé!")
        return redirect(url_for('home.index'))
      return f(*args, **kwargs)
    return decorated_function
  return decorator
