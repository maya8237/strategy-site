from . import db
from flask_login import UserMixin

from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    name = db.Column(db.String(1000), nullable=False)
    google = db.Column(db.Integer, nullable=False, default=0)

    def __repr__(self):
        return '<User %r>' % self.email
    """

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    """


class Admin(db.Model):
    __tablename__ = 'admins'
    # id = db.Column(db.Integer, primary_key=True)
    # email = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False, primary_key=True)

    def __repr__(self):
        return '<Admin %r>' % self.email


"""
class User(db.Model, UserMixin):
    __tablename__ = 'users'
    __table__ = db.Model.metadata.tables['users']
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))
    google = db.Column(db.Integer, default=0)


class Admin(db.Model):
    __tablename__ = 'admins'
    __table__ = db.Model.metadata.tables['admins']
    email = db.Column(db.String(120), unique=True, nullable=False)

"""
