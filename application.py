# Internal imports
# from db import init_db_command
from user import User
from game import Game, get_form_data

# Python standard libraries
import json
import os

# Third-party libraries
from flask import Flask, redirect, request, url_for, render_template, jsonify, abort
from flask_login import (
    LoginManager,
    current_user,
    login_required,
    login_user,
    logout_user,
)
from oauthlib.oauth2 import WebApplicationClient
import requests
from dotenv import load_dotenv

load_dotenv()

# Configuration
GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID", None)
GOOGLE_CLIENT_SECRET = os.environ.get("GOOGLE_CLIENT_SECRET", None)
GOOGLE_DISCOVERY_URL = (
    "https://accounts.google.com/.well-known/openid-configuration"
)

# Flask app setup
app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY") or os.urandom(24)
id = 0

# User session management setup
# https://flask-login.readthedocs.io/en/latest
login_manager = LoginManager()
login_manager.init_app(app)

# Naive database setup
"""try:
    init_db_command()
except sqlite3.OperationalError:
    # Assume it's already been created
    pass
"""
# OAuth 2 client setup
client = WebApplicationClient(GOOGLE_CLIENT_ID)


# Flask-Login helper to retrieve a user from our db
@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)


@app.route("/")
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
        return render_template('login.html')


def get_google_provider_cfg():
    return requests.get(GOOGLE_DISCOVERY_URL).json()


@app.route("/login")
def login():
    # Find out what URL to hit for Google login
    google_provider_cfg = get_google_provider_cfg()
    authorization_endpoint = google_provider_cfg["authorization_endpoint"]

    # Use library to construct the request for Google login and provide
    # scopes that let you retrieve user's profile from Google
    request_uri = client.prepare_request_uri(
        authorization_endpoint,
        redirect_uri=request.base_url + "/callback",
        scope=["openid", "email", "profile"],
    )
    return redirect(request_uri)


@app.route("/login/callback")
def callback():
    # Get authorization code Google sent back to you
    code = request.args.get("code")

    # Find out what URL to hit to get tokens that allow you to ask for
    # things on behalf of a user
    google_provider_cfg = get_google_provider_cfg()
    token_endpoint = google_provider_cfg["token_endpoint"]

    # Prepare and send a request to get tokens! Yay tokens!
    token_url, headers, body = client.prepare_token_request(
        token_endpoint,
        authorization_response=request.url,
        redirect_url=request.base_url,
        code=code
    )
    token_response = requests.post(
        token_url,
        headers=headers,
        data=body,
        auth=(GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET),
    )

    # Parse the tokens!
    client.parse_request_body_response(json.dumps(token_response.json()))

    # Now that you have tokens (yay) let's find and hit the URL
    # from Google that gives you the user's profile information,
    # including their Google profile image and email
    userinfo_endpoint = google_provider_cfg["userinfo_endpoint"]
    uri, headers, body = client.add_token(userinfo_endpoint)
    userinfo_response = requests.get(uri, headers=headers, data=body)

    # You want to make sure their email is verified.
    # The user authenticated with Google, authorized your
    # app, and now you've verified their email through Google!
    if userinfo_response.json().get("email_verified"):
        unique_id = userinfo_response.json()["sub"]
        users_email = userinfo_response.json()["email"]
        picture = userinfo_response.json()["picture"]
        users_name = userinfo_response.json()["given_name"]
    else:
        return "User email not available or not verified by Google.", 400

    # Create a user in your db with the information provided
    # by Google
    user = User(
        id_=unique_id, name=users_name, email=users_email, profile_pic=picture
    )

    # Doesn't exist? Add it to the database.
    if not User.get(unique_id):
        User.create(unique_id, users_name, users_email, picture)

    # Begin user session by logging the user in
    login_user(user)

    # Send user back to homepage
    return redirect(url_for("index"))


# @login_required
@app.route("/form", methods=["GET", "POST"])
def form():
    if request.method == "POST":
        ret_val = get_form_data()
        return ret_val

    return render_template("form.html")


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("index"))


def create_app():
    return app


if __name__ == "__main__":
    app.run(host="0.0.0.0", ssl_context='adhoc', port=443, threaded=True, debug=True)
