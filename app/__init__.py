from flask import Flask, render_template

from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate, MigrateCommand
from pytz import timezone
from dotenv import load_dotenv
from app.models import db, ma
import os

# init SQLAlchemy so we can use it later in our models
migrate = Migrate()
login_manager = LoginManager()

def create_app():
    APP_ROOT = os.path.join(os.path.dirname(__file__), "..")
    app = Flask(__name__, instance_path=os.path.join(APP_ROOT,"instance"))

    # Environment configurations
    APP_ROOT = os.path.join(os.path.dirname(__file__), "..")
    dotenv_path = os.path.join(APP_ROOT, ".env")
    load_dotenv(dotenv_path)
    app.config.from_object('config.settings.' + os.environ.get('FLASK_ENV'))

    # Initialize extensions
    db.init_app(app)
    ma.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)
    migrate.init_app(app,db)

    from app.models import Model
    from app.models.Model import User, Task

    with app.app_context():
        # create DB tables
        db.create_all()

        # Small HTTP Error Handling
        @app.errorhandler(404)
        def not_found(error):
          title = 'page not found'
          return render_template('errors/404.html', title=title), 404

        @login_manager.user_loader
        def load_user(user_id):
          return User.query.get(int(user_id))

        # blueprint for auth routes in our app
        from app.views.auth import auth as auth_blueprint
        app.register_blueprint(auth_blueprint)

        # blueprint for non-auth parts of app
        from app.views.home import home as home_blueprint
        app.register_blueprint(home_blueprint)

        # blueprint for tasks
        from app.views.task import task as task_blueprint
        app.register_blueprint(task_blueprint)

        # blueprint for categories
        from app.views.category import category as category_blueprint
        app.register_blueprint(category_blueprint)

        return app
