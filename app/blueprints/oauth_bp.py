from app import db
from app.db_interactors.user_db_inter import UserDbInter
from app.interactors.nick_creator import NickCreator
from app.interactors.validators import Validators
from app.models import OAuth

from flask import (Blueprint, current_app, flash, redirect, render_template,
                   request, url_for)

from flask_dance.consumer import oauth_authorized
from flask_dance.consumer.storage.sqla import SQLAlchemyStorage
from flask_dance.contrib.facebook import facebook, make_facebook_blueprint

from flask_login import current_user, login_required, login_user

from sqlalchemy.orm.exc import NoResultFound

oauth_bp = Blueprint('oauth_bp', __name__)

fb_blueprint = make_facebook_blueprint(
    client_id=current_app.config['FB_ID'],
    client_secret=current_app.config['FB_SECRET'],
    redirect_to='facebook.set_nick',
    storage=SQLAlchemyStorage(OAuth, db.session, user=current_user))


@fb_blueprint.route('/v1/facebook')
def fb_login():
    if not facebook.authorized:
        return redirect(url_for('facebook.login'))
    else:
        return redirect(url_for('home_bp.index'))


@login_required
@fb_blueprint.route('/v1/set_nick', methods=['GET', 'POST'])
def set_nick():
    if request.method == 'POST':
        user = UserDbInter().get_user(current_user.user_id)
        if user.nick_changed:
            redirect(url_for('home_bp.index'))
        else:
            nick = request.form.get('nick')
            error = Validators().validate_nick(nick)
            if not error:
                UserDbInter().update_nick(nick)
                return redirect(url_for('home_bp.index'))
            else:
                flash(error)
                return redirect('/v1/set_nick')
    else:
        return render_template('set_nick.html', title='Set Nick')


@oauth_authorized.connect_via(fb_blueprint)
def fb_logged_in(blueprint, token):
    if not token:
        flash('Failed to log in via Facebook.')
        return False
    resp = blueprint.session.get('/me?fields=id,email')
    if not resp.ok:
        flash('Failed to get user data')
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
        flash('Logged in successfully.')
    else:
        temp_nick = NickCreator().create_temp_nick(user_data['email'])
        user = UserDbInter().add_user(email=user_data['email'],
                                      nick=temp_nick,
                                      user_type='oauth')
        UserDbInter().assign_oauth_user(oauth, user)
        login_user(user)
        flash('Sign in successfully.')
    return False
