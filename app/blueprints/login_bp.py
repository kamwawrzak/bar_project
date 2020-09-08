from app import lm
from app.models import RegularUser

from flask import Blueprint, flash, redirect, request, url_for

from flask_login import login_user

from werkzeug.security import check_password_hash
from werkzeug.urls import url_parse


login_bp = Blueprint('login', __name__)


@lm.user_loader
def load_user(user_id):
    return RegularUser.query.get(user_id)


@login_bp.route('/v1/login', methods=['GET', 'POST'])
def login():
    d = get_form_data()
    user = RegularUser.query.filter_by(email=d['email']).first()
    if user:
        if check_password_hash(user.password_hash, d['password']):
            login_user(user)
            flash('You have logged in successfully.')
            next_page = request.args.get('next')
            if not next_page or url_parse(next_page).netloc != '':
                return redirect(url_for('index'))
            return redirect(url_for('index'))
    else:
        flash('This email address is not registered.')
        return redirect(url_for('login'))


def get_form_data():
    d = {}
    d['email'] = request.form.get('email')
    d['password'] = request.form.get('password')
    return d
