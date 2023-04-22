# Third-party libraries
from flask import Flask
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import *
import os
from flask_login import LoginManager


def create_app():
    # Flask app setup
    app = Flask(__name__)
    app.secret_key = os.environ.get("SECRET_KEY") or os.urandom(24)

    global db, game_db

    with app.app_context():
        # Initialize the first database
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite?timeout=30'
        db = SQLAlchemy(app)
        """
        # Initialize the second database
        app.config['SQLALCHEMY_BINDS'] = {'game': 'sqlite:///game_db.sqlite'}
        game_db = SQLAlchemy(app)
        game_db.session.rollback()  # rollback to avoid dropping tables of the main database.
        """

        from .models import User, Admin
        # from .game_model import GameData

        # Create the databases
        db.create_all()

        db.init_app(app)
        # game_db.init_app(app)

    # User session management setup
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    # Flask-Login helper to retrieve a user from our db
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(user_id)

    # blueprint for auth routes in our app
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    # blueprint for non-auth parts of app
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app
