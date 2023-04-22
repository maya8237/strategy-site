# Internal imports
# from db import init_db_command
from . import game

# Python standard libraries
import json
import os
from functools import wraps

# Third-party libraries
from flask import Flask, redirect, request, url_for, render_template, jsonify, abort, Blueprint
from flask_login import (
    LoginManager,
    current_user,
    login_required,
    login_user,
    logout_user,
)
from . import db
from .models import Admin

main = Blueprint('main', __name__)



# returns if user received is an admin
def is_admin(user):
    if not user.is_authenticated:
        return False
    admin = Admin.query.filter_by(email=user.email).first()
    return admin is not None


# defines a decorator that checks if the current user is an admin
def admin_required(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            return current_app.login_manager.unauthorized()
        else:
            if not is_admin(current_user):
                abort(403)
        return func(*args, **kwargs)
    return decorated_function


# load default variables and functions
def template(file, **kwargs):
    kwargs['is_admin'] = is_admin
    return render_template(file, **kwargs)


@main.route("/")
def index():
    return template('index.html')


@login_required
@main.route('/profile')
def profile():
    return template('profile.html', name=current_user.name)


@admin_required
@login_required
@main.route("/form", methods=["GET", "POST"])
def form():
    if request.method == "POST":
        ret_val = get_form_data()
        return ret_val

    return template("form.html", name=current_user.name)
