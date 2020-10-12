from app import db

from flask_login import UserMixin


class RegularUser(db.Model, UserMixin):
    user_id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    nick = db.Column(db.String(16), unique=True, nullable=False)
    password_hash = db.Column(db.String(86), nullable=False)
    register_date = db.Column(db.String, nullable=False)
    image = db.Column(db.String, default='default.jpg')
    drinks_number = db.Column(db.Integer, default=0)

    def get_id(self):
        return self.user_id


class Drink(db.Model):
    drink_id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.Integer, db.ForeignKey(RegularUser.user_id),
                       nullable=False)
    name = db.Column(db.String(35), nullable=False)
    category = db.Column(db.String(35), nullable=False)
    technique = db.Column(db.String(20), nullable=True)
    description = db.Column(db.String(250), nullable=True)
    preparation = db.Column(db.String(250), nullable=False)
    ingredients = db.Column(db.String(250), nullable=False)
    add_date = db.Column(db.String, nullable=False)
    image = db.Column(db.String(250),
                      default='default.jpg')


class Comment(db.Model):
    comment_id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.Integer, db.ForeignKey(RegularUser.user_id),
                       nullable=False)
    author_nick = db.Column(db.String, nullable=False)
    drink = db.Column(db.Integer, db.ForeignKey(Drink.drink_id),
                      nullable=False)
    date = db.Column(db.String, nullable=False)
    content = db.Column(db.String(250), nullable=False)
