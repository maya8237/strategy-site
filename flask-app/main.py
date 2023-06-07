# Python standard libraries
from functools import wraps

# Third-party libraries
from flask import redirect, request, url_for, render_template, abort, Blueprint
from flask_login import (
    current_user,
    login_required,
)

from game import Game
from models import Admin
from admin_tools import template, is_admin

main = Blueprint('main', __name__)


@main.route("/")
def index():
    return template('index.html')


@main.route('/profile')
@login_required
def profile():
    return template('profile.html', name=current_user.name)


@main.route("/form", methods=["GET", "POST"])
@login_required
def form():
    if request.method == "POST":
        ret_val = Game()
        # add duplicate games(that are ignored) to different database
        if type(ret_val) == Game:
            return redirect(url_for('main.after_form'))
        else:
            print("game object not returned")

    return template("form.html", name=current_user.name)


@main.route("/after_form")
@login_required
def after_form():
    return template("after_form.html", name=current_user.name)

