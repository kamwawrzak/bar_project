from . import db


class RegularUser(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password_hash = db.Column(db.String(86), nullable=False)


class Drink(db.Model):
    pass
