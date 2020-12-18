from app import db

from flask_dance.consumer.storage.sqla import OAuthConsumerMixin

from flask_login import UserMixin


class User(db.Model, UserMixin):
    user_id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    oauth_user = db.Column(db.Boolean, default=False)
    nick = db.Column(db.String(16), unique=True, default=None)
    password_hash = db.Column(db.String(86))
    register_date = db.Column(db.String)
    image = db.Column(db.String)
    drinks_number = db.Column(db.Integer, default=0)

    def get_id(self):
        return self.user_id


class OAuth(OAuthConsumerMixin, db.Model):
    provider_user_id = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey(User.user_id))
    user = db.relationship(User)


class Drink(db.Model):
    CATEGORIES = ['whisky/bourbon', 'vodka', 'rum', 'gin', 'tequila/mezcal',
                  'other']
    TECHNIQUES = ['stir', 'shake', 'stir/shake', 'build', 'other']
    SEARCH_CRITERIA = ['drink name', 'ingredient']
    UNITS = ['ml', 'piece(s)', 'drop(s)']

    drink_id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.Integer, db.ForeignKey(User.user_id),
                       nullable=False)
    author_nick = db.Column(db.String, nullable=False)
    name = db.Column(db.String(35), nullable=False)
    category = db.Column(db.String(35), nullable=False)
    technique = db.Column(db.String(20), nullable=True)
    description = db.Column(db.String(250), nullable=True)
    preparation = db.Column(db.String(250), nullable=False)
    add_date = db.Column(db.String, nullable=False)
    image = db.Column(db.String)
    views = db.Column(db.Integer, default=0)
    avg_rate = db.Column(db.Float, default=0)


class Ingredient(db.Model):
    ingr_id = db.Column(db.Integer, primary_key=True)
    ingr_name = db.Column(db.String, nullable=False)
    ingr_amount = db.Column(db.Float)
    ingr_unit = db.Column(db.String)
    drink = db.Column(db.Integer, db.ForeignKey(Drink.drink_id),
                      nullable=False)


class Comment(db.Model):
    comment_id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.Integer, db.ForeignKey(User.user_id),
                       nullable=False)
    author_nick = db.Column(db.String, nullable=False)
    drink = db.Column(db.Integer, db.ForeignKey(Drink.drink_id),
                      nullable=False)
    date = db.Column(db.String, nullable=False)
    content = db.Column(db.String(250), nullable=False)


class Vote(db.Model):
    vote_id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.Integer, db.ForeignKey(User.user_id))
    drink = db.Column(db.Integer, db.ForeignKey(Drink.drink_id))
    value = db.Column(db.Integer)
