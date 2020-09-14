from app import lm
from app.models import RegularUser
from app.web_interactors import WebInteractors

from flask import Blueprint, flash, redirect, render_template, request, url_for

from flask_login import login_required, login_user, logout_user

from werkzeug.security import check_password_hash
from werkzeug.urls import url_parse


login_bp = Blueprint('login', __name__)


@lm.user_loader
def load_user(user_id):
    return RegularUser.query.get(user_id)


@login_bp.route('/v1/login')
def login():
    return render_template('login.html', title='Login')


@login_bp.route('/v1/login', methods=['GET', 'POST'])
def login_post():
    d = WebInteractors().get_form_data('email', 'password', 'remember')
    v = validate_data(d['email'], d['password'])
    if v:
        login_user(v, remember=d['remember'])
        flash('You have logged in successfully.')
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            return redirect(url_for('home_bp.index'))
        return redirect(url_for('home_bp.index'))
    else:
        flash(v)
        return redirect(url_for('login_bp.login'))


@login_required
@login_bp.route('/v1/logout')
def logout():
    logout_user()
    flash('You have been logged out')
    return redirect(url_for('home_bp.index'))


def validate_data(email, password):
    user = RegularUser.query.filter_by(email=email).first()
    if not user:
        return 'This email is not registered'
    elif not check_password_hash(user.password_hash, password):
        return 'Incorrect password'
    else:
        return user
