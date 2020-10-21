from app import db

from flask_dance.consumer.storage.sqla import OAuthConsumerMixin

from flask_login import UserMixin


class User(db.Model, UserMixin):
    user_id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    oauth_user = db.Column(db.Boolean, default=False)
    nick = db.Column(db.String(16), unique=True)
    nick_changed = db.Column(db.Boolean, default=True)
    password_hash = db.Column(db.String(86))
    register_date = db.Column(db.String)
    image = db.Column(db.String, default='default.jpg')
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

    drink_id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.Integer, db.ForeignKey(User.user_id),
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
    author = db.Column(db.Integer, db.ForeignKey(User.user_id),
                       nullable=False)
    author_nick = db.Column(db.String, nullable=False)
    drink = db.Column(db.Integer, db.ForeignKey(Drink.drink_id),
                      nullable=False)
    date = db.Column(db.String, nullable=False)
    content = db.Column(db.String(250), nullable=False)
