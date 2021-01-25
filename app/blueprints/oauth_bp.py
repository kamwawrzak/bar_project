from app import db
from app.db_interactors.user_db_inter import UserDbInter
from app.interactors.validators import Validators
from app.models import OAuth

from flask import (Blueprint, current_app, flash, redirect, request, url_for)

from flask_dance.consumer import oauth_authorized
from flask_dance.consumer.storage.sqla import SQLAlchemyStorage
from flask_dance.contrib.facebook import facebook, make_facebook_blueprint

from flask_login import current_user, login_required, login_user

from sqlalchemy.orm.exc import NoResultFound

oauth_bp = Blueprint('oauth_bp', __name__)

fb_blueprint = make_facebook_blueprint(
    client_id=current_app.config['FB_ID'],
    client_secret=current_app.config['FB_SECRET'],
    scope=['email'],
    storage=SQLAlchemyStorage(OAuth, db.session, user=current_user))


@fb_blueprint.route('/v1/facebook')
def fb_login():
    """Delete drink's image

    GET: Checks if user is authorized if so it redirects to home page.
         Otherwise start facebook OAuth authorization.
    """
    if not facebook.authorized:
        return redirect(url_for('facebook.login'))
    return redirect(url_for('home_bp.index'))


@login_required
@fb_blueprint.route('/v1/set_nick', methods=['POST'])
def set_nick():
    """Set user's nick.

    GET: Get and verify nick passed by user. Next assign its value to currently
         logged in user nick property and redirects to home page. If there is
         any issue flash the error and redirects to home page.
    Only logged in users can use this route.
    """
    if request.method == 'POST':
        nick = request.form.get('nick')
        error = Validators().validate_nick(nick)
        if not error:
            UserDbInter().update_nick(nick)
            flash('Your account has been created.', category='success')
        else:
            flash(error, category='error')
        return redirect(url_for('home_bp.index'))


@oauth_authorized.connect_via(fb_blueprint)
def fb_logged_in(blueprint, token):
    """Facebook OAuth2 authorization.

    The signal gets sent request to facebook for authorization user. If user
    can login to facebook and allows the application gets required data it
    checks if the user exists in database. If it exists it will logged in.
    Otherwise new User and OAuth objects will be added to database and then
    user will be logged in.

    Parameters
    ---------
    blueprint: OAuth2ConsumerBlueprint
        flask_dance blueprint object in this case: 'fb_blueprint'.
    token: OAuth2Token
        token received from authorization service in this case: facebook.

    Returns
    -------
    boolean
        False - to disable standard storing token data. Instead storing token
        in database has been implemented.
    """

    if not token:
        flash('Failed to log in via Facebook.', category='error')
        return False
    resp = facebook.get('me?fields=email')
    if not resp.ok:
        flash('Failed to obtain your data from Facebook.', category='error')
        return False
    user_data = resp.json()
    try:
        oauth = UserDbInter().get_oauth(blueprint.name, user_data['id'])
    except NoResultFound:
        oauth = UserDbInter().add_oauth(provider=blueprint.name,
                                        provider_user_id=user_data['id'],
                                        token=token)
    if oauth.user:
        login_user(oauth.user)
        flash('You have been logged in.', category='success')
    else:
        user = UserDbInter().add_user(email=user_data['email'],
                                      nick=None,
                                      user_type='oauth')
        UserDbInter().assign_oauth_user(oauth, user)
        login_user(user)
    return False
