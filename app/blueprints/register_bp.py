from app import db
from app.models import RegularUser

from flask import Blueprint, flash, redirect, request, url_for

from werkzeug.security import generate_password_hash


register_bp = Blueprint('register_bp', __name__)


@register_bp.route('/v1/register', methods=['GET', 'POST'])
def register_post():
    d = get_form_data()
    error = check_data(d['email'], d['nick'], d['password'], d['confirm_pass'])
    if error is None:
        pass_hash = generate_password_hash(d['password'], method='SHA256')
        new_user = RegularUser(email=d['email'], nick=d['nick'],
                               password_hash=pass_hash)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('index'))
    else:
        flash(error)
        return redirect(url_for('registration'))


def get_form_data():
    d = {'email': request.form.get('email'),
         'nick': request.form.get('nick'),
         'password': request.form.get('password'),
         'confirm_pass': request.form.get('confirm')}
    return d


def check_data(email, nick, password, confirm_pass):
    if not email:
        error = 'Email is required.'
    elif not nick:
        error = 'Nick name is required.'
    elif not password:
        error = 'Password is required.'
    elif RegularUser.query.filter_by(email=email).first():
        error = 'This email address is already registered.'
    elif RegularUser.query.filter_by(nick=nick).first():
        error = 'This nickname already exists'
    elif password != confirm_pass:
        error = "Password and Confirm Password don't match."
    elif validate_password(password) is not None:
        error = validate_password(password)
    else:
        error = None
    return error


def validate_password(password):
    specials = ['!', '@', '#', '$', '%', '^', '&', '*', '(', ')']
    if len(password) > 15:
        error = 'Password is too long'
    elif len(password) < 8:
        error = 'Password is too short.'
    elif not any(char.isdigit() for char in password):
        error = 'Password must contain at least one digit'
    elif not any(char.isupper() for char in password):
        error = 'Password must contain at least one capital letter'
    elif not any(char.islower() for char in password):
        error = 'Password must contain at least one lower letter'
    elif not any(char in specials for char in password):
        error = 'Password must contain at least of symbols: !@#$%^&*()'
    elif any(char == ' ' for char in password):
        error = 'Password cannot include spaces'
    else:
        error = None
    return error
