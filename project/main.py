# Internal imports
# from db import init_db_command
from . import game

# Python standard libraries
import json
import os

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

main = Blueprint('main', __name__)


@main.route("/")
def index():
    if current_user.is_authenticated:
        return (
            """<a style="font-family:calibri;text-align:center"/>
                <h1 style="font-size:30px" dir=rtl>שלום
                    <span>{}!</span></h1>
                    <img style="display: block;
                margin: auto;" src="{}" alt="Google profile pic"/><br>
                <a href="/form" style="text-decoration:none;"><button type="button" style="
                width: 100px;
                font-size: 20px;
                border-radius: 5px;
                padding: 10px;
                border: none;
                font-weight: 500;
                background-color: #5e1583;
                color: white;
                cursor: pointer;
                display: block;
                margin: auto;
                margin-top: 25px;">FORM</button></a><br><br><br>
                <a href="/logout" style="text-decoration:none;"><button type="button" style="
                display: block;
                width: 90px;
                font-size: 15px;
                border-radius: 5px;
                padding: 10px;
                border: none;
                font-weight: 500;
                background-color: black;
                color: white;
                cursor: pointer;
                margin: auto;
                margin-top: 25px;">LOGOUT</button></a></a>""".format(
                current_user.name, current_user.profile_pic
            )
        )
    else:
        return render_template('index.html')


@main.route('/profile')
def profile():
    return render_template('profile.html')


# @login_required
@main.route("/form", methods=["GET", "POST"])
def form():
    if request.method == "POST":
        ret_val = get_form_data()
        return ret_val

    return render_template("form.html")
