from app import db
from app.db_interactors.comment_db_inter import CommentDbInter
from app.db_interactors.drink_db_inter import DrinkDbInter
from app.db_interactors.vote_db_inter import VoteDbInter
from app.interactors.date_time_inter import DatetimeInter
from app.interactors.img_inter import ImgInter
from app.models import OAuth, User

from flask_login import current_user

from werkzeug.security import generate_password_hash


class UserDbInter:

    def get_user(self, user_id):
        """User getter.

        Function finds User object by user_id property and returns it.

        Parameters
        ----------
        user_id: int

        Returns
        ----------
        User
            Single User object.
        """
        return User.query.filter_by(user_id=user_id).first()

    def user_by_nick(self, nick):
        """User by nick getter.

        Function finds User object by nick property and returns it.

        Parameters
        ----------
        nick: string

        Returns
        ----------
        User
            Single User object.
        """
        return User.query.filter_by(nick=nick).first()

    def user_by_email(self, email):
        """User by email getter.

        Function finds User object by email property and returns it.

        Parameters
        ----------
        email: string

        Returns
        ----------
        User
            Single User object.
        """
        return User.query.filter_by(email=email).first()

    def get_oauth(self, blueprint, user_id):
        """OAuth getter.

        Function finds OAuth object for specific blueprint and specific User.

        Parameters
        ----------
        blueprint: String
            Name of OAuth2 provider for example: facebook
        user_id: int

        Returns
        ----------
        OAuth
            Single OAuth object.
        """
        return OAuth.query.filter_by(provider=blueprint,
                                     provider_user_id=user_id).one()

    def add_user(self, email, user_type, img=None, password=None, nick=None):
        """Add new user.

        Function creates new User object and add it to database. Optionally it
        upload image do S3 bucket.

        Parameters
        ----------
        email: String
        user_type: String
            It takes two values: 'regular' for normal register user or 'oauth'
            for users register via OAuth2 protocol.
            Name of OAuth2 provider for example: facebook
        img: FileStorage
        password: String
        nick: String

        Returns
        ----------
        User
            New User object.
        """
        register_date = DatetimeInter().get_date()
        default_link = ImgInter().get_default_img('user')
        if user_type == 'regular':
            new_user = User(email=email,
                            oauth_user=False,
                            password_hash=password,
                            nick=nick,
                            register_date=register_date,
                            image=default_link)
            db.session.add(new_user)
            db.session.commit()
            if img:
                img_name = ImgInter().upload_img(img, new_user)
                new_user.image = img_name
                db.session.commit()
        elif user_type == 'oauth':
            new_user = User(email=email,
                            oauth_user=True,
                            register_date=register_date,
                            image=default_link)
        db.session.add(new_user)
        db.session.commit()
        return new_user

    def delete_user(self, user_id):
        """Delete user.

        Function delete User object and assigned to that user OAuth, Drink,
        Vote and Comment objects from database. If user's image is different
        than default it also delete this image from S3 bucket.

        Parameters
        ----------
        user_id: int
        """
        user = UserDbInter().get_user(user_id)
        oauth = OAuth.query.filter_by(user_id=user_id).first()
        drinks = DrinkDbInter().user_all_drinks(user_id)
        if user.image != ImgInter().get_default_img('user'):
            ImgInter().delete_img(user)
        CommentDbInter().delete_many_comments(user_id=user_id)
        VoteDbInter().delete_user_votes(user_id)
        for d in drinks:
            DrinkDbInter().delete_drink(d.drink_id)
        db.session.delete(user)
        if oauth:
            db.session.delete(oauth)
        db.session.commit()

    def update_password(self, password):
        """Update password.

        Function hash new password and assign it to currently logged in user
        password property.

        Parameters
        ----------
        password: String
        """
        current_user.password_hash = generate_password_hash(password, 'SHA256')
        db.session.commit()

    def update_nick(self, nick):
        """Update nick.

        Function assigns passed nick to currently logged in user nick property.
        It should be used for Users logged in via OAuth2 protocol.

        Parameters
        ----------
        nick: String
        """
        current_user.nick = nick
        db.session.commit()

    def add_oauth(self, provider, provider_user_id, token):
        """Add new OAuth.

        Function creates new OAuth object and add it to database.

        Parameters
        ----------
        provider: String
            Name of OAuth authorization provider for example: 'facebook'
        provider_user_id: String
            User id in provider's database
        token: String
            Token received from OAuth provider.
        """
        oauth = OAuth(provider=provider,
                      provider_user_id=provider_user_id,
                      token=token)
        db.session.add(oauth)
        db.session.commit()
        return oauth

    def assign_oauth_user(self, oauth, user):
        """Assign User to OAuth object.

        Function assigns User object to user propert of OAuth object.

        Parameters
        ----------
        oauth: OAuth
        user: User
        """
        oauth.user = user
        db.session.commit()
