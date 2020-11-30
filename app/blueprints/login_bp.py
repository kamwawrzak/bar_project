from app import lm
from app.interactors.validators import Validators
from app.interactors.web_inter import WebInter
from app.models import User

from flask import Blueprint, flash, redirect, render_template, request, url_for

from flask_login import login_required, login_user, logout_user

from werkzeug.urls import url_parse


login_bp = Blueprint('login', __name__)


@lm.user_loader
def load_user(user_id):
    return User.query.get(user_id)


@login_bp.route('/v1/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html', title='Login')
    else:
        d = WebInter().get_form_data('email', 'password', 'remember')
        v = Validators().validate_login_data(d['email'], d['password'])
        if isinstance(v, User):
            login_user(v, remember=d['remember'])
            flash('You have been logged in', category='success')
            next_page = request.args.get('next')
            if not next_page or url_parse(next_page).netloc != '':
                return redirect(url_for('home_bp.index'))
            return redirect(url_for('home_bp.index'))
        else:
            flash(v, category='error')
            return redirect(url_for('login.login'))


@login_required
@login_bp.route('/v1/logout')
def logout():
    logout_user()
    flash('You have been logged out.', category='success')
    return redirect(url_for('home_bp.index'))
