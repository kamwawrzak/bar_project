from app import db

from flask_login import UserMixin


class RegularUser(db.Model, UserMixin):
    user_id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    nick = db.Column(db.String(16), unique=True, nullable=False)
    password_hash = db.Column(db.String(86), nullable=False)

    def get_id(self):
        return self.user_id


class Drink(db.Model):
    drink_id = db.Column(db.Integer, primary_key=True)
