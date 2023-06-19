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
admin_list = ["maya.yellin@gmail.com", "ma@test", "maya@test"]

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

    def update_admin_list(admin_list):
        existing_admins = Admin.query.all()
        existing_emails = [admin.email for admin in existing_admins]
        print("EXISTING ADMINS", str(existing_emails))
        # Find missing admins
        missing_emails = list(set(admin_list) - set(existing_emails))
        print("MISSING ADMINS", str(missing_emails))
        # Find admins to be removed
        admins_to_remove = [admin for admin in existing_admins if admin.email not in admin_list]

        for email in missing_emails:
            new_admin = Admin(email=email)
            db.session.add(new_admin)

        for admin in admins_to_remove:
            db.session.delete(admin)

        db.session.commit()

        print("UPDATED ADMINS", str(admin_list))

    update_admin_list(admin_list)

# User session management setup
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.init_app(app)

directory = "images"

if not os.path.exists(directory):
    os.makedirs(directory)

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
