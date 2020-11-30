from app import db
from app.db_interactors.comment_db_inter import CommentDbInter
from app.db_interactors.drink_db_inter import DrinkDbInter
from app.interactors.date_time_inter import DatetimeInter
from app.interactors.img_inter import ImgInter
from app.models import OAuth, User

from flask_login import current_user

from werkzeug.security import generate_password_hash


class UserDbInter:

    def get_user(self, user_id):
        user = User.query.filter_by(user_id=user_id).first()
        return user

    def user_by_nick(self, nick):
        user = User.query.filter_by(nick=nick).first()
        return user

    def user_by_email(self, email):
        user = User.query.filter_by(email=email).first()
        return user

    def get_oauth(self, blueprint, user_id):
        return OAuth.query.filter_by(provider=blueprint,
                                     provider_user_id=user_id).one()

    def add_user(self, email, user_type, img=None, password=None, nick=None):
        register_date = DatetimeInter().get_date()
        if user_type == 'regular':
            new_user = User(email=email,
                            oauth_user=False,
                            password_hash=password,
                            nick=nick,
                            nick_changed=True,
                            register_date=register_date)
            db.session.add(new_user)
            db.session.commit()
            if img:
                img_name = ImgInter().upload_img(img, new_user)
                new_user.image = img_name
                db.session.commit()
        elif user_type == 'oauth':
            new_user = User(email=email,
                            oauth_user=True,
                            register_date=register_date)
        db.session.add(new_user)
        db.session.commit()
        return new_user

    def delete_user(self, user_id):
        user = UserDbInter().get_user(user_id)
        drinks = DrinkDbInter().search_by_user(user.user_id)
        oauth = OAuth.query.filter_by(user_id=user_id).first()
        comments = CommentDbInter().get_user_comments(user_id)
        if user.image != 'default.jpg':
            ImgInter().delete_img(user)
        for d in drinks:
            if d.image != 'default.jpg':
                ImgInter().delete_img(d)
            db.session.delete(d)
        for c in comments:
            CommentDbInter().delete_comment(c.comment_id)
        db.session.delete(user)
        if oauth:
            db.session.delete(oauth)
        db.session.commit()

    def update_password(self, password):
        current_user.password_hash = generate_password_hash(password, 'SHA256')
        db.session.commit()

    def update_nick(self, nick):
        current_user.nick = nick
        db.session.commit()

    def add_oauth(self, provider, provider_user_id, token):
        oauth = OAuth(provider=provider,
                      provider_user_id=provider_user_id,
                      token=token)
        db.session.add(oauth)
        db.session.commit()
        return oauth

    def assign_oauth_user(self, oauth, user):
        oauth.user = user
        db.session.commit()
