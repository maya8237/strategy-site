# Third-party libraries
from flask import Flask
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import *
import os
from flask_login import LoginManager

# Flask app setup
app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY") or os.urandom(24)

app.config['SECRET_KEY'] = app.secret_key
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_BINDS'] = {
    'games': 'sqlite:///games.db'
}
db = SQLAlchemy(app)
with app.app_context():
    from models import *

    db.create_all()
    db.init_app(app)

# User session management setup
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.init_app(app)


# Flask-Login helper to retrieve a user from our db
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


# blueprint for auth routes in our app
from auth import auth as auth_blueprint

app.register_blueprint(auth_blueprint)

# blueprint for non-auth parts of app
from main import main as main_blueprint

app.register_blueprint(main_blueprint)

# blueprint for admin info-processing parts of app
from admin_tools import admin_tools as admin_tools_blueprint

app.register_blueprint(admin_tools_blueprint)
